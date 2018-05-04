
import json
import re
from datetime import datetime

from couriersplease.validate import Validator



class EntityBase:
    'Base for API entities'


    def get_dict(self, omitted_keys=[]):
        'convert Entity to dict for conversion to JSON'
        entity_dict = dict()
        for key, value in vars(self).items():
            if key == 'items':
                entity_dict['items'] = list()
                for item in value:
                    entity_dict['items'].append(item.get_dict())
            elif key not in ('url', 'name', 'verb') and key not in omitted_keys:
                entity_dict[to_camel_case(key)] = value
        return entity_dict



class DomesticItem(EntityBase):
    'Couriers Please Domestic Item'

    def __init__(self, item_data):
        EntityBase.__init__(self)
        self.quantity = item_data['quantity']
        self.length = item_data['length']
        self.height = item_data['height']
        self.width = item_data['width']
        self.physical_weight = item_data['physical_weight']


    def validate(self):
        'validate the entity attributes'
        v = Validator(self)
        v.look_at('quantity').required().integer()
        v.look_at('length').required().integer()
        v.look_at('height').required().integer()
        v.look_at('width').required().integer()
        v.look_at('physical_weight').required().decimal()
        return v


    
class DomesticPickup(EntityBase):
    'Couriers Please Domestic Pickup'


    def __init__(self, shipments):
        EntityBase.__init__(self)
        self.when = datetime.today() # @todo

        # set pickup address
        self.address1 = shipments[0].pickup_address1
        self.address2 = shipments[0].pickup_address2
        self.address3 = None
        # API docs: "address4: if a company, enter the name of the contact person"
        self.address4 = shipments[0].pickup_first_name + ' ' + shipments[0].pickup_last_name
        # API docs: "address5: Enter a pickup phone number"
        self.address5 = shipments[0].pickup_phone
        self.suburb   = shipments[0].pickup_suburb
        self.postcode = shipments[0].pickup_postcode
        self.email = shipments[0].pickup_email
        self.customer_name = shipments[0].pickup_company_name

        # set destination address
        if len(shipments) > 1:
            # API docs: "destinationAddress1: Enter consignment count"
            self.destination_address1 = str(len(shipments)) + ' consignments'
        elif len(shipments) > 0:
            self.destination_address1 = shipments[0].destination_address1
            self.destination_address2 = shipments[0].destination_address2
            self.destination_address3 = None
            self.destination_address4 = None
            self.destination_address5 = None
            self.destination_suburb   = shipments[0].destination_suburb
            self.destination_postcode = shipments[0].destination_postcode
        
        # API docs: "destinationAddress3: Enter number of items and total weight"
        item_count = 0
        total_weight = 0.00
        for shipment in shipments:
            item_count += len(shipment.items)
            for item in shipment.items:
                total_weight += item.physical_weight
        if item_count > 0:
            self.destination_address3 = str(item_count) + ' items, ' + str(total_weight) + 'kg'


    def get_dict(self):
        entity_dict = EntityBase.get_dict(self)
        'format date as string'
        entity_dict['when'] = self.when.strftime('%Y-%m-%d %I:%I %p')
        return entity_dict


    def validate(self):
        'validate the entity attributes'
        v = Validator(self)
        v.look_at('when').required().date()
        v.look_at('address1').required().string(maxlength=20)
        v.look_at('address2').string(maxlength=20)
        v.look_at('address3').string(maxlength=20)
        v.look_at('address4').string(maxlength=20)
        v.look_at('address5').string(maxlength=20)
        v.look_at('suburb').required().string()
        v.look_at('postcode').required().string(length=4)
        v.look_at('email').required().email()
        v.look_at('customer_name').required().string(maxlength=50)
        v.look_at('destination_address1').required().string(maxlength=20)
        v.look_at('destination_address2').string(maxlength=20)
        v.look_at('destination_address3').string(maxlength=20)
        v.look_at('destination_address4').string(maxlength=20)
        v.look_at('destination_address5').string(maxlength=20)
        v.look_at('destination_suburb').string()
        v.look_at('destination_postcode').string(length=4)
        return v



class DomesticQuote(EntityBase):
    'Couriers Please Domestic Quote'


    def __init__(self, location_from, location_to, items):
        EntityBase.__init__(self)
        if not location_from.pickup:
            raise NotPickupLocationError('location_from.pickup must be True')
        self.from_suburb = location_from.suburb
        self.from_postcode = location_from.postcode
        self.to_suburb = location_to.suburb
        self.to_postcode = location_to.postcode
        self.items = items
        self.rates = list()


    def validate(self):
        'validate the entity attributes'
        v = Validator(self)
        v.look_at('from_suburb').required().string()
        v.look_at('from_postcode').required().string()
        v.look_at('to_suburb').required().string()
        v.look_at('to_postcode').required().string()
        v.look_at('items').required().items()
        return v



class DomesticShipment(EntityBase):
    'Couriers Please Domestic Shipment'


    def __init__(self):
        EntityBase.__init__(self)
        # pickup address
        self.pickup_first_name = None
        self.pickup_last_name = None
        self.pickup_company_name = None
        self.pickup_email = None
        self.pickup_address1 = None
        self.pickup_address2 = None
        self.pickup_suburb = None
        self.pickup_state = None
        self.pickup_postcode = None
        self.pickup_phone = None
        self.pickup_is_business = None
        # destination address
        self.destination_first_name = None
        self.destination_last_name = None
        self.destination_company_name = None
        self.destination_email = None
        self.destination_address1 = None
        self.destination_address2 = None
        self.destination_suburb = None
        self.destination_state = None
        self.destination_postcode = None
        self.destination_phone = None
        self.destination_is_business = None
        # contact address
        self.contact_first_name = None
        self.contact_last_name = None
        self.contact_company_name = None
        self.contact_email = None
        self.contact_address1 = None
        self.contact_address2 = None
        self.contact_suburb = None
        self.contact_state = None
        self.contact_postcode = None
        self.contact_phone = None
        self.contact_is_business = None
        # other fields
        self.special_instruction = None
        self.reference_number = None
        self.terms_accepted = None
        self.dangerous_goods = None
        self.rate_card_id = None
        self.items = list()
        # tracking
        self.consignment_code = None


    def get_dict(self):
        'omit tracking info from entity dict'
        return EntityBase.get_dict(self, omitted_keys=[
            'consignment_code', 'consignment_info'
        ])


    def setAddress(self, type, address):
        for key, value in address.items():
            name = type + '_' + key
            if hasattr(self, name):
                setattr(self, name, value)
            else:
                raise Exception('Invalid property: ' + name)


    def validate(self):
        'validate the entity attributes'
        v = Validator(self)
        v.look_at('pickup_first_name').required().string(maxlength=50)
        v.look_at('pickup_last_name').required().string(maxlength=50)
        v.look_at('pickup_company_name').string(maxlength=50)
        # @todo pickup_company_name is required if pickup_is_business is True
        v.look_at('pickup_email').required().email()
        v.look_at('pickup_address1').required().string(maxlength=100)
        v.look_at('pickup_address2').string(maxlength=100)
        v.look_at('pickup_suburb').required().suburb()
        v.look_at('pickup_state').required().state()
        v.look_at('pickup_postcode').required().postcode()
        v.look_at('pickup_phone').required().phone()
        v.look_at('pickup_is_business').required().boolean()
        v.look_at('destination_first_name').required().string(maxlength=50)
        v.look_at('destination_last_name').required().string(maxlength=50)
        v.look_at('destination_company_name').string(maxlength=50)
        # @todo pickup_company_name is required if destination_is_business is True
        v.look_at('destination_email').required().email()
        v.look_at('destination_address1').required().string(maxlength=100)
        v.look_at('destination_address2').string(maxlength=100)
        v.look_at('destination_suburb').required().suburb()
        v.look_at('destination_state').required().state()
        v.look_at('destination_postcode').required().postcode()
        v.look_at('destination_phone').required().phone()
        v.look_at('destination_is_business').required().boolean()
        v.look_at('contact_first_name').required().string(maxlength=50)
        v.look_at('contact_last_name').required().string(maxlength=50)
        v.look_at('contact_company_name').string(maxlength=50)
        # @todo contact_company_name is required if contact_is_business is True
        v.look_at('contact_email').required().email()
        v.look_at('contact_address1').required().string(maxlength=100)
        v.look_at('contact_address2').string(maxlength=100)
        v.look_at('contact_suburb').required().suburb()
        v.look_at('contact_state').required().state()
        v.look_at('contact_postcode').required().postcode()
        v.look_at('contact_phone').required().phone()
        v.look_at('contact_is_business').required().boolean()
        v.look_at('special_instruction').string(maxlength=140)
        v.look_at('reference_number').string(maxlength=40)
        v.look_at('terms_accepted').required().boolean(True)
        v.look_at('dangerous_goods').required().boolean(False)
        v.look_at('rate_card_id').string(length=3)
        v.look_at('items').required().items()
        return v



class Location(EntityBase):
    'Couriers Please Location Entity'


    def __init__(self, data):
        EntityBase.__init__(self)
        self.postcode = data['Postcode']
        self.state = data['State']
        self.suburb = data['Suburb']
        self.pickup = data['PickUpFlag'] == 'Y'



def to_camel_case(name):
    'convert key to camelCase'
    components = name.split('_')
    return components[0] + "".join(x.title() for x in components[1:])



class NotPickupLocationError(Exception):
    pass