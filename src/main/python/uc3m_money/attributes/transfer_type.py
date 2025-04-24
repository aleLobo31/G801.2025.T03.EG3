"""Attribute class Transfer Type module"""
from uc3m_money.attributes.attribute import Attribute

class TransferType(Attribute):
    """Attribute class Transfer Type"""
    def __init__(self, transfer_type):
        super().__init__()
        self._validation_pattern = r"(ORDINARY|INMEDIATE|URGENT)"
        self._exception_message = "Invalid transfer type"
        self._attribute_value = self._validate(transfer_type)
