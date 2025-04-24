"""Deposit json class module"""
from uc3m_money.storage.json_store import JsonStore
from uc3m_money.account_management_config import DEPOSITS_STORE_FILE


class DepositJsonStore:
    """Deposit json class implementing singleton"""
    class _DepositJsonStore(JsonStore):
        """private class with all the deposit json implementation"""
        _file_name = DEPOSITS_STORE_FILE

        def add_item(self, item):
            self._data_list.append(item.to_json())
            self.save_list_to_file()

    __instance = None

    def __new__(cls):
        if not DepositJsonStore.__instance:
            DepositJsonStore.__instance = DepositJsonStore._DepositJsonStore()
        return DepositJsonStore.__instance
