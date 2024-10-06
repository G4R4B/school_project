"""
author: Paul Vie
"""
import random
import math
import base64
import argparse
import subprocess


def miller_rabin(n):
    p = n - 1
    s = 0
    while p % 2 == 0:
        p = p // 2
        s += 1
    for _ in range(50):
        a = random.randint(2, n - 1)
        x = pow(a, p, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
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
            return p


def extended_gcd(a, b):
    if b == 0:
        return (a, 1, 0)
    else:
        d, x, y = extended_gcd(b, a % b)
        return (d, y, x - (a // b) * y)


def modinv(a, m):
    d, x, y = extended_gcd(a, m)
    if d != 1:
        raise ValueError("Modular inverse does not exist")
    return x % m


def generate_keypair(bits):
    p = generate_prime(bits)
    q = generate_prime(bits)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537
    if e >= phi:
        raise ValueError("e must be less than phi")
    if extended_gcd(e, phi)[0] != 1:
        raise ValueError("e must be coprime with phi")
    d = modinv(e, phi)
    return (n, e), (n, d)


def rsa_break(n):
    #find rho_pollard file
    find = subprocess.Popen(["find", ".", "-name", "rho_pollard"], stdout=subprocess.PIPE)
    out = find.communicate()
    out = out[0].decode("utf-8")
    out = out.split("\n")
    out = out[0]
    if not out:
        raise ValueError("rho_pollard not found (you must compile it)")
    # run rho_pollard
    batcmd = out + " {}".format(n)
    result = subprocess.check_output(batcmd, shell=True)
    result = result.decode("utf-8")
    print(result)
    factors = result.split("\n")
    return int(factors[0].split(" = ")[1]), int(factors[1].split(" = ")[1])
    
    

def decrypt_with_known_factors(ciphertext, public, factors):
    p, q = factors
    phi = (p - 1) * (q - 1)
    d = modinv(public[1], phi)
    return pow(ciphertext, d, public[0])

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
    parser.add_argument("--mode", type=str, choices=["encrypt", "decrypt", "break", "demo"], help="Mode", required=True)
    parser.add_argument("--bits", type=int, default=64, help="Number of bits for the key")
    parser.add_argument("-p","--public", type=str, help="Public key")
    parser.add_argument("-d","--private", type=str, help="Private key")
    parser.add_argument("-c", "--ciphertext", type=int, help="Ciphertext")
    parser.add_argument("--plain", type=str, help="Text to encrypt")
    args = parser.parse_args()
    if args.mode == "encrypt":
        if not args.plain:
            raise ValueError("You must provide a text to encrypt")
        if not args.public:
            public, private = generate_keypair(args.bits)
            text = args.plain.encode()
            if int.from_bytes(text, "big") > public[0]:
                raise ValueError("Plaintext too long")
            cyphertext = pow(int.from_bytes(text, "big"), public[1], public[0])
            print("Public key:", public)
            print("Private key:", private)
            print("Cyphertext:", cyphertext)
        else:
            public = tuple(map(int, args.public.replace('(','').replace(')','').split(",")))
            text = args.plain.encode()
            if int.from_bytes(text, "big") > public[0]:
                raise ValueError("Plaintext too long")
            cyphertext = pow(int.from_bytes(text, "big"), public[1], public[0])
            print("Cyphertext:", cyphertext)

    elif args.mode == "decrypt":
        if not args.private:
            raise ValueError("You must provide a private key")
        if not args.ciphertext:
            raise ValueError("You must provide a ciphertext")
        private = tuple(map(int, args.private.replace('(','').replace(')','').split(",")))
        plaintext = pow(args.ciphertext, private[1], private[0])
        print("Plaintext:", plaintext.to_bytes((plaintext.bit_length() + 7) // 8, "big"))
        
    elif args.mode == "break":
        public = tuple(map(int, args.public.replace('(','').replace(')','').split(",")))
        factors = rsa_break(public[0])
        print("Private key:", public[0], modinv(public[1],(factors[0]-1) * (factors[1]-1)))
        if args.ciphertext:
            plaintext = decrypt_with_known_factors(args.ciphertext, public, factors)
            print("Plaintext:", plaintext.to_bytes((plaintext.bit_length() + 7) // 8, "big"))
            
    elif args.mode == "demo":
        public, private = generate_keypair(48)
        text = b"Hello bob!"
        print("Plaintext:", text)
        print("Public key:", public)
        print("Private key:", private)
        if int.from_bytes(text, "big") > public[0]:
            raise ValueError("Plaintext too long")
        cyphertext = pow(int.from_bytes(text, "big"), public[1], public[0])
        print("Cyphertext:", cyphertext)
        plaintext = pow(cyphertext, private[1], private[0])
        print("Plaintext recovered :", plaintext.to_bytes((plaintext.bit_length() + 7) // 8, "big"))
        factors = rsa_break(public[0])
        print("Private key breaked:", public[0], modinv(public[1],(factors[0]-1) * (factors[1]-1)))
        plaintext = decrypt_with_known_factors(cyphertext, public, factors)
        print("Plaintext breaked:", plaintext.to_bytes((plaintext.bit_length() + 7) // 8, "big"))
    else:
        print("You must provide a mode")
        
    



# factor find with rho_pollard
# plaindecrypt = decrypt_with_known_factors(618641947730401572003416228772502808, (2614864743974603474046080737080411737, 65537), (584535046023135133, 4473409698468465389))

# print(plaindecrypt.to_bytes((plaindecrypt.bit_length() + 7) // 8, "big"))
