from .json_store import JsonStore
from ..account_management_config import BALANCES_STORE_FILE


class AccountBalanceJsonStore(JsonStore):
    _file_name = BALANCES_STORE_FILE