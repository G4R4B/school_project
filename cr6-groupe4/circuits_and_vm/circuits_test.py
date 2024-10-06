import unittest
from circuits import min_n


def value_to_8_bits(value):
    assert 0 <= value and value < 256

    bits = [int(i) for i in bin(value)[2:]]

    return [0] * (8 - len(bits)) + bits


def bits_to_value(bits):
    value = 0
    for bit in bits:
        value = value * 2 + bit

    return value


class TestGraph(unittest.TestCase):

    def test_to_bits(self):
        self.assertEqual([0] * 8, value_to_8_bits(0))
        self.assertEqual([0] * 7 + [1], value_to_8_bits(1))
        self.assertEqual([1, 1, 1, 0, 1, 0, 0, 1], value_to_8_bits(233))
        self.assertEqual([1] * 8, value_to_8_bits(255))

    def test_from_bits(self):
        for k in range(255):
            self.assertEqual(bits_to_value(value_to_8_bits(k)), k)

    def test_min_8(self):

        for a_value in range(256):
            for b_value in range(256):
                min_value = min(a_value, b_value)

                bits_a = value_to_8_bits(a_value)
                bits_b = value_to_8_bits(b_value)

                result = min_n(bits_a, bits_b)
                self.assertEqual(min_value, bits_to_value(result))


if __name__ == "__main__":
    unittest.main()
