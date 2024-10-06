import unittest
import os
from garbled_circuits import new_garbled_circuit, evaluate

import sys

sys.path.append('../ot_rsa/')
import ot_rsa 

sys.path.append('../circuits_and_vm/')
import circuits
import virtual_machine 

import random
import time

def value_to_8_bits(value):
    assert 0 <= value and value < 256
    bits = [int(i) for i in bin(value)[2:]]
    return [0] * (8 - len(bits)) + bits


def output_to_value(bits):
    value = 0
    for i in range(len(bits)):
        value += bits[i][1] * 2 ** i
    return value

def temps_prevu(number_for_the_moment, total_number, time_start):
    return total_number / number_for_the_moment * (time.time() - time_start)

class TestGarbledCircuits(unittest.TestCase):
    def test_garbled_circuits(self):
        init_vector_aes = os.urandom(16)
        Keyrand = os.urandom(16)
        input_size_bits = 8
        time_start = time.time()
        circuit_graph, in_a_nodes, in_b_nodes, out_a_nodes, out_b_nodes = circuits.create_min_n(input_size_bits)
        for a_value in range(256):
            print("Dure depuis :","{:.2f}".format(time.time() - time_start), "temps prévu : ", "{:.2f}".format(temps_prevu(a_value + 1, 255, time_start)), end="\r")
            b_value = random.randint(0, 255) # garbled_circuits too long to run with 256^2 tests
            a_bits = value_to_8_bits(a_value)
            b_bits = value_to_8_bits(b_value)

    
            bobs = { node.index: (ot_rsa.Bob(), b_bit) for node, b_bit in zip(in_b_nodes, b_bits) }

            garbled_circuit, alice_in_keys, bobs_with_alice_msgs = new_garbled_circuit(
                circuit_graph, init_vector_aes, in_a_nodes, in_b_nodes, out_a_nodes, out_b_nodes, a_bits, bobs)

            out_a_results, _out_b_results = evaluate(
                    circuit_graph, in_a_nodes, in_b_nodes, out_a_nodes, out_b_nodes, init_vector_aes,
                    garbled_circuit, alice_in_keys, bobs_with_alice_msgs)
                # Testing against simple min because is already too long to run
            min_value = min(a_value, b_value)
            self.assertEqual(min_value, output_to_value(out_a_results))

                # # Testing against circuits 
                # circuits_min_bits = circuits.min_n(a_bits, b_bits)
                # circuits_min_value = bits_to_value(circuits_min_bits)
                # # TODO: self.assertEqual with out_a_results_decrypted

                # # Testing against VM 
                # a_vm_bits, b_vm_bits = virtual_machine.test(a_bits, b_bits, input_size_bits, circuit_graph)
                # a_vm_value, b_vm_value = bits_to_value(a_vm_bits), bits_to_value(b_vm_bits)
                # # TODO: self.assertEqual with out_a_results_decrypted


if __name__ == "__main__":
    unittest.main()
