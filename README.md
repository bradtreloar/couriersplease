# CouriersPlease API Python library

## Introduction

This is a Python library to help developers integrate with the CouriersPlease API.

API docs: https://apidev.couriersplease.com.au/documentation/

## Usage

This library provides a Client class that handles communication with
the CouriersPlease server.

#### Instantiate the Client

Your will need an auth token in order to consume the API:
API tokens page: https://apidev.couriersplease.com.au/#/tokens

```python
from couriersplease.client import Client

# instantiate a production client using
# your Developer ID (e.g. 123456789) and
# your Production API Token, created through the Developer portal
client = Client({
    'user': '123456789' # ID
    'pass': 'DFFAF46F0799FD174EC1AC253011D990C1ADA2AEDBCBA27E4AF48B7F3FD87918' # token
})

# instantiate a sandbox client for development using
# your Developer ID (e.g. 123456789)
# Your Sandbox API Token, created through the Developer portal
client = Client({
    'user': '123456789' 
    'pass': 'DFFAF46F0799FD174EC1AC253011D990C1ADA2AEDBCBA27E4AF48B7F3FD87918' # token
}, sandbox=True)
```

#### Get Location Suggestions from Locations API

Before requesting a quote or creating a consignment, a valid suburb/postcode set should be
fetched from the Locations API.

The client returns a list of Location objects, each with the following properties:
- postcode
- state
- suburb (in all caps)
- pickup (True if CouriersPlease can pickup from this suburb)

If no valid locations match the search then the client returns an empty list

```python
# the Locations API takes a postcode or (partial) suburb name as argument
postcode_or_suburb_name = 'Adelaide'
locations = client.get_locations(postcode_or_suburb_name)
```

#### Build list of items to be delivered

In order to get a quote or create a consignment, CouriersPlease requires a
list of items. This library provides a DomesticItem class for items.

```python
from couriersplease.entity import DomesticItem

items = list()
item = DomesticItem({
    'quantity': 5
    'length': 40 # cm
    'height': 60 # cm
    'width': 30 # cm
    'physical_weight': 0.05 # kg
})
items.append(item)
```

#### Get Domestic Rates from Quote API

Client.get_domestic_quote returns a DomesticQuote object. DomesticQuote.rates is
a list of rates returned by the API.

Each rate is a DomesticRate object which contains the following properties:
- code (rate card code)
- description (rate card description)
- freight_charge (excluding GST)
- fuel_surcharge (excluding GST)
- total_charge (freight_charge + fuel_surcharge)
- eta
- pickup_cutoff_time
- weight (greater of the physical weight or the volumetric weight)

```python
# instantiate a quote object from two Location objects
# and a list of DomesticItem objects
# from_location must be a pickup address
quote = client.get_domestic_quote(from_location, to_location, items)
rates = quote.rates
```

#### Create Domestic Shipment (Consignment) using Shipment API

DomesticShipment requires three addresses:
- pickup_address
- destination_address
- contact_address (the contact details for the recipient)

```python
example_address = {
    'first_name': 'Brad',
    'last_name': 'Treloar',
    'company_name': 'Treloar Digital', # required only if is_business is True
    'email': 'brad@treloardigital.com.au',
    'address1': '1001 Imaginary Street',
    'address2': '',
    'suburb': 'IMAGINARYVILLE', # Valid suburb name from Location API
    'state': 'ZZZ', # Valid state code from Location API
    'postcode': '9999', # Valid postcode from Location API
    'phone': '0412 345 678', # spaces and numbers only, plus optional '+'
    'is_business': True, 
}
```

A DomesticShipment object must be created and then passed to the Client to create the shipment.

The DomesticShipment should be validated using the Shipment API before it is created.

```python
shipment = DomesticShipment({
    'pickup_address': {...}, # see example_address above for required dict structure
    'destination_address': {...},
    'contact_address': {...}, 
    'special_instruction': 'Leave on front porch', # extra instructions for the courier
    'reference_number': 'EXAMPLE', # the sender's reference number
    'terms_accepted': True, # Must accept Terms and Conditions
    'dangerous_goods': False, # Must be False; dangerous goods shipments are not handled by the API
    'rate_card_id': 'L55', # code from DomesticRate object retrieved from Quote API
    'items': [...], # list of DomesticItem objects
})

# check that the shipment is valid
is_valid = client.validate_domestic_shipment(shipment)

# create the consignment
if is_valid:
    consignment_code = client.create_domestic_shipment(shipment)
```

