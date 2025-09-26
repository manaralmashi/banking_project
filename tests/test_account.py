import unittest
from bank.customer import Customer
from bank.account import Account
class TestAccount(unittest.TestCase):

    # [1]. open - (if i want run something before test)
    def setUp(self):
        # Customer objects - for testing
        self.customer1 = Customer('1', 'Salma', 'Yosuf', 'Salma@12345')
        self.customer2 = Customer('2', 'Alaa', 'Faisal', 'Alaa@1234', balance_checking = 200)
        self.customer3 = Customer('3', 'Hala', 'Saad', 'Hala@1234', balance_savings = 1500)
        self.customer4 = Customer('4', 'Hasan', 'Yaser', 'Hasan@1234', balance_checking = 3000, balance_savings = 5000)
        self.customer5 = Customer('5', 'Muna', 'Saif', 'Muna@1234', balance_checking = 15, balance_savings = 50)
        self.customer6 = Customer('6', 'Inactive', 'User', 'Inactive@123', balance_checking = 1000, balance_savings = 2000, is_active = False)

        # Account objects - for testing
        self.account1 = Account(self.customer1) # No accounts
        self.account2 = Account(self.customer2) # Only checking account
        self.account3 = Account(self.customer3) # Only savings account
        self.account4 = Account(self.customer4) # Both checking and savings accounts
        self.account5 = Account(self.customer5) # Low balance
        self.account6 = Account(self.customer6) # Deactive account

    # [2]. testing methods
    # --------------------------------------- Withdraw Tests ---------------------------------------
    def test_success_withdraw_checking(self):
        # [ Test 1 ] success withdraw from Checking Account
        # Use ( account2: Only checking account)
        success, message = self.account2.withdraw(100, "checking")
        self.assertTrue(success)
        self.assertIn("withdrawn from the Checking Account", message)
        self.assertEqual(self.customer2.balance_checking, 100)

    def test_success_withdraw_savings(self):
        # [ Test 2 ] success withdraw from Savings Account
        # Use ( account3: Only savings account)
        success, message = self.account3.withdraw(500, "savings")
        self.assertTrue(success)
        self.assertIn("withdrawn from the Savings Account", message)
        self.assertEqual(self.customer3.balance_savings, 1000)

    def test_withdraw_amount_greater_than_checking(self):
        # [ Test 3 ] withdraw from Checking Account that the amount is greater than in checking account
        # Use ( account2: Only checking account)
        success, message = self.account2.withdraw(300, "checking")
        self.assertFalse(success)
        self.assertIn("greater than the amount in your Checking Account", message)
        self.assertEqual(self.customer2.balance_checking, 200)  # balance doesn't change

    def test_withdraw_amount_greater_than_savings(self):
        # [ Test 4 ] withdraw from Checking Account that the amount is greater than in savings Account
        # Use ( account3: Only savings account)
        success, message = self.account3.withdraw(2000, "savings")
        self.assertFalse(success)
        self.assertIn("greater than the amount in your Savings Account", message)
        self.assertEqual(self.customer3.balance_savings, 1500)  # balance doesn't change

    def test_withdraw_no_checking_account(self):
        # [ Test 5 ] withdraw from Checking Account that does NOT exist
        # Use ( account1: No accounts)
        success, message = self.account1.withdraw(100, "checking")
        self.assertFalse(success)
        self.assertIn("do NOT have a Checking Account", message)

    def test_withdraw_no_savings_account(self):
        # [ Test 6 ] withdraw from Savings Account that does NOT exist
        # Use ( account1: No accounts)
        success, message = self.account1.withdraw(100, "savings")
        self.assertFalse(success)
        self.assertIn("do NOT have a Savings Account", message)

    def test_withdraw_invalid_account_type(self):
        # [ Test 7 ] withdraw from Invalid account type
        # Use ( account4: Both checking and savings accounts)
        success, message = self.account4.withdraw(100, "markit")
        self.assertFalse(success)
        self.assertIn("Invalid Account Type", message)

    def test_withdraw_from_deactive_account(self):
        # [ Test 8 ] withdraw from Deactive account type
        # Use ( account6: Deactive account)
        success, message = self.account6.withdraw(100, "checking")
        self.assertFalse(success)
        self.assertIn("Account is Deactive", message)
        self.assertEqual(self.customer6.balance_checking, 1000)  # balance doesn't change

    # --------------------------------------- Deposit Tests ---------------------------------------
    def test_deposit(self):
        pass
        
    # --------------------------------------- Transfer Tests ---------------------------------------
    def test_transfer(self):
        pass
        
    # [3]. close - (if i want run something after test)
    def tearDown(self):
        pass