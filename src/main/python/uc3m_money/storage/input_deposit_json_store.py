from .json_store import JsonStore

class InputDepositJsonStore:
    class __InputDepositJsonStore(JsonStore):
        def __init__(self, input_file):
            self._file_name = input_file

        def load_list_from_file(self, fnf_error=False):
            super().load_list_from_file(fnf_error)
            return self._data_list

    __instance = None

    def __new__(cls, input_name):
        if not InputDepositJsonStore.__instance:
            InputDepositJsonStore.__instance = InputDepositJsonStore.__InputDepositJsonStore(input_name)
        else:
            InputDepositJsonStore.__instance._file_name = input_name
        return InputDepositJsonStore.__instance
