class Account:
    def __init__(self, customer):
        self.customer = customer
    
    def withdraw(self, amount, account_type):
        pass
    
    def deposit(self, amount, account_type):
        pass
    
    def transfer(self):
        pass
    
    def get_balance(self, account_type):
        if  self.customer.has_checking_account() and account_type == "checking":
            return self.customer.balance_checking

        elif self.customer.has_savings_account() and account_type == "savings":
            return self.customer.balance_savings
            
        return None