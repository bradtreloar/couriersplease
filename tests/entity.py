
import unittest

from couriersplease.entity import DomesticItem, DomesticQuote, DomesticPickup, DomesticShipment, Location



class EntityTestCase(unittest.TestCase):


    def dummy_domestic_quote(self):
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
        return DomesticQuote(location_from, location_to, items)


    def dummy_domestic_item(self):
        return DomesticItem({
            'quantity': 5,
            'length': 40,
            'height': 60,
            'width': 30,
            'physical_weight': 0.05,
        })


    def dummy_domestic_pickup(self, shipments):
        return DomesticPickup({
            "account_name": "ALLBIZ",
            "contact_name": "Brad Treloar",
            "contact_email": "brad@allbizsupplies.biz",
        }, shipments)


    def dummy_domestic_shipment(self):
        # set addresses
        pickup_address = {
            'first_name': 'Brad',
            'last_name': 'Treloar',
            'company_name': 'Allbiz Supplies',
            'email': 'brad@allbizsupplies.biz',
            'address1': "125 O'Sullivan",
            'address2': 'Beach Road',
            'suburb': 'LONSDALE',
            'state': 'SA',
            'postcode': '5160',
            'phone': '0883262899',
            'is_business': True,
        }
        destination_address = {
            'first_name': 'Brad',
            'last_name': 'Treloar',
            'company_name': 'Treloar Digital',
            'email': 'brad@treloardigital.com.au',
            'address1': '38 Evergreen Court',
            'address2': '',
            'suburb': 'ALDINGA BEACH',
            'state': 'SA',
            'postcode': '5173',
            'phone': '0468812860',
            'is_business': False,
        }
        return DomesticShipment({
            'pickup_address': pickup_address,
            'destination_address': destination_address,
            'contact_address': destination_address,
            'special_instruction': 'Leave on porch',
            'reference_number': 'TEST_DUMMY',
            'terms_accepted': True,
            'dangerous_goods': False,
            'rate_card_id': 'L55',
            'items': [ self.dummy_domestic_item() ],
        })


    def dummy_location(self):
        return Location({
            'Postcode': '5173',
            'State': 'SA',
            'Suburb': 'ALDINGA BEACH',
            'PickUpFlag': 'Y',
        })



if __name__ == '__main__':
    unittest.main()
    