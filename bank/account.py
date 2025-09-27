# from bank.bank_management import BankManagement
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
            
            # withdraw the amount from checking account
            self.customer.balance_checking -= amount
            return True, f"✅ The amount of {amount}$ was withdrawn from the Checking Account 💸.\n💳 Current Checking Account Balance: {self.customer.balance_checking}$ 💳"
        
        # ---------- 2. WITHDRAW FROM SAVINGS ACCOUNT ----------
        elif account_type == "savings":
            # if the customer doesn't have a savings account
            if not self.customer.has_savings_account():
                return False, "⚠️ You do NOT have a Savings Account!"
            
            # if the amount greater than in savings account
            if self.customer.balance_savings < amount:
                return False, "⚠️ The amount to be withdrawn is greater than the amount in your Savings Account!"
            
            # withdraw the amount from savings account
            self.customer.balance_savings -= amount
            return True, f"✅ The amount of {amount}$ was withdrawn from the Savings Account 💸.\n💳 Current Savings Account Balance: {self.customer.balance_savings}$ 💳"
        
        return False, "⚠️ Invalid Account Type!"
    
    def deposit(self, amount, account_type):
        # if the amount less than or equal to 0
        if amount <= 0:
            return False, "⚠️ Deposit amount must be greater than zero!"

        # ---------- 1. DEPOSIT INTO CHECKING ACCOUNT ----------
        if account_type == "checking":
            # if the customer doesn't have a checking account
            if not self.customer.has_checking_account():
                return False, "⚠️ You do NOT have a Checking Account!"
            
            # deposit the amount into checking account
            self.customer.balance_checking += amount
            return True, f"✅ ${amount} has been deposited to Checking Account 💰.\n💳 Current Checking Account Balance: {self.customer.balance_checking}$ 💳"
        
        # ---------- 2. DEPOSIT INTO SAVINGS ACCOUNT ----------
        elif account_type == "savings":
            # if the customer doesn't have a savings account
            if not self.customer.has_savings_account():
                return False, "⚠️ You do NOT have a Savings Account!"
            
            # deposit the amount into savings account
            self.customer.balance_savings += amount
            return True, f"✅ ${amount} has been deposited to Savings Account 💰.\n💳 Current Savings Account Balance: {self.customer.balance_savings}$ 💳"

        return False, "⚠️ Invalid Account Type!"
    
    def transfer(self, amount, from_account, to_account, receiving_customer_ID = None, bank_management = None):
        # if the amount less than or equal to 0
        if amount <= 0:
            return False, "⚠️ Transfer amount must be greater than zero!"
        
        # -------------------- 1. Transfer money between my accounts --------------------
        if receiving_customer_ID is None:

            # Transfer from Checking to Savings
            if from_account == "checking" and to_account == "savings":
                
                # if the amount to transfer greater than in `balance_checking`
                if self.customer.balance_checking < amount:
                    return False, "⚠️ The amount to be transfer is greater than the amount in your Checking Account!"
                
                # Decrease money from Checking, and Increase money in Savings
                self.customer.balance_checking -= amount
                self.customer.balance_savings += amount
                return True, f"✅ ${amount} has been transferred from Checking to Savings.\n💳 Current Checking Account Balance: {self.customer.balance_checking}$\n💳 Current Savings Account Balance: {self.customer.balance_savings}$ 💳"
            
            # Transfer from Savings to Checking
            elif from_account == "savings" and to_account == "checking":
                
                # if the amount to transfer greater than in `balance_savings`
                if self.customer.balance_savings < amount:
                    return False, "⚠️ The amount to be transfer is greater than the amount in your Savings Account!"
                
                # Decrease money from Savings, and Increase money in Checking
                self.customer.balance_savings -= amount
                self.customer.balance_checking += amount
                return True, f"✅ ${amount} has been transferred from Savings to Checking.\n💳 Current Checking Account Balance: {self.customer.balance_checking}$\n💳 Current Savings Account Balance: {self.customer.balance_savings}$ 💳"
            
        
        # -------------------- 2. Transfer money to another customer --------------------
        elif receiving_customer_ID is not None:
            # Check the existence of the account
            if from_account == "checking" and not self.customer.has_checking_account():
                return False, "⚠️ You do NOT have a Checking Account!"
            
            if from_account == "savings" and not self.customer.has_savings_account():
                return False, "⚠️ You do NOT have a Savings Account!"
            
            # Check if the amount to be transfer is greater than in Account or not
            if from_account == "checking" and self.customer.balance_checking < amount:
                return False, "⚠️ The amount to be transfer is greater than the amount in your Checking Account!"
            
            if from_account == "savings" and self.customer.balance_savings < amount:
                return False, "⚠️ The amount to be transfer is greater than the amount in your Savings Account!"
            
            # search recipient customer by id
            recipient_customer = bank_management.search_customer(receiving_customer_ID)
            if not recipient_customer:
                return False, "⚠️ Recipient customer not found!"
            
            if not recipient_customer.is_active:
                return False, "⚠️ Recipient account is deactivated!"
            
            # Transfer from `from_account` to `recipient_customer`
            # - Decrease money from current customer account
            if from_account == "checking":
                current_balanca = self.customer.balance_checking
                self.customer.balance_checking -= amount
            else:
                current_balanca = self.customer.balance_savings
                self.customer.balance_savings -= amount
            
            # - Increase money in `recipient_customer`'s checking account
            if recipient_customer.has_checking_account():
                recipient_customer.balance_checking += amount
            else:
                # if he does NOT has checking account, Now it will created and increased by the amount
                recipient_customer.balance_checking = amount
            
            return True, f"✅ ${amount} has been transferred from your {from_account.capitalize()} account to Customer 🌟 {recipient_customer.get_fullname()} | with ID:{receiving_customer_ID} 🌟\n\n💳 Current {from_account.capitalize()} Account Balance: {current_balanca}$ 💳"
        
        return False, "⚠️ Invalid transfer operation!"
    
    def get_balance(self, account_type):
        if  self.customer.has_checking_account() and account_type == "checking":
            return self.customer.balance_checking

        elif self.customer.has_savings_account() and account_type == "savings":
            return self.customer.balance_savings

        return None