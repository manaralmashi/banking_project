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
    def test_success_deposit_checking(self):
        # [ Test 9 ] success deposit to Checking Account
        # Use ( account2: Only checking account)
        initial_balance = self.customer2.balance_checking
        deposit_amount = 300
        expected_balance = initial_balance + deposit_amount
        
        success, message = self.account2.deposit(deposit_amount, "checking")
        self.assertTrue(success)
        self.assertIn("deposited to Checking Account", message)
        
        # Verify balance update
        self.assertEqual(self.customer2.balance_checking, expected_balance)

    def test_success_deposit_savings(self):
        # [ Test 10 ] success deposit to Savings Account
        # Use ( account3: Only savings account)
        initial_balance = self.customer3.balance_savings
        deposit_amount = 500
        expected_balance = initial_balance + deposit_amount
        
        success, message = self.account3.deposit(deposit_amount, "savings")
        self.assertTrue(success)
        self.assertIn("deposited to Savings Account", message)
        
        # Verify balance update
        self.assertEqual(self.customer3.balance_savings, expected_balance)

    def test_deposit_no_checking_account(self):
        # [ Test 11 ] deposit to Checking Account that does NOT exist
        # Use ( account1: No accounts)
        success, message = self.account1.deposit(100, "checking")
        
        self.assertFalse(success)
        self.assertIn("do NOT have a Checking Account", message)
        self.assertIsNone(self.customer1.balance_checking)  # balance_checking = None

    def test_deposit_no_savings_account(self):
        # [ Test 12 ] deposit to Savings Account that does NOT exist
        # Use ( account1: No accounts)
        success, message = self.account1.deposit(100, "savings")

        self.assertFalse(success)
        self.assertIn("do NOT have a Savings Account", message)
        self.assertIsNone(self.customer1.balance_savings)  # balance_savings = None

    def test_deposit_invalid_account_type(self):
        # [ Test 13 ] deposit to Invalid account type
        # Use ( account4: Both checking and savings accounts)
        initial_balance_checking = self.customer4.balance_checking
        initial_balance_savings = self.customer4.balance_savings
        
        success, message = self.account4.deposit(100, "markit")
        self.assertFalse(success)
        self.assertIn("Invalid Account Type", message)
        
        # Verify balances didn't change
        self.assertEqual(self.customer4.balance_checking, initial_balance_checking)
        self.assertEqual(self.customer4.balance_savings, initial_balance_savings)

    def test_deposit_zero_amount(self):
        # [ Test 14 ] deposit amount = 0 into account
        # Use ( account2: Only checking account)
        initial_balance = self.customer2.balance_checking
        
        success, message = self.account2.deposit(0, "checking")
        self.assertFalse(success)
        self.assertIn("Deposit amount must be greater than zero", message)
        self.assertEqual(self.customer2.balance_checking, initial_balance)  # Verify balances didn't change

    def test_deposit_negative_amount(self):
        # [ Test 15 ] deposit negative amount (edge case)
        # Use ( account2: Only checking account)
        initial_balance = self.customer2.balance_checking
        
        success, message = self.account2.deposit(-250, "checking")
        self.assertFalse(success)
        self.assertIn("Deposit amount must be greater than zero", message)
        self.assertEqual(self.customer2.balance_checking, initial_balance)  # Verify balances didn't change

    def test_deposit_decimal_amount(self):
        # [ Test 16 ] deposit decimal amount
        # Use ( account2: Only checking account)
        initial_balance = self.customer2.balance_checking
        decimal_amount = 153.67
        expected_balance = initial_balance + decimal_amount
        
        success, message = self.account2.deposit(decimal_amount, "checking")
        self.assertTrue(success)
        self.assertIn("deposited to Checking Account", message)
        
        # Used `assertAlmostEqual()` instead of `assertEqual()` floating-point comparisons to avoid precision issues.
        self.assertAlmostEqual(self.customer2.balance_checking, expected_balance, places=2)

    def test_deposit_multiple_times_checking(self):
        # [ Test 17 ] multiple deposits to Checking Account
        # Use ( account2: Only checking account)
        initial_balance = self.customer2.balance_checking
        
        # deposit 1
        success1, message1 = self.account2.deposit(200, "checking")
        self.assertTrue(success1)
        self.assertEqual(self.customer2.balance_checking, initial_balance + 200)
        
        # deposit 2
        success2, message2 = self.account2.deposit(100, "checking")
        self.assertTrue(success2)
        self.assertEqual(self.customer2.balance_checking, initial_balance + 300)
        
        # deposit 3
        success3, message3 = self.account2.deposit(150, "checking")
        self.assertTrue(success3)
        self.assertEqual(self.customer2.balance_checking, initial_balance + 450)

    # --------------------------------------- Transfer Tests ---------------------------------------
    def test_transfer(self):
        pass
        
    # [3]. close - (if i want run something after test)
    def tearDown(self):
        pass