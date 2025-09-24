import unittest
from bank.customer import Customer
class TestCustomer(unittest.TestCase):

    # [1]. open - (if i want run something before test)
    def setUp(self):
        # print('-------- setUp --------') # for testing
        self.customer1 = Customer('7654', 'Manar', 'Saad', 'Mnr@1')
        self.customer2 = Customer('7655', 'Manar', 'Saad', 'manar@12345')
        self.customer3 = Customer('7656', 'Manar', 'Saad', 'Manar@saad')
        self.customer4 = Customer('7657', 'Manar', 'Saad', 'Manar12345')
        self.customer5 = Customer('7658', 'Manar', 'Saad', 'Manar Saad')
        self.customer6 = Customer('7659', 'Manar', 'Saad', 'Manar@12345')

    # [2]. testing methods
    def test_is_valid_password(self):
        # print('-------- on test_is_valid_password()--------') # for testing
        self.assertEqual(self.customer1.is_valid_password(), False)  # "⚠️ Password must be between 8 and 15 characters long!"
        self.assertEqual(self.customer2.is_valid_password(), False)  # "⚠️ Password must contain at least one uppercase letter!"
        self.assertEqual(self.customer3.is_valid_password(), False)  # "⚠️ Password must contain at least one digit!"
        self.assertEqual(self.customer4.is_valid_password(), False)  # "⚠️ Password must contain at least one special character (!@#$%^&*())!"
        self.assertEqual(self.customer5.is_valid_password(), False)  # "⚠️ Password cannot contain spaces!"
        self.assertEqual(self.customer6.is_valid_password(), True)   # Password is valid :)

    # [3]. close - (if i want run something after test)
    def tearDown(self):
        pass