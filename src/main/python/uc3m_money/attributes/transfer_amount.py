from uc3m_money.account_management_exception import AccountManagementException
from uc3m_money.attributes.attribute import Attribute

class TransferAmount(Attribute):
    def __init__(self, amount):
        self._exception_message = "Invalid transfer amount"
        self._attribute_value = self._validate(amount)

    def _validate(self, amount):
        try:
            parsed_float_amount = float(amount)
        except ValueError as ex:
            raise AccountManagementException(self._exception_message) from ex
        parsed_string_amount = str(parsed_float_amount)
        if '.' in parsed_string_amount:
            number_of_decimals = len(parsed_string_amount.split('.')[1])
            if number_of_decimals > 2:
                raise AccountManagementException(self._exception_message)
        if parsed_float_amount < 10 or parsed_float_amount > 10000:
            raise AccountManagementException(self._exception_message)
        return amount