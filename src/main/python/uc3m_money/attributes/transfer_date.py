from datetime import datetime, timezone

from uc3m_money.account_management_exception import AccountManagementException
from uc3m_money.attributes.attribute import Attribute

class TransferDate(Attribute):
    def __init__(self, transfer_date):
        self._validation_pattern = r"^(([0-2]\d|3[0-1])\/(0\d|1[0-2])\/\d\d\d\d)$"
        self._exception_message = "Invalid date format"
        self._attribute_value = self._validate(transfer_date)

    def _validate(self, transfer_date):
        try:
            parsed_transfer_date  = datetime.strptime(super()._validate(transfer_date), "%d/%m/%Y").date()
        except ValueError as ex:
            raise AccountManagementException(self._exception_message) from ex

        if parsed_transfer_date < datetime.now(timezone.utc).date():
            raise AccountManagementException("Transfer date must be today or later.")

        if parsed_transfer_date.year < 2025 or parsed_transfer_date.year > 2050:
            raise AccountManagementException(self._exception_message)
        return transfer_date