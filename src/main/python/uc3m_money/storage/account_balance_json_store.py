"""Account balance json class module"""
from uc3m_money.storage.json_store import JsonStore
from uc3m_money.account_management_config import BALANCES_STORE_FILE


class AccountBalanceJsonStore:
    """Account balance json class implementing singleton"""
    class _AccountBalanceJsonStore(JsonStore):
        """private class of account balance json"""
        _file_name = BALANCES_STORE_FILE

    __instance = None

    def __new__(cls):
        if not AccountBalanceJsonStore.__instance:
            AccountBalanceJsonStore.__instance = AccountBalanceJsonStore._AccountBalanceJsonStore()
        return AccountBalanceJsonStore.__instance
