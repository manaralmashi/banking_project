import unittest
from bank.customer import Customer
from bank.account import Account
from bank.bank_management import BankManagement
class TestAccount(unittest.TestCase):

    # [1]. open - (if i want run something before test)
    def setUp(self):
        # Customer objects - for testing
        self.customer1 = Customer('1', 'Salma', 'Yosuf', 'Salma@12345')
        self.customer2 = Customer('2', 'Alaa', 'Faisal', 'Alaa@1234', balance_checking = 200)
        self.customer3 = Customer('3', 'Hala', 'Saad', 'Hala@1234', balance_savings = 1500)
        self.customer4 = Customer('4', 'Hasan', 'Yaser', 'Hasan@1234', balance_checking = 3000, balance_savings = 5000)
        self.customer5 = Customer('5', 'Muna', 'Saif', 'Muna@1234', balance_checking = 15, balance_savings = 50)
        self.customer6 = Customer('6', 'deactive', 'User', 'deactive@123', balance_checking = 1000, balance_savings = 2000, is_active = False)
        # Customer objects - for Overdraft testing 
        self.customer7 = Customer('7', 'Ahmed', 'Saad', 'Ahmed@123', balance_checking = 50)
        self.customer8 = Customer('8', 'Manar', 'Ali', 'Manar@123', balance_checking = -50)
        self.customer9 = Customer('9', 'Ghala', 'Ammar', 'Ghala@123', balance_checking = -80)

        # Account objects - for testing
        self.account1 = Account(self.customer1) # No accounts
        self.account2 = Account(self.customer2) # Only checking account
        self.account3 = Account(self.customer3) # Only savings account
        self.account4 = Account(self.customer4) # Both checking and savings accounts
        self.account5 = Account(self.customer5) # Low balance
        self.account6 = Account(self.customer6) # Deactive account
        # Account objects - for Overdraft testing 
        self.account7 = Account(self.customer7)  # test 1st overdraft
        self.account8 = Account(self.customer8)  # Negative balance
        self.account9 = Account(self.customer9)  # Negative balance

        # BankManagement objects - for testing transfers to other customers
        self.bank_management = BankManagement()
        # add customers in bank_management
        self.bank_management.customers = {
            '1': self.customer1,
            '2': self.customer2, 
            '3': self.customer3,
            '4': self.customer4,
            '5': self.customer5,
            '6': self.customer6,
            '7': self.customer7,
            '8': self.customer8,
            '9': self.customer9
        }

    # [2]. testing methods
    # --------------------------------------- Withdraw Tests ---------------------------------------
    def test_success_withdraw_checking(self):
        # [ Test 1 ] success withdraw from Checking Account
        # Use ( account2: Only checking account )
        success, message = self.account2.withdraw(100, "checking")
        self.assertTrue(success)
        self.assertIn("withdrawn from Checking Account", message)
        self.assertEqual(self.customer2.balance_checking, 100)
        success, message = self.account2.withdraw(100, "checking")

    def test_success_withdraw_savings(self):
        # [ Test 2 ] success withdraw from Savings Account
        # Use ( account3: Only savings account )
        success, message = self.account3.withdraw(500, "savings")
        self.assertTrue(success)
        self.assertIn("withdrawn from the Savings Account", message)
        self.assertEqual(self.customer3.balance_savings, 1000)

    def test_withdraw_amount_greater_than_checking(self):
        # [ Test 3 ] withdraw from Checking Account that the amount is greater than in checking account
        # Use ( account2: Only checking account )
        success, message = self.account2.withdraw(300, "checking") #here the resulting balance become (-100), so we can't withdraw greater than 300$.
        self.assertTrue(success)
        self.assertIn("Overdraft Fee", message)
        # initial balance = 200, it withdrawn 300 and decrease 35$, so 200 - 300 - 355 = -135
        self.assertEqual(self.customer2.balance_checking, -135)

    def test_withdraw_amount_greater_than_savings(self):
        # [ Test 4 ] withdraw from Checking Account that the amount is greater than in savings Account
        # Use ( account3: Only savings account )
        success, message = self.account3.withdraw(2000, "savings")
        self.assertFalse(success)
        self.assertIn("greater than the amount in your Savings Account", message)
        self.assertEqual(self.customer3.balance_savings, 1500)  # balance doesn't change

    def test_withdraw_no_checking_account(self):
        # [ Test 5 ] withdraw from Checking Account that does NOT exist
        # Use ( account1: No accounts )
        success, message = self.account1.withdraw(100, "checking")
        self.assertFalse(success)
        self.assertIn("do NOT have a Checking Account", message)

    def test_withdraw_no_savings_account(self):
        # [ Test 6 ] withdraw from Savings Account that does NOT exist
        # Use ( account1: No accounts )
        success, message = self.account1.withdraw(100, "savings")
        self.assertFalse(success)
        self.assertIn("do NOT have a Savings Account", message)

    def test_withdraw_invalid_account_type(self):
        # [ Test 7 ] withdraw from Invalid account type
        # Use ( account4: Both checking and savings accounts )
        success, message = self.account4.withdraw(100, "markit")
        self.assertFalse(success)
        self.assertIn("Invalid Account Type", message)

    def test_withdraw_zero_amount(self):
        # [ Test 8 ] withdraw zero amount
        # Use ( account2: Only checking account )
        success, message = self.account2.withdraw(0, "checking")
        self.assertFalse(success)
        self.assertIn("must be greater than zero", message)
        self.assertEqual(self.customer2.balance_checking, 200)

    def test_withdraw_negative_amount(self):
        # [ Test 9 ] withdraw negative amount
        # Use ( account2: Only checking account )
        success, message = self.account2.withdraw(-50, "checking")
        self.assertFalse(success)
        self.assertIn("must be greater than zero", message)
        self.assertEqual(self.customer2.balance_checking, 200)

    def test_withdraw_from_deactive_account(self):
        # [ Test 10 ] withdraw from Deactive account type
        # Use ( account6: Deactive account )
        success, message = self.account6.withdraw(100, "checking")
        self.assertFalse(success)
        self.assertIn("Account is Deactive", message)
        self.assertEqual(self.customer6.balance_checking, 1000)  # balance doesn't change
    
    # ------------- Overdraft Protection Tests -------------
    def test_first_overdraft_checking(self):
        # [ Test 11 ] first overdraft from Checking Account
        # Use ( account7 )
        initial_balance = self.customer7.balance_checking  # balance_checking = 50
        amount = 100  # withdraw greater than balance (less than -100)
        
        success, message = self.account7.withdraw(amount, "checking")
        
        self.assertTrue(success)
        self.assertIn("Overdraft Fee", message)
        self.assertIn("Overdraft Count: 1", message)
        
        # 50 - 100 - 35 = -85
        expected_balance = initial_balance - amount - self.customer7.overdraft_fee
        self.assertEqual(self.customer7.balance_checking, expected_balance)
        self.assertEqual(self.customer7.overdraft_count, 1)
        self.assertTrue(self.customer7.is_active)  # Account still Active

    def test_second_overdraft_deactivates_account(self):
        # [ Test 12 ] second overdraft deactivates the account
        # Use ( account7 )

        # - (1st overdraft)
        self.account7.withdraw(60, 'checking')  # overdraft_count = 1
        
        # - diposit money to be positive
        self.account7.deposit(100, 'checking')
        
        # - (2nd overdraft) (must Deactive the account)
        success, message = self.account7.withdraw(120, 'checking')
        self.assertTrue(success)
        self.assertIn("Account deactivated due to overdrafts", message)
        self.assertEqual(self.customer7.overdraft_count, 2)
        self.assertFalse(self.customer7.is_active)  # Account Deactivated

    def test_withdraw_from_negative_balance_within_limit(self):
        # [ Test 13 ] withdraw from negative balance within $100 limit
        # Use ( account8: Negative balance )
        initial_balance = self.customer8.balance_checking  # -50
        amount = 30  # within $100 limit

        
        success, message = self.account8.withdraw(amount, "checking")
        
        self.assertTrue(success)
        # expected_balance: -50 - 80 = -130 (no fees bs its already negative)
        expected_balance = initial_balance - amount
        self.assertEqual(self.customer8.balance_checking, expected_balance)

    def test_withdraw_from_negative_balance_exceed_limit(self):
        # [ Test 14 ] withdraw from negative balance exceeding $100 limit
        # Use ( account8: Negative balance )
        initial_balance = self.customer8.balance_checking  # -50
        amount = 90  # -50 - 90 = -140
        
        success, message = self.account8.withdraw(amount, "checking")
        
        self.assertFalse(success)
        self.assertIn("Resulting balance cannot be less than $-100", message)
        self.assertEqual(self.customer8.balance_checking, initial_balance)  # balance doesn't change

    def test_overdraft_fee_calculation(self):
        # [ Test 16 ] verify overdraft fee calculation
        # Use ( account7 )
        initial_balance = 100
        self.customer7.balance_checking = initial_balance
        amount = 150  # will overdraft
        
        success, message = self.account7.withdraw(amount, "checking")
        self.assertTrue(success)
        # 100 - 150 - 35 = -85
        expected_balance = initial_balance - amount - self.customer7.overdraft_fee
        self.assertEqual(self.customer7.balance_checking, expected_balance)

    def test_no_overdraft_on_savings_account(self):
        # [ Test 17 ] no overdraft protection on savings account
        # Use ( account3: Only savings account )
        initial_balance = self.customer3.balance_savings  # balance_savings = 1500
        amount = 2000  # No overdraft
        
        success, message = self.account3.withdraw(amount, "savings")
        
        self.assertFalse(success)
        self.assertIn("greater than the amount in your Savings Account", message)
        self.assertEqual(self.customer3.balance_savings, initial_balance)  # balance doesn't change

    # --------------------------------------- Deposit Tests ---------------------------------------
    def test_success_deposit_checking(self):
        # [ Test 9 ] success deposit to Checking Account
        # Use ( account2: Only checking account )
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
        # Use ( account3: Only savings account )
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
        # Use ( account1: No accounts )
        success, message = self.account1.deposit(100, "checking")
        
        self.assertFalse(success)
        self.assertIn("do NOT have a Checking Account", message)
        self.assertIsNone(self.customer1.balance_checking)  # balance_checking = None

    def test_deposit_no_savings_account(self):
        # [ Test 12 ] deposit to Savings Account that does NOT exist
        # Use ( account1: No accounts )
        success, message = self.account1.deposit(100, "savings")

        self.assertFalse(success)
        self.assertIn("do NOT have a Savings Account", message)
        self.assertIsNone(self.customer1.balance_savings)  # balance_savings = None

    def test_deposit_invalid_account_type(self):
        # [ Test 13 ] deposit to Invalid account type
        # Use ( account4: Both checking and savings accounts )
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
        # Use ( account2: Only checking account )
        initial_balance = self.customer2.balance_checking
        
        success, message = self.account2.deposit(0, "checking")
        self.assertFalse(success)
        self.assertIn("Deposit amount must be greater than zero", message)
        self.assertEqual(self.customer2.balance_checking, initial_balance)  # Verify balances didn't change

    def test_deposit_negative_amount(self):
        # [ Test 15 ] deposit negative amount (edge case)
        # Use ( account2: Only checking account )
        initial_balance = self.customer2.balance_checking
        
        success, message = self.account2.deposit(-250, "checking")
        self.assertFalse(success)
        self.assertIn("Deposit amount must be greater than zero", message)
        self.assertEqual(self.customer2.balance_checking, initial_balance)  # Verify balances didn't change

    def test_deposit_decimal_amount(self):
        # [ Test 16 ] deposit decimal amount
        # Use ( account2: Only checking account )
        initial_balance = self.customer2.balance_checking
        decimal_amount = 153.67
        expected_balance = initial_balance + decimal_amount
        
        success, message = self.account2.deposit(decimal_amount, "checking")
        self.assertTrue(success)
        self.assertIn("deposited to Checking Account", message)
        
        # Used `assertAlmostEqual()` instead of `assertEqual()` floating-point comparisons to avoid precision issues.
        self.assertAlmostEqual(self.customer2.balance_checking, expected_balance, places = 2)

    def test_deposit_multiple_times_checking(self):
        # [ Test 17 ] multiple deposits to Checking Account
        # Use ( account2: Only checking account )
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
    # ----- 1. Transfer money between customer's accounts -----
    def test_success_transfer_checking_to_savings(self):
        # [ Test 18 ] success transfer from Checking to Savings
        # Use ( account4: Both checking and savings accounts )
        initial_checking = self.customer4.balance_checking
        initial_savings = self.customer4.balance_savings
        transfer_amount = 500
        
        success, message = self.account4.transfer(transfer_amount, "checking", "savings")
        
        self.assertTrue(success)
        self.assertEqual(self.customer4.balance_checking, initial_checking - transfer_amount)
        self.assertEqual(self.customer4.balance_savings, initial_savings + transfer_amount)

    def test_success_transfer_savings_to_checking(self):
        # [ Test 19 ] success transfer from Savings to Checking
        # Use ( account4: Both checking and savings accounts )
        initial_checking = self.customer4.balance_checking
        initial_savings = self.customer4.balance_savings
        transfer_amount = 1000
        
        success, message = self.account4.transfer(transfer_amount, "savings", "checking")
        
        self.assertTrue(success)
        self.assertEqual(self.customer4.balance_checking, initial_checking + transfer_amount)
        self.assertEqual(self.customer4.balance_savings, initial_savings - transfer_amount)

    def test_transfer_amount_greater_than_checking(self):
        # [ Test 20 ] transfer from Checking to Savings with amount greater than checking
        # Use ( account5: Low balance)
        initial_checking = self.customer5.balance_checking
        initial_savings = self.customer5.balance_savings
        transfer_amount = 1000  # greater than (checking balance = 15$)
        
        success, message = self.account5.transfer(transfer_amount, "checking", "savings")
        
        self.assertFalse(success)
        self.assertEqual(self.customer5.balance_checking, initial_checking)  # balance doesn't change
        self.assertEqual(self.customer5.balance_savings, initial_savings)    # balance doesn't change

    def test_transfer_amount_greater_than_savings(self):
        # [ Test 21 ] transfer from Savings to Checking with amount greater than savings
        # Use ( account5: Low balance)
        initial_checking = self.customer5.balance_checking
        initial_savings = self.customer5.balance_savings
        transfer_amount = 100  # greater than (checking balance = 50$)
        
        success, message = self.account5.transfer(transfer_amount, "savings", "checking")
        
        self.assertFalse(success)
        self.assertEqual(self.customer5.balance_checking, initial_checking)  # balance doesn't change
        self.assertEqual(self.customer5.balance_savings, initial_savings)    # balance doesn't change

    # def test_transfer_no_checking_account(self):
    #     # [ Test 22 ] transfer from Checking account that does NOT exist
    #     # Use ( account3: Only savings account )
    #     success, message = self.account3.transfer(100, "checking", "savings")
    #     self.assertFalse(success)

    # def test_transfer_no_savings_account(self):
    #     # [ Test 23 ] transfer to Savings account that does NOT exist
    #     # Use ( account2: Only checking account )
    #     success, message = self.account2.transfer(100, "checking", "savings")
    #     self.assertFalse(success)

    def test_transfer_zero_amount(self):
        # [ Test 27 ] transfer zero amount
        # Use ( account4: Both checking and savings accounts )
        initial_checking = self.customer4.balance_checking
        success, message = self.account4.transfer(0, "checking", "savings")

        self.assertFalse(success)
        self.assertEqual(self.customer4.balance_checking, initial_checking)    # balance doesn't change

    def test_transfer_negative_amount(self):
        # [ Test 28 ] transfer negative amount
        # Use ( account4: Both checking and savings accounts )
        initial_checking = self.customer4.balance_checking
        success, message = self.account4.transfer(-100, "checking", "savings")
        
        self.assertFalse(success)
        self.assertEqual(self.customer4.balance_checking, initial_checking)     # balance doesn't change

    def test_transfer_decimal_amount(self):
        # [ Test 29 ] transfer decimal amount
        # Use ( account4: Both checking and savings accounts )
        initial_checking = self.customer4.balance_checking
        initial_savings = self.customer4.balance_savings
        transfer_amount = 250.50
        
        success, message = self.account4.transfer(transfer_amount, "checking", "savings")
        
        self.assertTrue(success)
        self.assertAlmostEqual(self.customer4.balance_checking, initial_checking - transfer_amount, places = 2)
        self.assertAlmostEqual(self.customer4.balance_savings, initial_savings + transfer_amount, places = 2)

    # ----- 2. Test Transfer money to another customer -----
    def test_success_transfer_from_checking_to_another_customer(self):
        # [ Test 30 ] success transfer from Checking to another customer
        # Use ( account4 ------> account2 )
        initial_sender_checking = self.customer4.balance_checking
        initial_recipient_checking = self.customer2.balance_checking
        transfer_amount = 500
        
        success, message = self.account4.transfer(transfer_amount, "checking", "checking", "2", self.bank_management)
        self.assertTrue(success)
        self.assertEqual(self.customer4.balance_checking, initial_sender_checking - transfer_amount)
        self.assertEqual(self.customer2.balance_checking, initial_recipient_checking + transfer_amount)

    def test_transfer_to_another_customer_insufficient_balance(self):
        # [ Test 31 ] transfer to another customer with insufficient balance
        # Use ( account5 ------> account2 )
        initial_sender_checking = self.customer5.balance_checking
        initial_recipient_checking = self.customer2.balance_checking
        transfer_amount = 100  # greater than account5 checking balance (15$)
        
        success, message = self.account5.transfer(transfer_amount, "checking", "checking", "2", self.bank_management)
        self.assertFalse(success)
        self.assertEqual(self.customer5.balance_checking, initial_sender_checking)  # balance doesn't change
        self.assertEqual(self.customer2.balance_checking, initial_recipient_checking)  # balance doesn't change

    def test_transfer_to_another_customer_not_found(self):
        # [ Test 32 ] transfer to non-existent customer
        # Use ( account4 ------> non-existent customer )
        initial_checking = self.customer4.balance_checking
        
        success, message = self.account4.transfer(500, "checking", "checking", "999", self.bank_management)
        self.assertFalse(success)
        self.assertEqual(self.customer4.balance_checking, initial_checking)  # balance doesn't change

    def test_transfer_to_another_customer_deactive(self):
        # [ Test 33 ] transfer to deactivated customer
        # Use ( account4 ------> account6 (deactive) )
        initial_checking = self.customer4.balance_checking
        
        success, message = self.account4.transfer(500, "checking", "checking", "6", self.bank_management)
        self.assertFalse(success)
        self.assertEqual(self.customer4.balance_checking, initial_checking)  # balance doesn't change

    def test_transfer_to_another_customer_create_recipient_account(self):
        # [ Test 34 ] transfer to customer without checking account (should create it)
        # Use ( account4 ------> account1 (no checking account) )
        initial_sender_checking = self.customer4.balance_checking
        
        success, message = self.account4.transfer(300, "checking", "checking", "1", self.bank_management)
        self.assertTrue(success)
        self.assertEqual(self.customer4.balance_checking, initial_sender_checking - 300)
        self.assertEqual(self.customer1.balance_checking, 300)  # account created with the amount
        self.assertTrue(self.customer1.has_checking_account())

    # [3]. close - (if i want run something after test)
    def tearDown(self):
        pass