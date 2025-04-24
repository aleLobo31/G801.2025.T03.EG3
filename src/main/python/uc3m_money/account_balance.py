"""Account balance module"""
from uc3m_money.account_management_exception import AccountManagementException
from uc3m_money.attributes.iban import Iban
from uc3m_money.storage.transaction_json_store import TransactionJsonStore


class AccountBalance:
    """Account balance manager"""
    def __init__(self, iban):
        self._iban = Iban(iban).attribute_value
        self._total_balance = self.get_total_balance(self._iban)

    def get_total_balance(self, iban):
        """Sums total balance of a given IBAN"""
        transaction_store = TransactionJsonStore()
        transactions = transaction_store.load_list_from_file(fnf_error=True) # pylint: disable=no-member

        iban_found = False
        total_balance = 0
        for transaction in transactions:
            # print(transaction["IBAN"] + " - " + iban)
            if transaction["IBAN"] == iban:
                total_balance += float(transaction["amount"])
                iban_found = True
        if not iban_found:
            raise AccountManagementException("IBAN not found")
        return total_balance

    @property
    def iban(self):
        """IBAN property"""
        return self._iban

    @property
    def total_balance(self):
        """Total balance property"""
        return self._total_balance
