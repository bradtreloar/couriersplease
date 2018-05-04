
import unittest

from couriersplease.entity import DomesticItem, DomesticQuote, DomesticShipment, Location



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
        item = DomesticItem()
        item.quantity = 5
        item.length = 40
        item.height = 60
        item.width = 30
        item.physical_weight = 0.05
        return item


    def dummy_domestic_shipment(self):
        shipment = DomesticShipment()
        # set addresses
        pickup_address = {
            'first_name': 'Brad',
            'last_name': 'Treloar',
            'company_name': 'Allbiz Supplies',
            'email': 'brad@allbizsupplies.biz',
            'address1': "125 O'Sullivan Beach Road",
            'address2': '',
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
        shipment.setAddress('pickup', pickup_address)
        shipment.setAddress('destination', destination_address)
        shipment.setAddress('contact', destination_address)
        # set other fields
        shipment.special_instruction = 'Leave on front porch'
        shipment.reference_number = 'TEST_DUMMY'
        shipment.terms_accepted = True
        shipment.dangerous_goods = False
        shipment.rate_card_id = 'L55'
        # add item
        shipment.items.append(self.dummy_domestic_item())

        return shipment


    def dummy_location(self):
        return Location({
            'Postcode': '5173',
            'State': 'SA',
            'Suburb': 'ALDINGA BEACH',
            'PickUpFlag': 'Y',
        })



if __name__ == '__main__':
    unittest.main()
    