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
    def test_withdraw(self):
        pass

    def test_deposit(self):
        pass
        
    def test_transfer(self):
        pass
        
    # [3]. close - (if i want run something after test)
    def tearDown(self):
        pass