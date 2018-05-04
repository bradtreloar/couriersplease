
import requests

from couriersplease.entity import DomesticItem, DomesticPickup, DomesticQuote, DomesticRate, DomesticShipment, Location


class Client:
    'HTTP request client for CP API'


    def __init__(self, auth, sandbox=False):
        # save auth as tuple
        self.auth = (
            auth['user'],
            auth['pass']
        )
        self.headers = {
            'Accept': 'application/json',
        }
        if sandbox:
            self.base_url = 'https://api-test.couriersplease.com.au/v1/'
        else:
            self.base_url = 'https://api.couriersplease.com.au/v1/'


    def request(self, verb, path, data):
        'send HTTP request and return HTTP response'
        url = self.base_url + path
        if verb == 'GET':
            return requests.get(url,
                auth=self.auth,
                headers=self.headers,
                params=data
            )
        elif verb == 'POST':
            return requests.post(url,
                auth=self.auth,
                headers=self.headers,
                json=data
            )


    def book_domestic_pickup(self, shipment):
        # prepare pickup object from shipment
        pickup = DomesticPickup(shipment)
        response = self.request('POST', 'domestic/bookPickup', pickup.get_dict())
        body = response.json()
        if body['responseCode'] == 'SUCCESS':
            return body['data']['jobNumber']
        else:
            self.handle_unsuccessful_request(response)


    def create_domestic_shipment(self, shipment):
        response = self.request('POST', 'domestic/shipment/create', shipment.get_dict())
        body = response.json()
        if body['responseCode'] == 'SUCCESS':
            shipment.consignment_code = body['data']['consignmentCode']
            return body['data']['consignmentCode']
        else:
            self.handle_unsuccessful_request(response)


    def handle_unsuccessful_request(self, response):
        body = response.json()
        if body['responseCode'] == 'INVALID_INPUT':
            raise DataValidationError(
                body['msg'],
                body['data']['errors']
            )
        elif body['responseCode'] == 'UNAUTHORIZED':
            raise AuthenticationError(body['msg'])
        elif body['responseCode'] == 'SERVICE_UNAVAILABLE':
            raise ServiceUnavailableError('Service unavailable')


    def get_domestic_label(self, shipment):
        if shipment.consignment_code == None:
            raise ValueError
        # call the API and get the json response
        response = self.request('GET', 'domestic/shipment/label', {
            'consignmentNumber': shipment.consignment_code
        })
        body = response.json()
        if body['responseCode'] == 'SUCCESS':
            return body['data']['label']
        else:
            self.handle_unsuccessful_request(response)


    def get_domestic_quote(self, location_from, location_to, items):
        quote = DomesticQuote(location_from, location_to, items)
        # call the API and get the json response
        response = self.request('POST', 'domestic/quote', quote.get_dict())
        body = response.json()
        if body['responseCode'] == 'SUCCESS':
            for rate_data in body['data']:
                rate = DomesticRate(rate_data)
                quote.rates.append(rate)
            return quote
        else:
            self.handle_unsuccessful_request(response)


    def get_locations(self, location):
        response = self.request('GET', 'locations', {
            'suburbOrPostcode': location
        })
        body = response.json()
        if body['responseCode'] == 'SUCCESS':
            locations = list()
            for location_data in body['data']:
                location = Location(location_data)
                locations.append(location)
            return locations
        else:
            self.handle_unsuccessful_request(response)


    def locate_domestic_shipment(self, shipment):
        response = self.request('GET', 'domestic/locateParcel', {
            'trackingCode': shipment.consignment_code
        })
        body = response.json()
        if body['responseCode'] == 'SUCCESS':
            shipment.consignment_info = body['data']['consignmentInfo']
            return body['data']['consignmentInfo']
        else:
            self.handle_unsuccessful_request(response)


    def validate_domestic_shipment(self, shipment):
        response = self.request('POST', 'domestic/shipment/validate', shipment.get_dict())
        body = response.json()
        if body['responseCode'] == 'SUCCESS':
            return True
        else:
            self.handle_unsuccessful_request(response)



class AuthenticationError(Exception):
    pass
    


class DataValidationError(Exception):

    def __init__(self, message, errors):
        self.message = message
        self.errors = errors

    def __str__(self):
        return self.message



class ServiceUnavailableError(Exception):
    pass
