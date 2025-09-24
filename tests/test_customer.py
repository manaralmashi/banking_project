import unittest
from bank.customer import Customer
class TestCustomer(unittest.TestCase):

    # [1]. open - (if i want run something before test)
    def setUp(self):
        # print('-------- setUp --------') # for testing
        # objects for testing
        self.customer1 = Customer('1', 'Manar', 'Saad', 'Mnr@1')
        self.customer2 = Customer('2', 'amal', 'ali', 'amal@12345')
        self.customer3 = Customer('3', 'Fatima', 'Noor', 'Fatima@noor')
        self.customer4 = Customer('4', 'Ahmed', 'Talal', 'Ahmed12345')
        self.customer5 = Customer('5', 'Jana', 'khaled', 'Jana khaled')
        self.customer6 = Customer('6', 'Salma', 'Yosuf', 'Salma@12345')
        
        self.customer_with_checking = Customer('7', 'Alaa', 'Faisal', 'Alaa@1234', balance_checking = 200)
        self.customer_with_savings = Customer('8', 'Hala', 'Saad', 'Hala@1234', balance_savings = 1500)
        self.customer_with_both = Customer('9', 'Hasan', 'Yaser', 'Hasan@1234', balance_checking = 3000, balance_savings = 5000)
        self.customer_with_none = Customer('10', 'Muna', 'Saif', 'Muna@1234')
        
    # [2]. testing methods
    def test_is_valid_password(self):
        # print('-------- on test_is_valid_password()--------') # for testing
        self.assertEqual(self.customer1.is_valid_password(), False)  # "⚠️ Password must be between 8 and 15 characters long!"
        self.assertEqual(self.customer2.is_valid_password(), False)  # "⚠️ Password must contain at least one uppercase letter!"
        self.assertEqual(self.customer3.is_valid_password(), False)  # "⚠️ Password must contain at least one digit!"
        self.assertEqual(self.customer4.is_valid_password(), False)  # "⚠️ Password must contain at least one special character (!@#$%^&*())!"
        self.assertEqual(self.customer5.is_valid_password(), False)  # "⚠️ Password cannot contain spaces!"
        self.assertEqual(self.customer6.is_valid_password(), True)   # Password is valid :)

    def test_get_fullname(self):
        self.assertEqual(self.customer1.get_fullname(), "Manar Saad")
        self.assertEqual(self.customer2.get_fullname(), "amal ali")
        self.assertEqual(self.customer3.get_fullname(), "Fatima Noor")
        
    def test_is_equal_password(self):
        self.assertTrue(Customer.is_equal_password("Hala@1234", "Hala@1234")) # True
        self.assertTrue(Customer.is_equal_password("", "")) # True
        self.assertFalse(Customer.is_equal_password("Manar@123", "Maanr@123")) # False
        self.assertFalse(Customer.is_equal_password("Saad$12345", "saad$12345")) # False
        
    def test_has_checking_account(self):
        self.assertTrue(self.customer_with_checking.has_checking_account()) # True
        self.assertFalse(self.customer_with_savings.has_checking_account()) # False
        self.assertTrue(self.customer_with_both.has_checking_account()) # True
        self.assertFalse(self.customer_with_none.has_checking_account()) # False

    def test_has_savings_account(self):
        self.assertFalse(self.customer_with_checking.has_savings_account()) # False
        self.assertTrue(self.customer_with_savings.has_savings_account()) # True
        self.assertTrue(self.customer_with_both.has_savings_account()) # True
        self.assertFalse(self.customer_with_none.has_savings_account()) # False
        
    # [3]. close - (if i want run something after test)
    def tearDown(self):
        pass