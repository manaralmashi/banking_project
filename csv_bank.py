import csv

# take 'id', return (row) 'list of customer info'
def search_customer_by_id(account_id, customers):
    for customer in customers:
        if customer[0] == str(account_id):  # 1st column is account_id
            return customer
    return None

# to add and update entire csv file
def save_customers_to_csv(customers_info_list, filename = "bank.csv"):
    headers = ['account_id', 'first_name', 'last_name', 'password', 'balance_checking', 'balance_savings', 'is_active', 'overdraft_count']
    
    try:
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(customers_info_list)
        return True
    except Exception as e:
        print(f"⚠️ DEBUG CSV: Error saving file: {e}")
        return False

# to add only new row
def add_customer_to_csv(customer_info, filename = "bank.csv"):
    with open(filename, 'a', newline = '') as file:
        writer = csv.writer(file)
        writer.writerow(customer_info)

# return list of customers
def get_customers_from_csv(filename = "bank.csv"):
    try:
        with open(filename, 'r', newline = '') as file:
            reader = csv.reader(file)
            
            # 1st way (with for loop) -> preferred bs it's quick to understand:
            customers = []
            for row in reader:
                if row: # return without empty rows
                    customers.append(row)
            return customers

            # 2nd way (shorter):
            # return [row for row in reader if row]

    except FileNotFoundError:
        return []  # return empty [] if the file doesn't exist