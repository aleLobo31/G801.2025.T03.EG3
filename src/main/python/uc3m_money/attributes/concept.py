from uc3m_money.attributes.attribute import Attribute

class Concept(Attribute):
    def __init__(self, concept):
        self._validation_pattern = r"^(?=^.{10,30}$)([a-zA-Z]+(\s[a-zA-Z]+)+)$"
        self._exception_message = "Invalid concept format"
        self._attribute_value = self._validate(concept)