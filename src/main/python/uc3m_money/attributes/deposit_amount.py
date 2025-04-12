from uc3m_money.account_management_exception import  AccountManagementException
from uc3m_money.attributes.attribute import Attribute

class DepositAmount(Attribute):
    def __init__(self, amount):
        self._validation_pattern = r"^EUR [0-9]{4}\.[0-9]{2}"
        self._exception_message = "Error - Invalid deposit amount"
        self._attribute_value = self._validate(amount)

    def _validate(self, amount):
        parsed_deposit_amount = float(super()._validate(amount)[4:])
        if parsed_deposit_amount == 0:
            raise AccountManagementException("Error - Deposit must be greater than 0")
        return parsed_deposit_amount