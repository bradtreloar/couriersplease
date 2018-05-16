
import unittest

from couriersplease.util import condense_address



class UtilTestCase(unittest.TestCase):


    def test_condense(self):
        addresses = [
            "U99, 125 O'Sullivan Beach Road",
            "Unit 99, 125 O'Sullivan Beach Road",
            "Level 99, Barr Smith Building, 125 O'Sullivan Beach Road",
        ]

        print()

        for addr_string in addresses:
            cond_addr_string = condense_address(addr_string, 28)
            print(str(len(addr_string)), '=>', str(len(cond_addr_string)))
            print(addr_string, '=>', cond_addr_string)

        print()



if __name__ == '__main__':
    unittest.main()
    