"""Singleton account manager test case"""
import unittest
from uc3m_money.account_manager import AccountManager

class TestSingletonAccountManagerTests(unittest.TestCase):
    """Class for testing account manager"""
    def test_singleton_account_manager(self):
        """Testing three different variables that should be the same object"""
        account_manager_1 = AccountManager()
        account_manager_2 = AccountManager()
        account_manager_3 = AccountManager()

        self.assertEqual(account_manager_1, account_manager_2)
        self.assertEqual(account_manager_1, account_manager_3)
        self.assertEqual(account_manager_2, account_manager_3)
