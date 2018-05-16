
import re
from datetime import datetime

from couriersplease.enum import state_codes


class Validator:
    'Validator for API Entities'


    def __init__(self, entity):
        self.attr_name = None
        self.errors = dict()
        self.entity = entity
        self.attr = None


    def look_at(self, attr_name):
        'set the attribute to be tested'
        self.attr = getattr(self.entity, attr_name)
        self.attr_name = attr_name
        return self

    
    def mark_error(self, error_message):
        # initiatise the list of errors for this attribute
        if self.attr_name not in self.errors.keys():
            self.errors[self.attr_name] = list()
        # add error message
        # ignore other errors if required value is empty
        if 'required' not in self.errors[self.attr_name]:
            self.errors[self.attr_name].append(error_message)


    def required(self):
        'test that attr is not empty'
        if self.attr in [None, '', 0, []]:
            self.mark_error('required')
        return self

    
    def boolean(self, value=None):
        'test that attr is boolean'
        if not isinstance(self.attr, bool):
            self.mark_error('must be a boolean value')
        # validate against value if given and if attr is boolean
        if value and isinstance(self.attr, bool) and self.attr != value:
            self.mark_error('must be set to ' + str(value))


    def date(self):
        'test that attr is a date string'
        if not isinstance(self.attr, datetime):
            self.mark_error('must be a date')


    def decimal(self, min=None, max=None):
        'test that attr is a decimal'
        if not isinstance(self.attr, float):
            self.mark_error('must be a decimal number')
        self.number(min, max)
        return self


    def email(self):
        'test that attr is a date string'
        if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", self.attr):
            self.mark_error('must be a valid email')
        return self


    def integer(self, min=None, max=None):
        'test that attr is an integer'
        if not isinstance(self.attr, int):
            self.mark_error('must be an integer')
        self.number(min, max)
        return self


    def items(self):
        # @todo
        if not isinstance(self.attr, list):
            self.mark_error('must be a list of DomesticItem objects')
        else:
            for i, item in enumerate(self.attr):
                v = item.validate()
                for attr_name, error_messages in v.errors.items():
                    for error_message in error_messages:
                        # mark error for items, with item's index and attribute name added to message
                        self.mark_error('item ' + str(i + 1) + ', ' + attr_name + ': ' + error_message)
        return self

    
    def number(self, min=None, max=None):
        'test number limits'
        if min and self.attr < min:
            self.mark_error('must be greater than or equal to ' + str(min))
        if max and self.attr > max:
            self.mark_error('must be less than or equal to ' + str(max))
        return self

    
    def phone(self):
        # only numbers, spaces and initial plus symbol permitted
        if not re.match(r"(^\+{0,1}[0-9 ]{1,19}$)", self.attr):
            self.mark_error('must be a valid phone number')
        return self

    
    def postcode(self):
        # @todo
        pass

    
    def state(self):
        if self.attr not in state_codes:
            self.mark_error('must be a valid Australian state or territory code')


    def string(self, length=None, maxlength=None, minlength=None):
        'test that attr is a string'
        if not isinstance(self.attr, str):
            self.mark_error('must be a text string')
        if length: 
            if len(self.attr) != length:
                self.mark_error('must be exactly ' + str(length) + ' characters long')
        else:
            if minlength and len(self.attr) < minlength:
                self.mark_error('must be greater than or equal to ' + str(minlength) + ' characters long')
            if maxlength and len(self.attr) > maxlength:
                self.mark_error('must be less than or equal to ' + str(maxlength) + ' characters long')
        return self


    def suburb(self):
        # @todo
        pass
