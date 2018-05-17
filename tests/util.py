
import unittest

from couriersplease.util import condense_address



class UtilTestCase(unittest.TestCase):


    def test_condense(self):
        addresses = [
            "123 Easy Street",
            "U 99, 125 Reallylongname Beach Boulevard",
            "Unit 99, 125 Reallylongname Beach Boulevard",
            "Level 99, John Smith Building, 125 Reallylongname Beach Boulevard",
            "Level 99, John Smith Building, 125 Reallylongname Beach Boulevard (deliveries via Thatother Reallylongname Avenue)",
            "Level 99, John Smith Building, 125 O'Sullivan Beach Boulevard   (deliveries via Thatother Reallylongname Avenue)",
        ]

        print()

        for addr_string in addresses:
            cond_addr_string = condense_address(addr_string, [19, 19, 19])
            print(str(len(addr_string)), '=>', str(len(cond_addr_string)))
            print(addr_string, '=>', cond_addr_string)

        print()



if __name__ == '__main__':
    unittest.main()
    