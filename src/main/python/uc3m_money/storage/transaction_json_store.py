import json

from .json_store import JsonStore
from ..account_management_exception import AccountManagementException
from ..account_management_config import TRANSACTIONS_STORE_FILE

class TransactionJsonStore(JsonStore):
    def __init__(self):
        self._file_name = TRANSACTIONS_STORE_FILE

    def load_list_from_file(self):
        try:
            with open(self._file_name, "r", encoding="utf-8", newline="") as file:
                self._data_list = json.load(file)
        except FileNotFoundError as ex:
            raise AccountManagementException("Wrong file  or file path") from ex
        except json.JSONDecodeError as ex:
            raise AccountManagementException("JSON Decode Error - Wrong JSON Format") from ex
        return self._data_list
