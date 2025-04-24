"""Attribute class module"""
import re

from uc3m_money.account_management_exception import AccountManagementException

class Attribute:
    """Attribute principal class"""
    def __init__(self):
        self._validation_pattern = r''
        self._exception_message = ''
        self._attribute_value = ''

    def _validate(self, value):
        regex = re.compile(self._validation_pattern)
        regex_match = regex.fullmatch(value)
        if not regex_match:
            raise AccountManagementException(self._exception_message)
        return value

    @property
    def attribute_value(self):
        """attribute_value property"""
        return self._attribute_value

    @attribute_value.setter
    def attribute_value(self, value):
        """attribute_value setter"""
        self._attribute_value = value
