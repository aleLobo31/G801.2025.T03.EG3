from uc3m_money.account_management_exception import AccountManagementException
from uc3m_money.attributes.attribute import Attribute

class Iban(Attribute):
    def __init__(self, iban):
        self._validation_pattern = r"^ES[0-9]{22}"
        self._exception_message = "Invalid IBAN format"
        self._attribute_value = self._validate(iban)

    def _validate(self, input_iban):
        iban = super()._validate(input_iban)
        original_code = iban[2:4]

        # Replacing the control
        iban = iban[:2] + "00" + iban[4:]
        iban = iban[4:] + iban[:4]

        # Convertir el IBAN en una cadena numérica, reemplazando letras por números
        iban = (iban.replace('A', '10').replace('B', '11').
                replace('C', '12').replace('D', '13').replace('E', '14').
                replace('F', '15'))
        iban = (iban.replace('G', '16').replace('H', '17').
                replace('I', '18').replace('J', '19').replace('K', '20').
                replace('L', '21'))
        iban = (iban.replace('M', '22').replace('N', '23').
                replace('O', '24').replace('P', '25').replace('Q', '26').
                replace('R', '27'))
        iban = (iban.replace('S', '28').replace('T', '29').replace('U', '30').
                replace('V', '31').replace('W', '32').replace('X', '33'))
        iban = iban.replace('Y', '34').replace('Z', '35')

        # Convertir la cadena en un número entero
        parsed_int_iban = int(iban)

        # Calcular el módulo 97
        mod = parsed_int_iban % 97

        # Calcular el dígito de control (97 menos el módulo)
        control_digit = 98 - mod

        if int(original_code) != control_digit:
            # print(dc)
            raise AccountManagementException("Invalid IBAN control digit")

        return input_iban
