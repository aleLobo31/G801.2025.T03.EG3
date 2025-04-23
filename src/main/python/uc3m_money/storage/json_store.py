import json

from ..account_management_exception import AccountManagementException

class JsonStore:
    _data_list = []
    _file_name = ""

    def __init__(self):
        self.load_list_from_file()

    def load_list_from_file(self, fnf_error=False):
        try:
            with open(self._file_name, "r", encoding="utf-8", newline="") as file:
                self._data_list = json.load(file)
        except FileNotFoundError as ex:
            if fnf_error:
                raise AccountManagementException("Wrong file  or file path") from ex
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
