
# Learned 'Password validation' from `https://www.geeksforgeeks.org/python/password-validation-in-python/`
import re

class Customer:
    def __init__(self, account_id, first_name, last_name, password, balance_checking=0, balance_savings=0, is_active=True, overdraft_count=0):
        self.account_id = account_id
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.balance_checking = float(balance_checking) if balance_checking is not None else None
        self.balance_savings = float(balance_savings) if balance_savings is not None else None
        self.is_active = bool(is_active)
        self.overdraft_count = int(overdraft_count)
    
    def get_fullname(self):
        return f"{self.first_name} {self.last_name}"
    
    def is_equal_password(self, input_password):
        return self.password == input_password
    
    def has_checking_account(self):
        return self.balance_checking is not None
    
    def has_savings_account(self):
        return self.balance_savings is not None
    
    def to_customer_list(self):
        return [
            self.account_id, 
            self.first_name, 
            self.last_name, 
            self.password, 
            str(self.balance_checking) if self.balance_checking is not None else "",
            str(self.balance_savings) if self.balance_savings is not None else "",
            str(self.is_active), 
            str(self.overdraft_count)
        ]
    
    @classmethod
    def to_customer_object(customer_list):
        
        checking = customer_list[4] if customer_list[4] not in [None, ""] else None
        savings = customer_list[5] if customer_list[5] not in [None, ""] else None
        
        return Customer(
            customer_list[0],  # id
            customer_list[1],  # first name
            customer_list[2],  # last name
            customer_list[3],  # password
            checking,          # balance checking
            savings,           # balance savings
            customer_list[6],  # active or not?
            customer_list[7]   # overdraft count
        
            # customer_list[6] if len(customer_list) > 6 else True,
            # customer_list[7] if len(customer_list) > 7 else 0
        )