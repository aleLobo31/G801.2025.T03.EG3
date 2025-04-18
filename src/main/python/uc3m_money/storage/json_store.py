import json

from ..account_management_config import DEPOSITS_STORE_FILE, TRANSACTIONS_STORE_FILE, BALANCES_STORE_FILE
from ..account_management_exception import AccountManagementException

class JsonStore:
    _data_list = []
    _file_name = ""

    def __init__(self):
        self.load_list_from_file()

    def load_list_from_file(self):
        try:
            with open(self._file_name, "r", encoding="utf-8", newline="") as file:
                self._data_list = json.load(file)
        except FileNotFoundError:
            self._data_list = []
        except json.JSONDecodeError as ex:
            raise AccountManagementException("JSON Decode Error - Wrong JSON Format") from ex

    def save_list_to_file(self):
        try:
            with open(self._file_name, "w", encoding="utf-8", newline="") as file:
                json.dump(self._data_list, file, indent=2)
        except FileNotFoundError as ex:
            raise AccountManagementException("Wrong file  or file path") from ex
        except json.JSONDecodeError as ex:
            raise AccountManagementException("JSON Decode Error - Wrong JSON Format") from ex

    def add_item(self, item):
        self._data_list.append(item)
        self.save_list_to_file()

    def find_item(self, key, value):
        for item in self._data_list:
            if item.get(key) == value:
                return item
        return None

def get_deposit_iban_and_amount(input_deposit):
    try:
        deposit_iban = input_deposit["IBAN"]
        deposit_amount = input_deposit["AMOUNT"]
    except KeyError as e:
        raise AccountManagementException("Error - Invalid Key in JSON") from e
    return deposit_amount, deposit_iban


def input_deposit_json_store(input_file):
    try:
        with open(input_file, "r", encoding="utf-8", newline="") as file:
            input_deposit = json.load(file)
    except FileNotFoundError as ex:
        raise AccountManagementException("Error: file input not found") from ex
    except json.JSONDecodeError as ex:
        raise AccountManagementException("JSON Decode Error - Wrong JSON Format") from ex
    # comprobar valores del fichero
    deposit_amount, deposit_iban = get_deposit_iban_and_amount(input_deposit)
    return deposit_amount, deposit_iban


def transactions_json_store():
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


def account_balance_json_store(final_balance):
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