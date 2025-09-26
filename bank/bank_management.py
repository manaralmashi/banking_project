import csv_bank

from bank.customer import Customer
from bank.account import Account

class BankManagement:
    
    def __init__(self):
        self.customers = self.get_all_customers()
    
    def get_all_customers(self):
        customers_info = csv_bank.get_customers_from_csv()
        
        # create customers 'DICT' for faster search instead of 'LIST'
        customers = {} 
        for info in customers_info[1: ]: # start from `index 1` (bc `index 0` in is the header in csv file)
            customer = Customer.to_customer_object(info)
            customers[customer.account_id] = customer
        return customers
    
    def save_all_customers(self):
        customers_info_list = []

        # - take every customer and put it in `customers_info_list`
        for customer in self.customers.values():
            customer_info = customer.to_customer_list() # convert from  `DICT` to `LIST`
            customers_info_list.append(customer_info) # add (the small Customer list) to (the big Customers list)

        # - save all customers data on csv
        csv_bank.save_customers_to_csv(customers_info_list)
    
    def add_new_customer(self, first_name, last_name, password, account_type_choice, initial_deposit_checking = 0, initial_deposit_savings = 0):
        new_customer_id = 2025000 + len(self.customers) + 1
        
        # defined the checking_balance and savings_balance based on user selection
        checking_balance = None
        savings_balance = None
        
        if account_type_choice == "1":  # Only Checking
            checking_balance = initial_deposit_checking
            # savings_balance = None
        elif account_type_choice == "2":  # Only Savings
            # checking_balance = None
            savings_balance = initial_deposit_savings
        elif account_type_choice == "3":  # Both Checking and Savings
            checking_balance = initial_deposit_checking
            savings_balance = initial_deposit_savings
        
        new_customer = Customer(new_customer_id, first_name, last_name, password, checking_balance, savings_balance)
        
        # add the customer to the customers dict
        self.customers[new_customer_id] = new_customer
        self.save_all_customers()

        # redownload data from csv file
        self.customers = self.get_all_customers()

        return new_customer_id
    
    def create_customer_account(self, customer_object):
        new_account = Account(customer_object)
        return new_account

    def login(self, account_id, password):
        customer = self.customers.get(account_id)
        if customer and customer.is_valid_password() and customer.password == password and customer.is_active:
            return customer
        # elif not customer:
        #     # redownload data from csv file
        #     self.customers = self.get_all_customers() 
        #     customer = self.customers.get(account_id)
        return None
    
    # May use it later
    def search_customer(self, account_id):
        return csv_bank.search_customer_by_id(account_id, self.customers)
    
    # May use it later in main.py to show the account info
    def get_customer_accounts_info(self, customer):
        info = f"\n-----------------📉 Account Info 📉-----------------\n"
        info += f"🔹 Customer Name: {customer.first_name} {customer.last_name}\n"
        info += f"🔹 Account ID   : {customer.account_id}\n"
        
        if customer.has_checking_account():
            info += f"🔹 Checking Account: {customer.balance_checking}$\n"
        else:
            info += f"🔹 Checking Account: None\n"
        
        if customer.has_savings_account():
            info += f"🔹 Savings Account: {customer.balance_savings}$\n"
        else:
            info += f"🔹 Savings Account: None\n"
        
        info += f"🔹 Account: {'Active' if customer.is_active else 'Deactive'}\n"
        return info