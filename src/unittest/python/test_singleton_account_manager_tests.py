import unittest
from uc3m_money.account_manager import AccountManager

class TestSingletonAccountManagerTests(unittest.TestCase):
    def test_singleton_account_manager(self):
        account_manager_1 = AccountManager()
        account_manager_2 = AccountManager()
        account_manager_3 = AccountManager()

        self.assertEqual(account_manager_1, account_manager_2)
        self.assertEqual(account_manager_1, account_manager_3)
        self.assertEqual(account_manager_2, account_manager_3)
