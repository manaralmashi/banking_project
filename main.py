import sys      # needed for sys.exit()
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
    print('[0] Exit')
    print(' -------------------------------------------------')
    user_choice_main = input('Enter Your Choice Number (0-2): ')
    
    match user_choice_main:
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
                
            # --[ 4. Select Account Type ]--
            print('\n- Select Account Type:')
            print('[1] Just Open a \033[1mChecking\033[0m Account')
            print('[2] Just Open a \033[1mSavings\033[0m Account') 
            print('[3] Open Both a \033[1mSavings\033[0m and a \033[1mChecking\033[0m Account')
            
            while True:
                account_type_choice = input('Enter Account Type you want to open (1-3): ')
                # validate choice
                if account_type_choice in ['1', '2', '3']:
                    break
                print('⚠️ \033[1mInvalid Choice!\033[0m Try again.')
            
            # --[ 5. Initial Deposit to an account (Checking/Savings) ]--
            try:
                initial_deposit_checking = None
                initial_deposit_savings = None
                
                if account_type_choice == '1':
                    initial_deposit_checking = float(input('- Enter \033[1mInitial Deposit Amount\033[0m for Checking Account: $'))
                elif account_type_choice == '2':
                    initial_deposit_savings = float(input('- Enter \033[1mInitial Deposit Amount\033[0m for Savings Account: $'))
                elif account_type_choice == '3':
                    initial_deposit_checking = float(input('- Enter \033[1mInitial Deposit Amount\033[0m for Checking Account: $'))
                    initial_deposit_savings = float(input('- Enter \033[1mInitial Deposit Amount\033[0m for Savings Account: $'))
                
                if initial_deposit_checking is not None and initial_deposit_checking < 0:
                    print('⚠️ Initial Deposit Amount for Checking Account cannot be Negative!')
                elif initial_deposit_savings is not None and initial_deposit_savings < 0:
                    print('⚠️ Initial Deposit Amount for Savings Account cannot be Negative!')
                    
            except ValueError:
                print('⚠️ \033[1mInvalid Amount!\033[0m Try again.')
            
            # Create Customer Account
            new_account_id = bank_management.add_new_customer(first_name, last_name, password, account_type_choice, initial_deposit_checking, initial_deposit_savings)
            print(f'✅ Customer Account Create Successfully! You can Login with Your ID: {new_account_id}')

    
        # [2] Log In
        case '2':
            print('\n\n -----------(🚪       Log In       🚪)-----------\n')
            
            while True:
                # --[ 1. Ask the account ID & password ]--
                account_id = input('- Enter your Account ID: ').strip()
                password = input('- Enter your Password: ').strip()
                
                if account_id.lower() in ('b', 'back') or password.lower() in ('b', 'back'):
                    break # back to the main menu

                customer = bank_management.login(account_id, password)
                if customer:
                    # Customer Account
                    account = bank_management.create_customer_account(customer)

                    while True:
                        print(f'\n\n------------🌟 Welcome Back {customer.get_fullname()}! 🌟------------\n')
                        print('[1] \033[1mWithdraw\033[0m Money from Account') 
                        print('[2] \033[1mDeposit\033[0m Money into Account')
                        print('[3] \033[1mTransfer\033[0m Money Between Accounts')
                        print('[0] Exit')
                        user_choice_login = input('Enter Your Choice Number (0-3): ')
                        
                        match user_choice_login:
                            # Withdraw Money from Account
                            case '1':
                                print('\n----💸 Withdraw Money 💸----')
                            
                            # Deposit Money into Account
                            case '2':
                                print('\n----💸 Deposit Money 💸----')
                            
                            # Transfer Money Between Accounts
                            case '3':
                                print('\n----💸 Transfer Money 💸----')
                            
                            # Exit
                            case '0':
                                print('\n \033[1m-----------------------------------------------------------\033[0m')
                                print('|           💸🏦 \033[1mThank you for use ACME Bank\033[0m 🏦💸           |')
                                print(' \033[1m-----------------------------------------------------------\033[0m')
                                sys.exit()
                            
                            # Default case
                            case _:
                                print('⚠️ \033[1mInvalid Choice!\033[0m Try again.')
                else:
                    print('\n⚠️ Invalid account ID or password!\n!!! Don\'t have an account? Return to the main menu by typing "back or b" !!!\n')

        # [3] Exit
        case '0':
            print('\n \033[1m-----------------------------------------------------------\033[0m')
            print('|           💸🏦 \033[1mThank you for use ACME Bank\033[0m 🏦💸           |')
            print(' \033[1m-----------------------------------------------------------\033[0m')
            sys.exit()
        
        # [_] Default case
        case _:
            print('⚠️ \033[1mInvalid Choice!\033[0m Try again.')