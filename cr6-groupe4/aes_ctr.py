"""
author: Paul Vie
"""

from Crypto.Cipher import AES
import os
import base64
import random
import itertools
import argparse

def xor(a, b):
    return bytes([x ^ y for x, y in zip(a, b)])


def add_16(a, b):
    return ((int.from_bytes(a, "big") + int.from_bytes(b, "big")) % 2**128).to_bytes(
        16, "big"
    )


def AES_CTR_encrypt(key, plaintext, iv):
    table = []
    random.seed(int.from_bytes(iv, "big"))
    for i in range(0, len(plaintext), 16):
        table.append(plaintext[i : i + 16])
    table[-1] = table[-1] + (b"\x00" * (16 - len(table[-1])))
    for i in range(0, len(table)):
        compteur = bytearray(random.getrandbits(8) for _ in range(16))
        table[i] = xor(
            table[i], AES.new(key, AES.MODE_ECB).encrypt((add_16(iv, compteur)))
        )
    return b"".join(table)


def AES_CTR_decrypt(key, ciphertext, iv):
    table = []
    random.seed(int.from_bytes(iv, "big"))
    for i in range(0, len(ciphertext), 16):
        table.append(ciphertext[i : i + 16])
    for i in range(0, len(table)):
        compteur = bytearray(random.getrandbits(8) for _ in range(16))
        table[i] = xor(
            table[i], AES.new(key, AES.MODE_ECB).encrypt(add_16(iv, compteur))
        )
    return table


alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_=+!@#$%^&*()[]{}|;:,.<>?`~"


def test_AES_CTR():
    # Test with all possible plaintexts of length 2
    for elem in itertools.product(alphabet, repeat=2):
        plaintext = bytes("".join(elem), "utf-8")
        AES_key = os.urandom(16)
        iv = os.urandom(16)
        cyphertext = AES_CTR_encrypt(AES_key, plaintext, iv)
        returnplaintext = AES_CTR_decrypt(AES_key, cyphertext, iv)
        returnplaintext[-1] = returnplaintext[-1].replace(b"\x00", b"")
        returntext = b"".join(returnplaintext)
        if plaintext != returntext:
            print("Error")
            return False
    print("Success")
    # Test with plaintexts of random length 1 to 1000
    random_len_of_msg = [random.randint(1, 1000) for i in range(100)]
    for len_msg in random_len_of_msg:
        number_of_test = 100
        for elem in itertools.product(alphabet, repeat=len_msg):
            if number_of_test == 0:
                break
            plaintext = bytes("".join(elem), "utf-8")
            AES_key = os.urandom(16)
            iv = os.urandom(16)
            cyphertext = AES_CTR_encrypt(AES_key, plaintext, iv)
            returnplaintext = AES_CTR_decrypt(AES_key, cyphertext, iv)
            # delete padding
            returnplaintext[-1] = returnplaintext[-1].replace(b"\x00", b"")
            returntext = b"".join(returnplaintext)
            if plaintext != returntext:
                print("Error")
                return False
            number_of_test -= 1
    print("Success")



if __name__ == "__main__":
    argparse = argparse.ArgumentParser()
    argparse.add_argument(
        "--mode",
        type=str,
        choices=["demo", "test"],
        help="Mode",
        required=True,
    )
    argparse.add_argument(
        "-p", "--plaintext",
        type=str,
        help="Text to encrypt",
    )
    args = argparse.parse_args()
    if args.mode == "demo":
        if not args.plaintext:
            raise ValueError("Please provide a plaintext")
        AES_key = os.urandom(16)
        iv = os.urandom(16)
        plaintext = args.plaintext.encode()
        cyphertext = AES_CTR_encrypt(AES_key, plaintext, iv)
        print(f"Cyphertext : {base64.b64encode(cyphertext)}")
        returnplaintext = AES_CTR_decrypt(AES_key, cyphertext, iv)
        print(f"Decrypted plaintext : {returnplaintext}")
        print("Plaintext recovered: ", end="")
        for returntext in returnplaintext:
            print(bytes.decode(returntext), end="")
        print()
    if args.mode == "test":
        test_AES_CTR()
