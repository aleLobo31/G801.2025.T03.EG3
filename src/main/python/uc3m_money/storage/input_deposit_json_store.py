from .json_store import JsonStore

class InputDepositJsonStore(JsonStore):

    def __init__(self, input_file):
        self._file_name = input_file

    def load_list_from_file(self, fnf_error=False):
        super().load_list_from_file(fnf_error)
        return self._data_list