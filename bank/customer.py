
# Learned 'Password validation' from `https://www.geeksforgeeks.org/python/password-validation-in-python/`
import re

class Customer:
    def __init__(self, account_id, first_name, last_name, password, balance_checking = None, balance_savings = None, is_active = True, overdraft_count = 0):
        self.account_id = account_id
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.balance_checking = float(balance_checking) if balance_checking is not None else None
        self.balance_savings = float(balance_savings) if balance_savings is not None else None
        self.is_active = bool(is_active)
        self.overdraft_count = int(overdraft_count)
        self.overdraft_fee = 35.00
        self.max_overdraft_limit = -100.00
        self.max_overdraft_withdrawal = 100.00

        # fix update `is_active` error
        if isinstance(is_active, str):
            self.is_active = is_active.lower() == 'true'
        else:
            self.is_active = bool(is_active)
        
        # fix update `overdraft_count` error
        try:
            self.overdraft_count = int(overdraft_count)
        except (ValueError, TypeError):
            self.overdraft_count = 0
    
    def __str__(self):
        temp_list = [
            self.account_id, 
            self.first_name, 
            self.last_name, 
            self.password, 
            str(self.balance_checking) if self.balance_checking is not None else "",
            str(self.balance_savings) if self.balance_savings is not None else "",
            str(self.is_active), 
            str(self.overdraft_count)
        ]
        return f'{temp_list}'
        
    def get_fullname(self):
        return f"{self.first_name} {self.last_name}"
    
    @staticmethod
    def is_equal_password(password, confirm_password):
        return password == confirm_password
    
    def is_valid_password(self):
        password = self.password
        
        # Validates a password with criteria:
        # length 8-15 char
        if not (8 <= len(password) <= 15):
            print("⚠️ \033[1mPassword is NOT valid!⚠️ \033[0m, Must be between 8 and 15 characters long!\n")
            return False

        # At least one uppercase letter
        if not re.search(r"[A-Z]", password):
            print("⚠️ \033[1mPassword is NOT valid!⚠️ \033[0m, Must contain at least one uppercase letter!\n")
            return False

        # At least one lowercase letter
        if not re.search(r"[a-z]", password):
            print("⚠️ \033[1mPassword is NOT valid!⚠️ \033[0m, Must contain at least one lowercase letter!\n")
            return False

        # At least one digit
        if not re.search(r"\d", password):
            print("⚠️ \033[1mPassword is NOT valid!⚠️ \033[0m, Must contain at least one digit!\n")
            return False

        # At least one special char from !@#$%^&*()
        if not re.search(r"[!@#$%^&*()]", password):
            print("⚠️ \033[1mPassword is NOT valid!⚠️ \033[0m, Must contain at least one special character (!@#$%^&*())!\n")
            return False

        # No spaces
        if re.search(r"\s", password):
            print("⚠️ \033[1mPassword is NOT valid!⚠️ \033[0m, Cannot contain spaces!\n")
            return False

        return True # password is valid :)
    
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
    
    def to_customer_object(customer_list):
        
        checking = customer_list[4] if customer_list[4] not in [None, ""] else None
        savings = customer_list[5] if customer_list[5] not in [None, ""] else None
        
        # update `is_active`
        is_active = True  # default
        if len(customer_list) > 6 and customer_list[6] not in [None, ""]:
            is_active = customer_list[6].lower() == 'true'
        
        # update `overdraft_count`
        overdraft_count = 0  # default
        if len(customer_list) > 7 and customer_list[7] not in [None, ""]:
            try:
                overdraft_count = int(customer_list[7])
            except ValueError:
                overdraft_count = 0
        
        return Customer(
            customer_list[0],  # id
            customer_list[1],  # first name
            customer_list[2],  # last name
            customer_list[3],  # password
            checking,          # balance checking
            savings,           # balance savings
            is_active,         # active or not?
            overdraft_count    # overdraft count
        )