import json

from uc3m_money.account_management_config import TRANSACTIONS_STORE_FILE
from uc3m_money.account_management_exception import AccountManagementException
from uc3m_money.attributes.iban import Iban

class AccountBalance:
    def __init__(self, iban):
        self._iban = Iban(iban).attribute_value
        self._transaction_store = self.transactions_json_store()
        self._total_balance = self.get_total_balance(self._iban, self._transaction_store)

    @staticmethod
    def transactions_json_store():
        try:
            with open(TRANSACTIONS_STORE_FILE, "r", encoding="utf-8", newline="") as file:
                transaction_store = json.load(file)
        except FileNotFoundError as ex:
            raise AccountManagementException("Wrong file  or file path") from ex
        except json.JSONDecodeError as ex:
            raise AccountManagementException("JSON Decode Error - Wrong JSON Format") from ex
        return transaction_store

    def get_total_balance(self, iban, transaction_store):
        iban_found = False
        total_balance = 0
        for transaction in transaction_store:
            # print(transaction["IBAN"] + " - " + iban)
            if transaction["IBAN"] == iban:
                total_balance += float(transaction["amount"])
                iban_found = True
        if not iban_found:
            raise AccountManagementException("IBAN not found")
        return total_balance

    @property
    def iban(self):
        return self._iban

    @property
    def total_balance(self):
        return self._total_balance