from uc3m_money.attributes.attribute import Attribute

class TransferType(Attribute):
    def __init__(self, transfer_type):
        self._validation_pattern = r"(ORDINARY|INMEDIATE|URGENT)"
        self._exception_message = "Invalid transfer type"
        self._attribute_value = self._validate(transfer_type)