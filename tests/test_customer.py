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
        
    # [3]. close - (if i want run something after test)
    def tearDown(self):
        pass