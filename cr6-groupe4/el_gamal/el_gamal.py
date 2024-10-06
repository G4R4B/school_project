import random
from math import ceil, sqrt
import subprocess
import argparse


        
        
    
import sys
def miller_rabin(n):
    p = n-1
    s = 0
    while p % 2 == 0:
        p = p // 2
        s += 1
    for _ in range(50):
        a = random.randint(2, n-1)
        x = pow(a, p, n)
        if x == 1 or x == n-1:
            continue
        for _ in range(s-1):
            x = pow(x, 2, n)
            if x == n-1:
                break
        else:
            return False
    return True

def generate_prime(bits):
    while True:
        p = random.getrandbits(bits)
        if p % 2 == 0:
            p += 1
        if miller_rabin(p):
            if miller_rabin(2*p+1):
                return 2*p+1

        
def generator_of_the_group(p):
		p1 = 2
		p2 = (p-1) // p1
		while(True):
			g = random.randint(2, p-1)
			if pow(g, (p-1)//p1, p) != 1 and pow(g, (p-1)//p2, p) != 1:
				return g

def el_gamal_encrypt(p, g, A, plaintext):
    b = random.randint(2, p-2)
    B = pow(g, b, p)
    c = (pow(A, b, p) * plaintext) % p
    return B, c 

def el_gamal_decrypt(p, a, B, c):
    return (c * pow(B, p-1-a, p)) % p

def el_gamal_break(p, g, A):
    # BSGS
    #find bsgs file
    find = subprocess.Popen(["find", ".", "-name", "bsgs"], stdout=subprocess.PIPE)
    out = find.communicate()
    out = out[0].decode("utf-8")
    out = out.split("\n")
    bsgs = out[0]
    # run bsgs
    batcmd = bsgs + " {} {} {}".format(A, p, g)
    try:
        result = subprocess.check_output(batcmd, shell=True)
        result = result.decode("utf-8")
        result = result.split("a = ")[1].split("\n")[0]
        return int(result)
    except subprocess.CalledProcessError as e:
        print("p is too large, breaking the key is not possible on this machine, try with more RAM or a smaller prime number")
    return None
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="El Gamal encryption")
    parser.add_argument("--mode", type=str, choices=["encrypt", "decrypt", "break", "demo"], help="Mode", required=True)
    parser.add_argument("-p", type=int, help="prime number")
    parser.add_argument("-g", type=int, help="generator of the group")
    parser.add_argument("-a", type=int, help="private key")
    parser.add_argument("-A", type=int, help="public key")
    parser.add_argument("-B", type=int, help="public key")
    parser.add_argument("-c", "--cypher", type=int, help="cyphertext")
    parser.add_argument("--plain", type=str, help="plaintext to encrypt")
    
    args = parser.parse_args()
    if args.mode == "demo":
        p = generate_prime(44) # for demo purposes we use a small prime
        g = generator_of_the_group(p)
        a = random.randint(2, p-2)
        A = pow(g, a, p)
        text = b"hello"
        plaintext = int.from_bytes(text, "big")

        if (plaintext > p):
            print("Error plaintext too long")
            exit()

        B, cyphertext = el_gamal_encrypt(p, g, A, plaintext)

        print("Plaintext: ", plaintext.to_bytes(ceil(plaintext.bit_length() / 8), "big"))
        print(f"p: {p}, g: {g}, a: {a}, h: {A}, C2: {B}, cyphertext: {cyphertext.to_bytes(ceil(cyphertext.bit_length() / 8), 'big')}")
        abis = el_gamal_break(p, g, A)
        if abis is not None:
            print("Private key breaked: ", abis)
            plaintext = el_gamal_decrypt(p, abis, B, cyphertext)
            print("Plaintext recovered: ", plaintext.to_bytes(ceil(plaintext.bit_length() / 8), "big"))

    if args.mode == "encrypt":
        if args.plain is None:
            print("Error: missing arguments")
            exit()
        plaintext = args.plain.encode("utf-8")
        p = generate_prime(256)
        g = generator_of_the_group(p)
        a = random.randint(2, p-2)
        A = pow(g, a, p)
        plaintext = int.from_bytes(plaintext, "big")

        if (plaintext > p):
            print("Error plaintext too long")
            exit()

        B, cyphertext = el_gamal_encrypt(p, g, A, plaintext)

        print("Plaintext: ", plaintext.to_bytes(ceil(plaintext.bit_length() / 8), "big"))
        print(f"p: {p}\ng: {g}\na: {a}\nA: {A}\nB: {B}\ncyphertext: {cyphertext}")
        returntext = el_gamal_decrypt(p, a, B, cyphertext)
        print("Plaintext recovered from decryption: ", returntext.to_bytes(ceil(returntext.bit_length() / 8), "big"))
        
    if args.mode == "decrypt":
        if args.p is None or args.a is None or args.B is None:
            print("Error: missing arguments")
            exit()
        p = args.p
        a = args.a
        B = args.B
        cyphertext = int(args.cypher)
        plaintext = el_gamal_decrypt(p, a, B, cyphertext)
        print("Plaintext: ", plaintext.to_bytes(ceil(plaintext.bit_length() / 8), "big"))
    if args.mode == "break":
        if args.p is None or args.g is None or args.A is None:
            print("Error: missing arguments")
            exit()
        p = args.p
        g = args.g
        A = args.A
        a = el_gamal_break(p, g, A)
        if a is not None:
            print("Private key breaked: ", a)
        if args.cypher is not None and args.B is not None:
            B = args.B
            cyphertext = int(args.cypher)
            plaintext = el_gamal_decrypt(p, a, B, cyphertext)
            print("Plaintext recovered: ", plaintext.to_bytes(ceil(plaintext.bit_length() / 8), "big"))


