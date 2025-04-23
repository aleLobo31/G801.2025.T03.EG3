from .json_store import JsonStore
from ..account_management_config import TRANSACTIONS_STORE_FILE

class TransactionJsonStore(JsonStore):

    def __init__(self):
        self._file_name = TRANSACTIONS_STORE_FILE

    def load_list_from_file(self, fnf_error=False):
        super().load_list_from_file(fnf_error)
        return self._data_list


