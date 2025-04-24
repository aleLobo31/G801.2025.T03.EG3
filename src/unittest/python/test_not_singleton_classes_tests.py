import unittest
from uc3m_money.account_deposit import AccountDeposit

class TestNotSingletonTests(unittest.TestCase):
    def test_not_singleton_account_deposit(self):
        account_deposit_1 = AccountDeposit("ES9420805801101234567891", "EUR 1234.50")
        account_deposit_2 = AccountDeposit("ES9420805801101234567891", "EUR 1234.50")
        account_deposit_3 = AccountDeposit("ES9420805801101234567891", "EUR 1234.50")

        self.assertNotEqual(account_deposit_1, account_deposit_2)
        self.assertNotEqual(account_deposit_1, account_deposit_3)
        self.assertNotEqual(account_deposit_2, account_deposit_3)
