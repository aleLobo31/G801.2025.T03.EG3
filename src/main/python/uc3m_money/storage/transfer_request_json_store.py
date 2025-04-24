"""Transfer request json class module"""
from uc3m_money.storage.json_store import JsonStore
from uc3m_money.account_management_exception import AccountManagementException
from uc3m_money.account_management_config import TRANSFERS_STORE_FILE


class TransferRequestJsonStore:
    """Transfer request json class implementing singleton"""
    class _TransferRequestJsonStore(JsonStore):
        """Private class with all the implementation"""
        _file_name = TRANSFERS_STORE_FILE

        def add_item(self, item):
            transfer_request_found = self.find_item(key="transfer_code", value=item.transfer_code)
            if transfer_request_found:
                raise AccountManagementException("Duplicated transfer in transfer list")
            super().add_item(item.to_json())

    __instance = None

    def __new__(cls):
        if not TransferRequestJsonStore.__instance:
            TransferRequestJsonStore.__instance = TransferRequestJsonStore._TransferRequestJsonStore()
        return TransferRequestJsonStore.__instance
