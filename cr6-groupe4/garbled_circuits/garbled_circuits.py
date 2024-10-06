"""
Authors: Avon FitzGerald, Louka Chenal 
"""

import sys

from collections import defaultdict
import random
import os
sys.path.append('../')
sys.path.append('../ot_rsa/')
import ot_rsa
import aes_ctr

sys.path.append('../circuits_and_vm/')
import circuits 
from circuits import Graph, NodeType, Node

code = b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f'

def new_garbled_circuit(graph, init_vector_aes, in_nodes_a, in_nodes_b, output_a, output_b, a_bits, bobs):
    keys = defaultdict(dict)
    garbled_tables = {}
    
    for node in graph.vertex:
        if not (node.type == NodeType.OUT):
            if not any([x.type == NodeType.OUT and x.name == "B" for x in node.childs]):
                    keys[node.index] = [os.urandom(16) for _ in range(2)]
                    while keys[node.index][0] == keys[node.index][1]:
                        keys[node.index][1] = os.urandom(16)

    a_in_keys = defaultdict(dict)

    for a_bit, node in zip(a_bits, in_nodes_a):
        a_in_keys[node.index] = keys[node.index][a_bit]
        
    
    bot_received_from_ot = defaultdict(dict)

    for node in in_nodes_b:
        alice = ot_rsa.Alice()
        bob, bob_private_value = bobs[node.index]

        alice_public_tuple = alice.to_bob1(int.from_bytes((keys[node.index][0]), "big"), int.from_bytes((keys[node.index][1]), "big"))
        bob_v = bob.to_alice1(alice_public_tuple, bob_private_value)
        alice_encrypted_msg_0, alice_encrypted_msg_1 = alice.to_bob2(bob_v)
        message = bob.to_alice2(alice_encrypted_msg_0, alice_encrypted_msg_1)
        if message != int.from_bytes((keys[node.index][0]), "big") and message != int.from_bytes((keys[node.index][1]), "big"):
            print(f"MESSAGE: {message}")
            raise Exception("Bob did not receive the correct message from Alice")
        bot_received_from_ot[node.index] = {
            "bob": bob,
            "message": message
        }
    
    for node in graph.vertex:
        if not (node.type == NodeType.OUT):
            if not any([x.type == NodeType.OUT and x.name == "B" for x in node.childs]):
                garbled_tables[node.index] = new_garbled_table(node, keys, init_vector_aes)
            else:
                garbled_tables[node.index] = new_garbled_table_for_output(node, keys, init_vector_aes)
    return garbled_tables, a_in_keys, bot_received_from_ot


def new_garbled_table_for_output(node, keys, iv):

    garbled_table = []
    if node.type == NodeType.AND:
        for input_j in range(2):
            for input_k in range(2):
                key = keys[node.ancestors[0].index][input_j], keys[node.ancestors[1].index][input_k]
                encrypt_key = aes_ctr.AES_CTR_encrypt(key[0], aes_ctr.AES_CTR_encrypt(key[1], input_j*input_k.to_bytes(1, "big") + code, iv), iv)
                garbled_table.append(encrypt_key)
    elif node.type == NodeType.NOT:
        for input_j in range(2):
            key = keys[node.ancestors[0].index][input_j] 
            encrypt_key = aes_ctr.AES_CTR_encrypt(key, ((input_j + 1) % 2).to_bytes(1, "big") + code, iv)
            garbled_table.append(encrypt_key)
            
    elif node.type == NodeType.XOR:
        for input_j in range(2):
            for input_k in range(2):
                key = keys[node.ancestors[0].index][input_j], keys[node.ancestors[1].index][input_k]
                encrypt_key = aes_ctr.AES_CTR_encrypt(key[0], aes_ctr.AES_CTR_encrypt(key[1], ((input_j + input_k) % 2) .to_bytes(1, "big") + code, iv), iv)
                garbled_table.append(encrypt_key)
    random.shuffle(garbled_table)
    return garbled_table

def new_garbled_table(node, keys, iv):
    garbled_table = []
    if node.type == NodeType.AND:
        for input_j in range(2):
            for input_k in range(2):
                key = keys[node.ancestors[0].index][input_j], keys[node.ancestors[1].index][input_k]
                encrypt_key = aes_ctr.AES_CTR_encrypt(key[0], aes_ctr.AES_CTR_encrypt(key[1], keys[node.index][input_j*input_k] + code, iv), iv)
                garbled_table.append(encrypt_key)
    elif node.type == NodeType.NOT:
        for input_j in range(2):
            key = keys[node.ancestors[0].index][input_j] 
            encrypt_key = aes_ctr.AES_CTR_encrypt(key, keys[node.index][(input_j + 1) % 2] + code,iv)
            garbled_table.append(encrypt_key)
            
    elif node.type == NodeType.XOR:
        for input_j in range(2):
            for input_k in range(2):
                key = keys[node.ancestors[0].index][input_j], keys[node.ancestors[1].index][input_k]
                encrypt_key = aes_ctr.AES_CTR_encrypt(key[0], aes_ctr.AES_CTR_encrypt(key[1], keys[node.index][(input_j + input_k) % 2] + code, iv), iv)
                garbled_table.append(encrypt_key)
    random.shuffle(garbled_table)
    return garbled_table


def evaluate(circuit_graph, in_a_nodes, in_b_nodes, out_a_nodes, out_b_nodes, init_vector_aes, garbled_circuit, a_in_keys, bob_received_from_ot):
    results = defaultdict(dict)

    assert len(in_a_nodes) == len(a_in_keys)

    for node in in_a_nodes:
        results[node.index] = a_in_keys[node.index]

    for node_index, bob_received_from_ot in bob_received_from_ot.items():

        results[node_index] = bob_received_from_ot["message"].to_bytes(16, "big")

    topological_order = circuit_graph.topological_sort()
    for node in topological_order: 
        if node.type == NodeType.IN:
            continue

        # If one of the params in None, either:
        # - The inputs were not initialised properly in results (if node's type is INPUT)
        # - The topological order is wrong 

        key = None

        if node.type == NodeType.NOT:
            param = results[node.ancestors[0].index]
            assert param is not None
            key = param
        elif node.type in { NodeType.XOR, NodeType.AND }:
            first_param = results[node.ancestors[0].index]
            second_param = results[node.ancestors[1].index]
            assert first_param is not None and second_param is not None
            key = first_param, second_param

        if node.type == NodeType.NOT:
            
            garbled_table = garbled_circuit[node.index]
            garbled_decrypted_values = [aes_ctr.AES_CTR_decrypt(key , x, init_vector_aes) for x in garbled_table]
        elif node.type in { NodeType.XOR, NodeType.AND }:
            garbled_table = garbled_circuit[node.index]
            garbled_decrypted_values = [aes_ctr.AES_CTR_decrypt(key[1], b''.join(aes_ctr.AES_CTR_decrypt(key[0], x, init_vector_aes)), init_vector_aes) for x in garbled_table]

        has_found_result = False

        for x in garbled_decrypted_values:
            if x[1] == code:
                has_found_result = True
                result = x[0]
                results[node.index] = result
            elif b''.join(x)[1:17] == code:
                has_found_result = True
                result = x[0][0]
                results[node.index] = result

        assert has_found_result

    out_a_indices = { x.index for x in out_a_nodes }
    out_a_results = [ (k,v) for k, v in results.items() if k in out_a_indices ]
    
    out_b_indices = { x.index for x in out_b_nodes }
    out_b_results = [ (k,v) for k, v in results.items() if k in out_b_indices ]
    
    return out_a_results, out_b_results