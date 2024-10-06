"""
Unit tests for the ot_rsa.py module.

Author: Tony Ly SOAN
"""
import unittest
import ot_rsa
import random

class TestOtRsa(unittest.TestCase):
    def test_ot_rsa_0(self):
        for _ in range(100):
            m0 = random.randint(0, 2**16)
            m1 = random.randint(0, 2**16)

            alice = ot_rsa.Alice()
            bob = ot_rsa.Bob()

            alice_public_tuple = alice.to_bob1(m0, m1)

            bob_bit_choice = 0

            bob_v = bob.to_alice1(alice_public_tuple, bob_bit_choice)
            alice_encrypted_msgs = alice.to_bob2(bob_v)
            bob_decrypted_msg = bob.to_alice2(alice_encrypted_msgs[0], alice_encrypted_msgs[1])

            self.assertEqual(m0, bob_decrypted_msg)
            self.assertNotEqual(m1, bob_decrypted_msg)
    
    def test_ot_rsa_1(self):
        for _ in range(100):
            m0 = random.randint(0, 2**16)
            m1 = random.randint(0, 2**16)

            alice = ot_rsa.Alice()
            bob = ot_rsa.Bob()

            alice_public_tuple = alice.to_bob1(m0, m1)

            bob_bit_choice = 1

            bob_v = bob.to_alice1(alice_public_tuple, bob_bit_choice)
            alice_encrypted_msgs = alice.to_bob2(bob_v)
            bob_decrypted_msg = bob.to_alice2(alice_encrypted_msgs[0], alice_encrypted_msgs[1])

            self.assertNotEqual(m0, bob_decrypted_msg)
            self.assertEqual(m1, bob_decrypted_msg)

if __name__ == "__main__":
    unittest.main()