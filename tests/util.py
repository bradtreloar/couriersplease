
import unittest

from couriersplease.util import condense_address



class UtilTestCase(unittest.TestCase):


    def test_condense(self):
        addresses = [
            (
                "123 Easy Street",
                "123 EASY STREET"
            ),
            (
                "UNIT 99, 125 Reallylongname Beach Boulevard",
                "UNIT 99, 125 REALLYLONGNAME BEACH BOULEVARD"
            ),
            (
                "Level 99, 125 Reallylongname Beach Boulevard",
                "LEVEL 99, 125 REALLYLONGNAME BEACH BOULEVARD"
            ),
            (
                "Level 99, John Smith Building, 125 Reallylongname Beach Boulevard",
                "LVL99 125 REALLYLONGNAME BCH BLVD"
            ),
            (
                "Level 99, John Smith Building, 125 Reallylongname Beach Boulevard (deliveries via Thatother Reallylongname Avenue)",
                "LVL99 125 REALLYLONGNAME BCH BLVD"
            ),
        ]

        for addr in addresses:
            input = addr[0]
            expected_result = addr[1]
            result = condense_address(input, [15, 15, 15])
            self.assertEqual(result, expected_result)



if __name__ == '__main__':
    unittest.main()
    