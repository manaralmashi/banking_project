import csv_bank

from bank.bank_management import BankManagement
from bank.customer import Customer

bank_management = BankManagement()

while True:
    # Learn (print bold text) from `https://www.reddit.com/r/learnpython/comments/mxhxgm/how_do_i_print_bold_text/`
    print('\n \033[1m-----------------------------------------------------------\033[0m')
    print('|               💸🏦 \033[1mWelcome To ACME Bank\033[0m 🏦💸              |')
    print(' \033[1m-----------------------------------------------------------\033[0m')
    print('[1] Add New Customer')
    print('[2] Log In')
    print('[3] Exit')
    print(' -------------------------------------------------')
    user_choice = input('Enter your choice (1-3): ')
    
    match user_choice:
        # [1] Add New Customer
        case '1':
            print('\n -----------(👤 Create New Customer 👤)-----------')
            
            # --[ 1. Ask the FullName ]--
            while True:
                first_name = input('- Enter First Name: ').strip().capitalize()
                last_name = input('- Enter Last Name: ').strip().capitalize()
                
                # name validation
                if first_name.replace(" ", "").isalpha() and last_name.replace(" ", "").isalpha():
                    break
                else:
                    print('⚠️ Sorry, you have to write your name with only letters!')
            
            # --[ 2. Ask the Password ]--
            while True:
                # password validation
                password = input('- Enter Password (8-15 chars, with upper/lower/digit/special): ')
                temp_customer = Customer('temp', 'temp', 'temp', password)
                
                is_valid_password = temp_customer.is_valid_password()
                if is_valid_password:
                    # -[ 3. Ask for Confirm password ]-
                    while True:
                        confirm_password = input('- Confirm Password: ')
                        if Customer.is_equal_password(password, confirm_password):
                            break
                        else:
                            print("⚠️ Passwords DON'T match! Try again..")
                    break
    
        # [2] Log In
        case '2':
            pass
        
        # [3] Exit
        case '3':
            print('\n \033[1m-----------------------------------------------------------\033[0m')
            print('|           💸🏦 \033[1mThank you for use ACME Bank\033[0m 🏦💸           |')
            print(' \033[1m-----------------------------------------------------------\033[0m')
            break
        
        # [_] Default case
        case _:
            print('⚠️ \033[1mInvalid Choice!\033[0m Try again.')