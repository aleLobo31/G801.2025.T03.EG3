"""Transaction json class module"""
from uc3m_money.storage.json_store import JsonStore
from uc3m_money.account_management_config import TRANSACTIONS_STORE_FILE

class TransactionJsonStore:
    """Transaction json class implementing singleton"""
    class _TransactionJsonStore(JsonStore):

        def __init__(self):
            super().__init__()
            self._file_name = TRANSACTIONS_STORE_FILE

        def load_list_from_file(self, fnf_error=False):
            super().load_list_from_file(fnf_error)
            return self._data_list

    __instance= None

    def __new__(cls):
        if not TransactionJsonStore.__instance:
            TransactionJsonStore.__instance = TransactionJsonStore._TransactionJsonStore()
        return TransactionJsonStore.__instance
