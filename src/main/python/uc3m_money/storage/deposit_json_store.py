from .json_store import JsonStore
from ..account_management_config import DEPOSITS_STORE_FILE


class DepositJsonStore(JsonStore):
    _file_name = DEPOSITS_STORE_FILE

    def add_item(self, item):
        self._data_list.append(item.to_json())
        self.save_list_to_file()
