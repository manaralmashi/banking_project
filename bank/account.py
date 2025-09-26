class Account:
    def __init__(self, customer):
        self.customer = customer
    
    def withdraw(self, amount, account_type):
        # if the account is Deactive
        if not self.customer.is_active:
            return False, "⚠️ The Account is Deactive ⚠️"
        
        # ---------- 1. WITHDRAW FROM CHECKING ACCOUNT ----------
        if account_type == "checking":
            # if the customer doesn't have a checking account
            if not self.customer.has_checking_account():
                return False, "⚠️ You do NOT have a Checking Account!"
            
            # if the amount greater than in checking account
            if self.customer.balance_checking < amount:
                return False, "⚠️ The amount to be withdrawn is greater than the amount in your Checking Account!"
            
            # withdraw tme amount from checking account
            self.customer.balance_checking -= amount
            return True, f"✅ The amount of {amount}$ was withdrawn from the Checking Account 💸.\n💳 Current Checking Account Balance: {self.customer.balance_checking}$"
        
        # ---------- 2. WITHDRAW FROM SAVINGS ACCOUNT ----------
        elif account_type == "savings":
            # if the customer doesn't have a savings account
            if not self.customer.has_savings_account():
                return False, "⚠️ You do NOT have a Savings Account!"
            
            # if the amount greater than in savings account
            if self.customer.balance_savings < amount:
                return False, "⚠️ The amount to be withdrawn is greater than the amount in your Savings Account!"
            
            # withdraw tme amount from savings account
            self.customer.balance_savings -= amount
            return True, f"✅ The amount of {amount}$ was withdrawn from the Savings Account 💸.\n💳 Current Savings Account Balance: {self.customer.savings_checking}$"
        
        return False, "⚠️ Invalid Account Type!"
    
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