
import unittest

from tests.entity import EntityTestCase
from couriersplease.entity import DomesticItem, DomesticQuote



class ValidatorTestCase(EntityTestCase):


    def test_validate_domestic_quote(self):
        quote = self.dummy_domestic_quote()
        validator = quote.validate()
        self.assertEqual({}, validator.errors)

        # remove item quantity
        quote = self.dummy_domestic_quote()
        quote.items[0].quantity = None
        validator = quote.validate()
        self.assertEqual({
            'items': ['item 1, quantity: required'],
        }, validator.errors)

        # remove items altogether
        quote.items = None
        validator = quote.validate()
        self.assertEqual({
            'items': ['required'],
        }, validator.errors)


        # remove postcode
        quote = self.dummy_domestic_quote()
        quote.from_postcode = None
        validator = quote.validate()
        self.assertEqual({
            'from_postcode': ['required'],
        }, validator.errors)


    def test_validate_domestic_item(self):
        item = self.dummy_domestic_item()
        validator = item.validate()
        self.assertEqual({}, validator.errors)

        # remove quantity
        item = self.dummy_domestic_item()
        item.quantity = None
        validator = item.validate()
        self.assertEqual({
            'quantity': ['required'],
        }, validator.errors)



if __name__ == '__main__':
    unittest.main()
    