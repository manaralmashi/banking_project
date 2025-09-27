import csv_bank

from bank.customer import Customer
from bank.account import Account

class BankManagement:
    
    def __init__(self):
        self.customers = self.get_all_customers()
    
    def get_all_customers(self):
        customers_info = csv_bank.get_customers_from_csv()
        
        if not customers_info:
            print("⚠️ DEBUG: No customers found in CSV file")
            return {}
        
        # print(f"DEBUG: Reading {len(customers_info)} rows from CSV") #--> for testing
        
        # create customers 'DICT' for faster search instead of 'LIST'
        customers = {} 
        # valid_count = 0 #--> for testing
        
        # start `customers_info` from index 1 (bc index 0 is the header)
        for i, info in enumerate(customers_info[1:], 1):
            if not info or len(info) < 4:
                # print(f"⚠️ DEBUG: Skipping invalid row {i}") #--> for testing
                continue
                
            try:
                customer = Customer.to_customer_object(info)
                # print(f"DEBUG: Row {i} → ID: {customer.account_id}, Active: {customer.is_active}") #--> for testing
                
                # add customer obj to the big customers `dict`
                customers[customer.account_id] = customer
                # valid_count += 1 #--> for testing
                
            except Exception as e:
                print(f"⚠️ DEBUG: Error in row {i}: {e}")
        
        # print(f"DEBUG: Loaded {valid_count} valid customers") #--> for testing
        return customers
    
    def save_all_customers(self):
        try:
            if not self.customers:
                print("⚠️ No customers data to save")
                return False
            
            customers_info_list = []
            # print(f"Preparing to save {len(self.customers)} customers...") #--> for testing
            
            # - take every customer and put it in `customers_info_list`
            for customer_id, customer in self.customers.items():
                customer_info = customer.to_customer_list() # convert from  `DICT` to `LIST`
                # print(f"Customer {customer_id}: active={customer.is_active}, balance={customer.balance_checking}") #--> for testing
                customers_info_list.append(customer_info) # add (the small Customer list) to (the big Customers list)
            
            # - save all customers data on csv
            success = csv_bank.save_customers_to_csv(customers_info_list)
            
            if success:
                # print("✅ Customers saved successfully!") #--> for testing
                self.verify_save()
            else:
                print("⚠️ Failed to save customers")
                
            return success
            
        except Exception as e:
            print(f"⚠️ Error in save_all_customers: {e}")
            return False

    def verify_save(self):
        try:
            saved_customers = csv_bank.get_customers_from_csv()
            # print(f"Verification: {len(saved_customers)} rows in CSV file") #--> for testing
            
            # for i, customer_data in enumerate(saved_customers):
            #     print(f"CSV Row {i}: {customer_data}") #--> for testing
                
        except Exception as e:
            print(f"⚠️ Verification failed: {e}")
    
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
        # update CSV file
        self.refresh_customers()
        
        # ✅ search on updated data
        customer = self.search_customer(account_id)
        if customer and customer.password == password:
            return customer
        return None
    
    def refresh_customers(self):
        # update CSV file: redownload data from csv
        self.customers = self.get_all_customers()

        # print(f"🔄 Refreshed {len(self.customers)} customers from CSV") #--> for testing
    
    def update_customer(self, customer):
        # convert ID to string
        account_id = str(customer.account_id)
        if account_id in self.customers:
            self.customers[account_id] = customer
            self.save_all_customers()
            # print(f"✅ Updated customer {account_id} in memory and CSV") #--> for testing
        else:
            print(f"⚠️ Customer {account_id} not found for update")

    def search_customer(self, account_id):
        # return csv_bank.search_customer_by_id(account_id, self.customers)
        account_id_str = str(account_id)
        return self.customers.get(account_id_str)
    
    def customer_exists(self, account_id):
        return str(account_id) in self.customers
    
    # Display Account Info Card
    def get_account_info_card(self, customer):
                                    account_info_display = f"""
                                    \033[34m\033[1m _________________________________________________\033[0m\033[0m
                                    \033[34m\033[1m|                                                 |\033[0m\033[0m
                                    \033[34m\033[1m|\033[0m\033[0m          📊 \033[1mACME BANK ACCOUNT INFO\033[0m 📊         \033[34m\033[1m|\033[0m\033[0m
                                    \033[34m\033[1m|_________________________________________________|\033[0m\033[0m\n
                                            🔹 Customer Name : {customer.get_fullname()}  
                                            🔹 Account ID:   {customer.account_id}  
                                            🔹 Account Status:   {'🟢 ACTIVE 🟢' if customer.is_active else '🔴 DEACTIVATED 🔴'}  
                                    \033[34m\033[1m_________________________________________________\033[0m\033[0m \n"""

                                    if customer.has_checking_account():
                                        account_info_display += f"""
                                            💳 Checking Account: ${customer.balance_checking}"""
                                    else:
                                        account_info_display += f"""
                                            💳 Checking Account: NOT AVAILABLE
                                                🔄 Open from (Deposit Menu) If You Want!"""

                                    if customer.has_savings_account():
                                        account_info_display += f"""
                                            💳 Savings Account:  ${customer.balance_savings}"""
                                    else:
                                        account_info_display += f"""
                                            💳 Savings Account:  NOT AVAILABLE
                                                🔄 Open from (Deposit Menu) If You Want!"""

                                    # Add total balance if both accounts exist
                                    if customer.has_checking_account() and customer.has_savings_account():
                                        total_balance = (customer.balance_checking or 0) + (customer.balance_savings or 0)
                                        account_info_display += f"""
                                    \033[34m\033[1m_________________________________________________\033[0m\033[0m \n
                                            🔷 \033[1mTotal Balance\033[0m:   ${total_balance}"""

                                    # Add overdraft information
                                    account_info_display += f"""
                                    \033[34m\033[1m_________________________________________________\033[0m\033[0m \n
                                            ⚠️  \033[1mOverdraft Protection\033[0m:
                                                🔻 Overdraft Count: {customer.overdraft_count}
                                                🔻 Fee per Overdraft: ${customer.overdraft_fee}
                                                🔻 Max Overdraft Limit: ${customer.max_overdraft_limit}"""
                                    if customer.has_checking_account() and customer.balance_checking < 0:
                                         account_info_display += f"""
                                                🔻 Max Overdraft Limit: ${customer.max_overdraft_limit}"""

                                    account_info_display += """
                                    \033[34m\033[1m_________________________________________________\033[0m\033[0m"""
                                    
                                    return account_info_display