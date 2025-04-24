from .json_store import JsonStore
from ..account_management_config import TRANSACTIONS_STORE_FILE

class TransactionJsonStore:
    class __TransactionJsonStore(JsonStore):
        def __init__(self):
            self._file_name = TRANSACTIONS_STORE_FILE

        def load_list_from_file(self, fnf_error=False):
            super().load_list_from_file(fnf_error)
            return self._data_list

    __instance = None

    def __new__(cls):
        if not TransactionJsonStore.__instance:
            TransactionJsonStore.__instance = TransactionJsonStore.__TransactionJsonStore()
        return TransactionJsonStore.__instance
