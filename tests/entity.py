
import unittest

from couriersplease.entity import DomesticItem, DomesticQuote, DomesticShipment, Location



class EntityTestCase(unittest.TestCase):


    def dummy_domestic_quote(self):
        quote = DomesticQuote()
        quote.from_suburb = 'Lonsdale'
        quote.from_postcode = '5160'
        quote.to_suburb = 'Adelaide'
        quote.to_postcode = '5000'
        quote.items = list()
        quote.items.append(self.dummy_domestic_item())
        return quote


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
            'suburb': 'Lonsdale',
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
            'suburb': 'Aldinga beach',
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


    def dummy_location(self, suburb_or_postcode='5160'):
        location = Location(suburb_or_postcode)
        return location



if __name__ == '__main__':
    unittest.main()
    