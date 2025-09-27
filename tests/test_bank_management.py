import unittest
from bank.bank_management import BankManagement
from bank.customer import Customer
from bank.account import Account
class TestBankManagement(unittest.TestCase):

    # [1]. open - (if i want run something before test)
    def setUp(self):
        # Customer objects - for testing
        self.customer1 = Customer('1', 'Salma', 'Yosuf', 'Salma@12345')
        self.customer2 = Customer('2', 'Alaa', 'Faisal', 'Alaa@1234', balance_checking = 200)
        self.customer3 = Customer('3', 'Hala', 'Saad', 'Hala@1234', balance_savings = 1500)

        # Account objects - for testing
        self.account1 = Account(self.customer1) # 
        self.account2 = Account(self.customer2) # 
        self.account3 = Account(self.customer3) # 

        # BankManagement objects - for testing transfers to other customers
        self.bank_management = BankManagement()
        # add customers in bank_management
        self.bank_management.customers = {
            '1': self.customer1,
            '2': self.customer2, 
            '3': self.customer3,
        }

    # [2]. testing methods
    def test_customer_exists(self):
        # Test checking if customer exists
        self.assertTrue(self.bank_management.customer_exists('2'))
        self.assertFalse(self.bank_management.customer_exists('999'))

    def test_search_customer(self):
        # Test searching for customer by ID
        customer = self.bank_management.search_customer('3')
        self.assertIsNotNone(customer)
        self.assertEqual(customer.account_id, '3')

    def test_get_account_info_card(self):
        # Test getting customer account information
        info = self.bank_management.get_account_info_card(self.customer2)
        self.assertIn("Alaa", info)
        self.assertIn("Faisal", info)

    def test_create_customer_account(self):
        # Test creating account for customer
        account = self.bank_management.create_customer_account(self.customer1)
        self.assertEqual(account.customer.account_id, self.customer1.account_id)

    def test_refresh_customers(self):
        # Test refreshing customers data from CSV
        original_count = len(self.bank_management.customers) + 1 #add the header row
        self.bank_management.refresh_customers()
        self.assertEqual(len(self.bank_management.customers), original_count)

    def test_update_customer(self):
        # Test updating customer information
        self.customer1.first_name = "Muna"
        self.bank_management.update_customer(self.customer1)
        updated_customer = self.bank_management.search_customer('1')
        self.assertEqual(updated_customer.first_name, "Muna")

    def test_login(self):
        # Test customer login functionality
        customer = self.bank_management.login('2', 'Alaa@1234')
        self.assertIsNotNone(customer)
        self.assertEqual(customer.account_id, '2')

    def test_get_all_customers(self):
        # Test get all customers from bank management
        customers = self.bank_management.get_all_customers()
        self.assertIsInstance(customers, dict)

    def test_add_new_customer(self):
        # Test adding a new customer
        new_id = self.bank_management.add_new_customer("Yara", "Mosa", "Yara@1234", "1", 150)
        self.assertIsNotNone(new_id)

    def test_save_all_customers(self):
        # Test saving all customers to CSV
        success = self.bank_management.save_all_customers()
        self.assertTrue(success)

    def test_verify_save(self):
        # Test verification of saved data
        try:
            self.bank_management.verify_save()
            success = True
        except Exception:
            success = False
        self.assertTrue(success)
    
    # [3]. close - (if i want run something after test)
    def tearDown(self):
        pass