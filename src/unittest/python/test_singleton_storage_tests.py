import unittest
from uc3m_money.storage.account_balance_json_store import AccountBalanceJsonStore
from uc3m_money.storage.deposit_json_store import DepositJsonStore
from uc3m_money.storage.input_deposit_json_store import InputDepositJsonStore
from uc3m_money.storage.transaction_json_store import TransactionJsonStore
from uc3m_money.storage.transfer_request_json_store import TransferRequestJsonStore

class TestSingletonStorageTests(unittest.TestCase):
    def test_singleton_store(self):
        stores = [
            (TransferRequestJsonStore, "TransferRequestJsonStore"),
            (DepositJsonStore, "DepositJsonStore"),
            (AccountBalanceJsonStore, "AccountBalanceJsonStore"),
            (TransactionJsonStore, "TransactionJsonStore")
        ]

        for store_class, store_name in stores:
            with self.subTest(store=store_name):
                instance1 = store_class()
                instance2 = store_class()
                instance3 = store_class()

                self.assertEqual(instance1, instance2)
                self.assertEqual(instance1, instance3)
                self.assertEqual(instance2, instance3)

    def test_singleton_input_deposit_json_store(self):
            input_deposit_json_store_1 = InputDepositJsonStore("File1")
            input_deposit_json_store_2 = InputDepositJsonStore("File1")
            input_deposit_json_store_3 = InputDepositJsonStore("File1")

            self.assertEqual(input_deposit_json_store_1, input_deposit_json_store_2)
            self.assertEqual(input_deposit_json_store_1, input_deposit_json_store_3)
            self.assertEqual(input_deposit_json_store_2, input_deposit_json_store_3)

            input_deposit_json_store_4 = InputDepositJsonStore("File2")

            self.assertEqual(input_deposit_json_store_1, input_deposit_json_store_4)

