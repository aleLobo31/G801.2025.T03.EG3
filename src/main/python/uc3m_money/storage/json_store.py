"""Json Store principal class module"""
import json

from uc3m_money.account_management_exception import AccountManagementException

class JsonStore:
    """JsonStore principal class"""
    _data_list = []
    _file_name = ""

    def __init__(self):
        ...

    def load_list_from_file(self, fnf_error=False):
        """loads into data_list the file_name file"""
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
        """writes into file_name file the content of data_list"""
        try:
            with open(self._file_name, "w", encoding="utf-8", newline="") as file:
                json.dump(self._data_list, file, indent=2)
        except FileNotFoundError as ex:
            raise AccountManagementException("Wrong file  or file path") from ex
        except json.JSONDecodeError as ex:
            raise AccountManagementException("JSON Decode Error - Wrong JSON Format") from ex

    def add_item(self, item):
        """main method, loads content of file, adds the item, and saves into the same file"""
        self.load_list_from_file()
        self._data_list.append(item)
        self.save_list_to_file()

    def find_item(self, key, value):
        """method to find an item in data_list"""
        for item in self._data_list:
            if item.get(key) == value:
                return item
        return None
