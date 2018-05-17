
import unittest

from couriersplease.util import Address



class UtilTestCase(unittest.TestCase):


    def test_split_into_fields(self):
        tests = [
            (
                "UNIT 99 125 REALLYLONGNAME BEACH BOULEVARD",
                ["UNIT 99 125", "REALLYLONGNAME", "BEACH BOULEVARD"],
            )
        ]

        for addr in tests:
            input = addr[0]
            expected_result = addr[1]
            result = Address.split_into_fields(input, [15, 15, 15])
            self.assertEqual(result, expected_result)


    def test_compress(self):
        tests = [
            (
                ["Level 99, John Smith Building", "125 Reallylongname Beach Boulevard"],
                ["LVL99 125", "REALLYLONGNAME", "BCH BLVD"],
            )
        ]

        for addr in tests:
            input = addr[0]
            expected_result = addr[1]
            result = Address.compress(input, [15, 15, 15])
            self.assertEqual(result, expected_result)



if __name__ == '__main__':
    unittest.main()
    