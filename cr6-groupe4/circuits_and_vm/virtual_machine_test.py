import unittest
import virtual_machine
from circuits import create_min_n
import time

def value_to_8_bits(value):
    assert 0 <= value and value < 256

    bits = [int(i) for i in bin(value)[2:]]

    return [0] * (8 - len(bits)) + bits


def bits_to_value(bits):
    value = 0
    for bit in bits:
        value = value * 2 + bit

    return value

def temps_prevu(number_for_the_moment, total_number, time_start):
    return total_number / number_for_the_moment * (time.time() - time_start)


class TestVirtualMachine(unittest.TestCase):
    def test_virtual_machine(self):
        vm = virtual_machine.VirtualMachine()

        graph = create_min_n(8)[0]
        time_start = time.time()
        for a_value in range(255):
            print("Dure depuis :","{:.2f}".format(time.time() - time_start), "temps prévu : ", "{:.2f}".format(temps_prevu(a_value + 1, 255, time_start)), end="\r")
            for b_value in range(255):
                min_value = min(a_value, b_value)

                bits_a = value_to_8_bits(a_value)
                bits_b = value_to_8_bits(b_value)

                result = vm.test(bits_a, bits_b, 8, graph)
                result_a = result[0]
                result_b = result[1]
                self.assertEqual(
                    min_value,
                    bits_to_value(result_a),
                    f"A={a_value} [{bits_a}] | B={b_value} [{bits_b}] | RES={result} | EXPT={min_value}",
                )
                self.assertEqual(
                    result_a,
                    result_b,
                    f"A={a_value} [{bits_a}] | B={b_value} [{bits_b}] | RES={result} | EXPT={min_value}",
                )


if __name__ == "__main__":
    unittest.main()
