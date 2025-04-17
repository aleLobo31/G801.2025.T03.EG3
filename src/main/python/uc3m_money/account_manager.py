"""Account manager module """
from datetime import datetime, timezone
from uc3m_money.account_management_exception import AccountManagementException
from uc3m_money.storage.json_store import save_transfer_request, input_deposit_json_store, deposit_json_store, \
    transactions_json_store, account_balance_json_store

from uc3m_money.transfer_request import TransferRequest
from uc3m_money.account_deposit import AccountDeposit
from uc3m_money.attributes.iban import Iban

class AccountManager:
    """Class for providing the methods for managing the orders"""
    def __init__(self):
        pass
    #pylint: disable=too-many-arguments
    def transfer_request(self, from_iban: str,
                         to_iban: str,
                         concept: str,
                         transfer_type: str,
                         date: str,
                         amount: float)->str:
        """first method: receives transfer info and
        stores it into a file"""

        new_transfer_request = TransferRequest(from_iban=from_iban,
                                     to_iban=to_iban,
                                     transfer_concept=concept,
                                     transfer_type=transfer_type,
                                     transfer_date=date,
                                     transfer_amount=amount)

        save_transfer_request(new_transfer_request)

        return new_transfer_request.transfer_code

    def deposit_into_account(self, input_file:str)->str:
        """manages the deposits received for accounts"""
        deposit_amount, deposit_iban = input_deposit_json_store(input_file)

        new_deposit = AccountDeposit(to_iban=deposit_iban,
                                     deposit_amount=deposit_amount)

        deposit_json_store(new_deposit)

        return new_deposit.deposit_signature

    def calculate_balance(self, iban:str)->bool:
        """calculate the balance for a given iban"""
        # iban = self.validate_iban(iban)
        iban = Iban(iban).attribute_value
        transaction_store = transactions_json_store()
        total_balance = self.get_total_balance(iban, transaction_store)

        final_balance = {"IBAN": iban,
                        "time": datetime.timestamp(datetime.now(timezone.utc)),
                        "BALANCE": total_balance}

        account_balance_json_store(final_balance)
        return True

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
