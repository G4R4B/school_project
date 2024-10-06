"""
This module implements the RSA Oblivious Transfer Protocol. 
(https://en.wikipedia.org/wiki/Oblivious_transfer#1%E2%80%932_oblivious_transfer)

Author: Tony Ly Soan
"""

from __future__ import annotations
import sys
sys.path.append('../rsa/')
import rsa
import random

# Helper functions


def pick_random_zn(n: int):
    """
    Pick an integer in `Z_n`.

    Parameters:
        `n` (int): The upper bound (excluded) of the range.

    Returns:
        A random integer in the range `[0, n-1]`.
    """
    return random.randint(0, n - 1)


def pick_random_bit():
    """
    Pick a randomly generated bit (0 or 1).

    Returns:
        A randomly generated bit (0 or 1).
    """
    return random.randint(0, 1)


class Alice:
    """Class representing Alice in RSA Oblivious Transfer Protocol"""

    def __init__(self) -> None:
        pass

    def to_bob1(self, m0: int, m1: int):
        """
        First step of the RSA OT protocol.
        Calculates the values to be sent to Bob based on the messages `m0` and `m1` we want to send.

        Parameters:
            `m0` : The first message to be sent to Bob.
            `m1` : The second message to be sent to Bob.

        Returns:
            The tuple `(N, E, X0, X1)` to be sent to Bob.
            `N` : The RSA modulus.
            `E` : The RSA public exponent.
            `X0` : A random value in Z_N.
            `X1` : A random value in Z_N.
        """
        self.__M0 = m0
        self.__M1 = m1

        (self.N, self.E), (_, self.__D) = rsa.generate_keypair(512)

        self.X0 = pick_random_zn(self.N)
        self.X1 = pick_random_zn(self.N)

        return (self.N, self.E, self.X0, self.X1)

    def to_bob2(self, v: int):
        """
        Third step of the RSA OT protocol.
        Calculates the encrypted messages to be sent to Bob based on the value `v` received from Bob.

        Parameters:
            `v` : Bob's bit choice, which is blinded to Alice.

        Returns:
            The tuple `(M0_, M1_)` containing the encrypted messages to be sent to Bob.
        """

        self.__KO = pow(v - self.X0, self.__D, self.N)
        self.__K1 = pow(v - self.X1, self.__D, self.N)

        self.M0_ = (self.__M0 + self.__KO) % self.N
        self.M1_ = (self.__M1 + self.__K1) % self.N

        return (self.M0_, self.M1_)


class Bob:
    """Class representing Bob in RSA Oblivious Transfer Protocol"""

    def __init__(self) -> None:
        pass

    def to_alice1(self, alice_public_tuple, b: int):
        """
        Second step of the RSA OT protocol.
        Calculates the encrypted value to be sent to Alice based on the tuple received from Alice.

        Parameters:
            `alice_public_tuple1` : The tuple containing the parameters `(N, E, X0, X1)` of Alice.
            `b` : The chosen bit indicating which message to get (0 or 1).

        Returns:
            The value `v` to be sent to Alice.
            `v` : Bob's encrypted message choice.
        """
        assert b == 0 or b == 1

        self.N, self.E, self.X0, self.X1 = alice_public_tuple
        self.__B = b
        self.__K = pick_random_zn(self.N)

        if self.__B == 0:
            return (self.X0 + pow(self.__K, self.E, self.N)) % self.N
        else:
            return (self.X1 + pow(self.__K, self.E, self.N)) % self.N

    def to_alice2(self, M0_, M1_):
        """
        Fourth step of the RSA OT protocol.
        Decrypts the message Bob wants by using `__B`, based on the encrypted messages received from Alice.

        Parameters:
            alice_encrypted_msgs : A tuple containing the encrypted messages `(M0_, M1_)` from Alice.

        Returns:
            The decrypted message chosen.
        """

        if self.__B == 0:
            self.__M0 = (M0_ - self.__K) % self.N
            return self.__M0
        else:
            self.__M1 = (M1_ - self.__K) % self.N
            return self.__M1


# Demo
if __name__ == "__main__":
    alice_msg_1 = int.from_bytes(b"Coucou bob", "big")
    alice_msg_2 = int.from_bytes(b"Adios bob", "big")

    alice = Alice()
    bob = Bob()

    alice_public_tuple = alice.to_bob1(alice_msg_1, alice_msg_2)

    bob_random_bit = pick_random_bit()

    print(f"[DEBUG] Bob chose the bit {bob_random_bit} with message: ", end="")
    if bob_random_bit == 0:
        print(alice_msg_1.to_bytes((alice_msg_1.bit_length() + 7) // 8, "big"))
    else:
        print(alice_msg_2.to_bytes((alice_msg_2.bit_length() + 7) // 8, "big"))

    bob_v = bob.to_alice1(alice_public_tuple, bob_random_bit)
    alice_encrypted_msgs = alice.to_bob2(bob_v)
    bob_decrypted_msg = bob.to_alice2(alice_encrypted_msgs[0], alice_encrypted_msgs[1])

    print(
        f"[DEBUG] Bob received message {bob_random_bit}: ",
        bob_decrypted_msg.to_bytes((bob_decrypted_msg.bit_length() + 7) // 8, "big"),
    )
