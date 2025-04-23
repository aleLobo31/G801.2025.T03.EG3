"""Account manager module """
from datetime import datetime, timezone

from uc3m_money.transfer_request import TransferRequest
from uc3m_money.account_deposit import AccountDeposit
from uc3m_money.account_balance import AccountBalance
from uc3m_money.storage.transfer_request_json_store import TransferRequestJsonStore
from uc3m_money.storage.deposit_json_store import DepositJsonStore
from uc3m_money.storage.account_balance_json_store import AccountBalanceJsonStore

class AccountManager:
    """Class for providing the methods for managing the orders"""
    class __AccountManager:
        def __init__(self):
            pass
        #pylint: disable=too-many-arguments
        @staticmethod
        def transfer_request(from_iban: str,
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

            all_transfers = TransferRequestJsonStore()
            all_transfers.add_item(new_transfer_request)

            return new_transfer_request.transfer_code

        @staticmethod
        def deposit_into_account(input_file:str)->str:
            """manages the deposits received for accounts"""
            new_deposit = AccountDeposit.create_new_deposit_from_file(input_file)

            all_deposits = DepositJsonStore()
            all_deposits.add_item(new_deposit)

            return new_deposit.deposit_signature

        @staticmethod
        def calculate_balance(iban:str)->bool:
            """calculate the balance for a given iban"""
            new_account_balance = AccountBalance(iban)

            final_balance = {"IBAN": new_account_balance.iban,
                             "time": datetime.timestamp(datetime.now(timezone.utc)),
                             "BALANCE": new_account_balance.total_balance}

            all_balances = AccountBalanceJsonStore()
            all_balances.add_item(final_balance)

            return True

    __instance = None

    def __new__(cls):
        if not AccountManager.__instance:
            AccountManager.__instance = AccountManager.__AccountManager()
        return AccountManager.__instance
