"""Account manager module """
import re
import json
from datetime import datetime, timezone
from uc3m_money.account_management_exception import AccountManagementException
from uc3m_money.account_management_config import (TRANSFERS_STORE_FILE,
                                        DEPOSITS_STORE_FILE,
                                        TRANSACTIONS_STORE_FILE,
                                        BALANCES_STORE_FILE)

from uc3m_money.transfer_request import TransferRequest
from uc3m_money.account_deposit import AccountDeposit


class AccountManager:
    """Class for providing the methods for managing the orders"""
    def __init__(self):
        pass

    @staticmethod
    def validate_iban(input_iban: str):
        """
    Calcula el dígito de control de un IBAN español.

    Args:
        input_iban (str): El IBAN sin los dos últimos dígitos (dígito de control).

    Returns:
        str: El dígito de control calculado.
        """
        iban_regex = re.compile(r"^ES[0-9]{22}")
        iban_match = iban_regex.fullmatch(input_iban)
        if not iban_match:
            raise AccountManagementException("Invalid IBAN format")
        iban = input_iban
        original_code = iban[2:4]
        #replacing the control
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

        # Mover los cuatro primeros caracteres al final

        # Convertir la cadena en un número entero
        parsed_int_iban = int(iban)

        # Calcular el módulo 97
        mod = parsed_int_iban % 97

        # Calcular el dígito de control (97 menos el módulo)
        control_digit = 98 - mod

        if int(original_code) != control_digit:
            #print(dc)
            raise AccountManagementException("Invalid IBAN control digit")

        return input_iban

    def validate_concept(self, concept: str):
        """regular expression for checking the minimum and maximum length as well as
        the allowed characters and spaces restrictions
        there are other ways to check this"""
        concept_regex = re.compile(r"^(?=^.{10,30}$)([a-zA-Z]+(\s[a-zA-Z]+)+)$")

        concept_match = concept_regex.fullmatch(concept)
        if not concept_match:
            raise AccountManagementException ("Invalid concept format")

    def validate_transfer_date(self, transfer_date):
        """validates the arrival date format  using regex"""
        transfer_date_regex = re.compile(r"^(([0-2]\d|3[0-1])\/(0\d|1[0-2])\/\d\d\d\d)$")
        transfer_date_match = transfer_date_regex.fullmatch(transfer_date)
        if not transfer_date_match:
            raise AccountManagementException("Invalid date format")

        try:
            parsed_transfer_date  = datetime.strptime(transfer_date, "%d/%m/%Y").date()
        except ValueError as ex:
            raise AccountManagementException("Invalid date format") from ex

        if parsed_transfer_date < datetime.now(timezone.utc).date():
            raise AccountManagementException("Transfer date must be today or later.")

        if parsed_transfer_date.year < 2025 or parsed_transfer_date.year > 2050:
            raise AccountManagementException("Invalid date format")
        return transfer_date
    #pylint: disable=too-many-arguments
    def transfer_request(self, from_iban: str,
                         to_iban: str,
                         concept: str,
                         transfer_type: str,
                         date: str,
                         amount: float)->str:
        """first method: receives transfer info and
        stores it into a file"""
        self.validate_iban(from_iban)
        self.validate_iban(to_iban)
        self.validate_concept(concept)
        self.validate_transfer_type(date, transfer_type)
        self.validate_transfer_amount(amount)

        new_transfer_request = TransferRequest(from_iban=from_iban,
                                     to_iban=to_iban,
                                     transfer_concept=concept,
                                     transfer_type=transfer_type,
                                     transfer_date=date,
                                     transfer_amount=amount)

        try:
            with open(TRANSFERS_STORE_FILE, "r", encoding="utf-8", newline="") as file:
                transfer_store = json.load(file)
        except FileNotFoundError:
            transfer_store = []
        except json.JSONDecodeError as ex:
            raise AccountManagementException("JSON Decode Error - Wrong JSON Format") from ex

        for transfer in transfer_store:
            if (transfer["from_iban"] == new_transfer_request.from_iban and
                    transfer["to_iban"] == new_transfer_request.to_iban and
                    transfer["transfer_date"] == new_transfer_request.transfer_date and
                    transfer["transfer_amount"] == new_transfer_request.transfer_amount and
                    transfer["transfer_concept"] == new_transfer_request.transfer_concept and
                    transfer["transfer_type"] == new_transfer_request.transfer_type):
                raise AccountManagementException("Duplicated transfer in transfer list")

        transfer_store.append(new_transfer_request.to_json())

        try:
            with open(TRANSFERS_STORE_FILE, "w", encoding="utf-8", newline="") as file:
                json.dump(transfer_store, file, indent=2)
        except FileNotFoundError as ex:
            raise AccountManagementException("Wrong file  or file path") from ex
        except json.JSONDecodeError as ex:
            raise AccountManagementException("JSON Decode Error - Wrong JSON Format") from ex

        return new_transfer_request.transfer_code

    def validate_transfer_amount(self, amount):
        try:
            parsed_float_amount = float(amount)
        except ValueError as ex:
            raise AccountManagementException("Invalid transfer amount") from ex
        parsed_string_amount = str(parsed_float_amount)
        if '.' in parsed_string_amount:
            number_of_decimals = len(parsed_string_amount.split('.')[1])
            if number_of_decimals > 2:
                raise AccountManagementException("Invalid transfer amount")
        if parsed_float_amount < 10 or parsed_float_amount > 10000:
            raise AccountManagementException("Invalid transfer amount")

    def validate_transfer_type(self, date, transfer_type):
        transfer_type_regex = re.compile(r"(ORDINARY|INMEDIATE|URGENT)")
        transfer_type_match = transfer_type_regex.fullmatch(transfer_type)
        if not transfer_type_match:
            raise AccountManagementException("Invalid transfer type")
        self.validate_transfer_date(date)

    def deposit_into_account(self, input_file:str)->str:
        """manages the deposits received for accounts"""
        try:
            with open(input_file, "r", encoding="utf-8", newline="") as file:
                input_deposit = json.load(file)
        except FileNotFoundError as ex:
            raise AccountManagementException("Error: file input not found") from ex
        except json.JSONDecodeError as ex:
            raise AccountManagementException("JSON Decode Error - Wrong JSON Format") from ex

        # comprobar valores del fichero
        deposit_amount, deposit_iban = self.get_deposit_iban_and_amount(input_deposit)


        deposit_iban = self.validate_iban(deposit_iban)
        parsed_deposit_amount = self.validate_deposit_amount(deposit_amount)

        new_deposit = AccountDeposit(to_iban=deposit_iban,
                                     deposit_amount=parsed_deposit_amount)

        try:
            with open(DEPOSITS_STORE_FILE, "r", encoding="utf-8", newline="") as file:
                deposit_store = json.load(file)
        except FileNotFoundError as ex:
            deposit_store = []
        except json.JSONDecodeError as ex:
            raise AccountManagementException("JSON Decode Error - Wrong JSON Format") from ex

        deposit_store.append(new_deposit.to_json())

        try:
            with open(DEPOSITS_STORE_FILE, "w", encoding="utf-8", newline="") as file:
                json.dump(deposit_store, file, indent=2)
        except FileNotFoundError as ex:
            raise AccountManagementException("Wrong file  or file path") from ex
        except json.JSONDecodeError as ex:
            raise AccountManagementException("JSON Decode Error - Wrong JSON Format") from ex

        return new_deposit.deposit_signature

    def validate_deposit_amount(self, deposit_amount):
        deposit_amount_regex = re.compile(r"^EUR [0-9]{4}\.[0-9]{2}")
        deposit_amount_match = deposit_amount_regex.fullmatch(deposit_amount)
        if not deposit_amount_match:
            raise AccountManagementException("Error - Invalid deposit amount")
        parsed_deposit_amount = float(deposit_amount[4:])
        if parsed_deposit_amount == 0:
            raise AccountManagementException("Error - Deposit must be greater than 0")
        return parsed_deposit_amount

    def get_deposit_iban_and_amount(self, input_deposit):
        try:
            deposit_iban = input_deposit["IBAN"]
            deposit_amount = input_deposit["AMOUNT"]
        except KeyError as e:
            raise AccountManagementException("Error - Invalid Key in JSON") from e
        return deposit_amount, deposit_iban

    def read_transactions_file(self):
        """loads the content of the transactions file
        and returns a list"""
        try:
            with open(TRANSACTIONS_STORE_FILE, "r", encoding="utf-8", newline="") as file:
                transaction_store = json.load(file)
        except FileNotFoundError as ex:
            raise AccountManagementException("Wrong file  or file path") from ex
        except json.JSONDecodeError as ex:
            raise AccountManagementException("JSON Decode Error - Wrong JSON Format") from ex
        return transaction_store


    def calculate_balance(self, iban:str)->bool:
        """calculate the balance for a given iban"""
        iban = self.validate_iban(iban)
        transaction_store = self.read_transactions_file()
        total_balance = self.get_total_balance(iban, transaction_store)

        final_balance = {"IBAN": iban,
                        "time": datetime.timestamp(datetime.now(timezone.utc)),
                        "BALANCE": total_balance}

        try:
            with open(BALANCES_STORE_FILE, "r", encoding="utf-8", newline="") as file:
                balance_store = json.load(file)
        except FileNotFoundError:
            balance_store = []
        except json.JSONDecodeError as ex:
            raise AccountManagementException("JSON Decode Error - Wrong JSON Format") from ex

        balance_store.append(final_balance)

        try:
            with open(BALANCES_STORE_FILE, "w", encoding="utf-8", newline="") as file:
                json.dump(balance_store, file, indent=2)
        except FileNotFoundError as ex:
            raise AccountManagementException("Wrong file  or file path") from ex
        return True

    def get_total_balance(self, iban, transaction_store):
        iban_found = False
        total_balance = 0
        for transaction in transaction_store:
            # print(transaction["IBAN"] + " - " + iban)
            if transaction["IBAN"] == iban:
                total_balance += float(transaction["amount"])
                iban_found = True
        if not iban_found:
            raise AccountManagementException("IBAN not found")
        return total_balance
