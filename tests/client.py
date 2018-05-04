
import unittest
import yaml

from tests.entity import EntityTestCase
from couriersplease.client import Client, DataValidationError



class ClientTestCase(EntityTestCase):


    def setUp(self):
        with open('settings.yml', 'r') as stream:
            settings = yaml.load(stream)
        self.client = Client(settings)
        # use sandbox API
        self.client.base_url = 'https://api-test.couriersplease.com.au/v1/'


    def test_book_domestic_pickup(self):
        shipment = self.dummy_domestic_shipment()
        shipments = [ shipment ]
        try:
            job_number = self.client.book_domestic_pickup(shipments)
            self.assertIsInstance(job_number, str)
        except DataValidationError as ex:
            print(ex.errors)


    def test_create_domestic_shipment(self):
        shipment = self.dummy_domestic_shipment()
        consignment_code = self.client.create_domestic_shipment(shipment)
        self.assertIsInstance(consignment_code, str)
        self.assertIsInstance(shipment.consignment_code, str)


    def test_get_domestic_label(self):
        shipment = self.dummy_domestic_shipment()
        self.client.create_domestic_shipment(shipment)
        label = self.client.get_domestic_label(shipment)
        self.assertIsInstance(label, str)


    def test_get_domestic_quote(self):
        # test with a valid shipment
        shipment = self.dummy_domestic_shipment()
        self.client.create_domestic_shipment(shipment)
        quote = self.client.get_domestic_quote(shipment)
        self.assertTrue(len(quote.rates) > 0, 'API call returned no results')
        for rate in quote.rates:
            for key in ['CalculatedFreightCharge', 'Weight']:
                self.assertIn(key, rate.keys())

        # test again without required field
        shipment.pickup_postcode = None
        try:
            quote = self.client.get_domestic_quote(shipment)
        except DataValidationError as ex:
            self.assertEqual([{
                'type': 'Required Field', 
                'field': 'fromPostcode', 
                'description': 'Please select From Postcode.'
            }], ex.errors)


    def test_get_location_suggestions(self):
        # test with valid input
        for query in ['5160', 'Adel']:
            suggestions = self.client.get_location_suggestions(query)
            for suggestion in suggestions:
                for key in ['Postcode', 'Suburb', 'State']:
                    self.assertIn(key, suggestion.keys())

        # test with invalid inputs
        for query in ['500000', 'Foo Bar Qux']:
            suggestions = self.client.get_location_suggestions(query)
            self.assertTrue(len(suggestions) == 0, 'Expected no suggestions for fake suburb')


    def test_validate_domestic_shipment(self):
        # test against valid shipment
        shipment = self.dummy_domestic_shipment()
        is_valid = self.client.validate_domestic_shipment(shipment)
        self.assertTrue(is_valid)

        # test again without required field
        shipment.pickup_postcode = None
        try:
            self.client.validate_domestic_shipment(shipment)
        except DataValidationError as ex:
            self.assertEqual([{
                'type': 'Required Field', 
                'field': 'pickupPostcode', 
                'description': 'Please enter value pickup postcode.'
            }], ex.errors)

    
    def test_locate_domestic_shipment(self):
        shipment = self.dummy_domestic_shipment()
        self.client.create_domestic_shipment(shipment)
        consignment_info = self.client.locate_domestic_shipment(shipment)
        for consignment in consignment_info:
            self.assertIn('itemsCoupons', consignment.keys())



if __name__ == '__main__':
    unittest.main()
    