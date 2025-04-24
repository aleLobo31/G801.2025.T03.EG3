from .json_store import JsonStore
from ..account_management_config import BALANCES_STORE_FILE


class AccountBalanceJsonStore:
    class __AccountBalanceJsonStore(JsonStore):
        _file_name = BALANCES_STORE_FILE

    __instance = None

    def __new__(cls):
        if not AccountBalanceJsonStore.__instance:
            AccountBalanceJsonStore.__instance = AccountBalanceJsonStore.__AccountBalanceJsonStore()
        return AccountBalanceJsonStore.__instance