
import unittest
import yaml

from tests.entity import EntityTestCase
from couriersplease.client import Client, DataValidationError, AuthenticationError
from couriersplease.entity import Location, DomesticRate



class ClientTestCase(EntityTestCase):


    def setUp(self):
        # auth.yml must be a YAML file containing
        # two string properties: user and pass
        with open('auth.yml', 'r') as auth:
            self.client = Client(yaml.load(auth), sandbox=True)


    def test_book_domestic_pickup(self):
        shipment = self.dummy_domestic_shipment()
        self.client.create_domestic_shipment(shipment)

        # calculate weight manually instead of using the QUote API
        shipment.total_weight = 0.00
        for item in shipment.items:
            # assume physical weight is OK for this test
            shipment.total_weight += item.physical_weight
        if shipment.total_weight < 0.1:
            shipment.total_weight = 0.1
        
        pickup = self.dummy_domestic_pickup([ shipment ])
        job_number = self.client.book_domestic_pickup(pickup)
        self.assertIsInstance(job_number, str)



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
        location_from = Location({
            'Postcode': '5160',
            'State': 'SA',
            'Suburb': 'LONSDALE',
            'PickUpFlag': 'Y',
        })
        location_to = Location({
            'Postcode': '5173',
            'State': 'SA',
            'Suburb': 'ALDINGA BEACH',
            'PickUpFlag': 'Y',
        })
        items = list()
        items.append(self.dummy_domestic_item())
        quote = self.client.get_domestic_quote(location_from, location_to, items)
        self.assertTrue(len(quote.rates) > 0, 'API call returned no results')
        for rate in quote.rates:
            self.assertIsInstance(rate, DomesticRate)

        # test again without required field
        location_from.postcode = None
        try:
            self.client.get_domestic_quote(location_from, location_to, items)
            self.fail('Expected DataValidationError')
        except DataValidationError as ex:
            self.assertEqual([{
                'type': 'Required Field', 
                'field': 'fromPostcode', 
                'description': 'Please select From Postcode.'
            }], ex.errors)


    def test_get_location_suggestions(self):
        # test with valid input
        for query in ['5160', 'Adel']:
            locations = self.client.get_locations(query)
            for location in locations:
                self.assertIsInstance(location, Location)

        # test with invalid inputs
        for query in ['500000', 'Foo Bar Qux']:
            locations = self.client.get_locations(query)
            self.assertTrue(len(locations) == 0, 'Expected no suggestions for fake suburb')


    def test_validate_domestic_shipment(self):
        # test against valid shipment
        shipment = self.dummy_domestic_shipment()
        is_valid = self.client.validate_domestic_shipment(shipment)
        self.assertTrue(is_valid)

        # test again without required field
        shipment.pickup_postcode = None
        try:
            self.client.validate_domestic_shipment(shipment)
            self.fail('Expected DataValidationError')
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
    