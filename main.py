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
                        # --[ 2. Ask the operation ]--
                        print(f'\n\n------------🌟 Welcome Back {customer.get_fullname()}! 🌟------------\n')
                        print('[1] \033[1mWithdraw\033[0m Money from Account') 
                        print('[2] \033[1mDeposit\033[0m Money into Account')
                        print('[3] \033[1mTransfer\033[0m Money Between Accounts')
                        print('[0] Exit')
                        user_choice_login = input('Enter Your Choice Number (0-3): ')
                        
                        match user_choice_login:
                            # Withdraw Money from Account
                            case '1':
                                # --[ 3. Ask account type for withdraw ]--
                                print('\n----💸 Withdraw Money 💸----')
                                print('[1] Withdraw from \033[1mChecking\033[0m Account') 
                                print('[2] Withdraw from \033[1mSavings\033[0m Account')
                                print('[3] Back')
                                print('[0] Exit')
                                user_choice_withdraw = input('- Enter Your Choice Number (0-3): ')
                                
                                match user_choice_withdraw:
                                    # Withdraw from Checking Account
                                    case '1':
                                        account_type = 'checking'
                                        
                                        # If customer does NOT has checking account, create it if he wants
                                        if not customer.has_checking_account():
                                            print('⚠️ \033[1mYou do NOT have a Checking Account!\033[0m')
                                            continue  # return to Withdraw menu
                                        
                                        print('\n----💸 Withdraw from \033[1mChecking\033[0m Account 💸----')
                                        print(f'💳 Balance in checking account: \033[1m{customer.balance_checking}\033[0m$ 💳')
                                        
                                        # --[ 4. Ask the amount to withdraw ]--
                                        while True:
                                            try:
                                                amount = float(input(f'- Enter Amount to Withdraw from Checking Account: $'))
                                                success, message = account.withdraw(amount, account_type)
                                                print(message)
                                                if success:
                                                    bank_management.save_all_customers()
                                                break
                                            except ValueError:
                                                print('\n⚠️ \033[1mInvalid Amount!\033[0m Try again.')
                                        
                                        # stay in withdraw menu after the withdraw process (success or failure)
                                        continue
                                    
                                    # Withdraw from Savings Account
                                    case '2':
                                        account_type = 'savings'
                                        
                                        # If customer does NOT has savings account, create it if he wants
                                        if not customer.has_savings_account():
                                            print('⚠️ \033[1mYou do NOT have a Savings Account!\033[0m')
                                            continue  # return to Withdraw menu
                                        
                                        print('\n----💸 Withdraw from \033[1mSavings\033[0m Account 💸----')
                                        print(f'💳 Balance in savings account: \033[1m{customer.balance_savings}\033[0m$ 💳')
                                        
                                        # --[ 4. Ask the amount to withdraw ]--
                                        while True:
                                            try:
                                                amount = float(input(f'- Enter Amount to Withdraw from Savings Account: $'))
                                                success, message = account.withdraw(amount, account_type)
                                                print(message)
                                                if success:
                                                    bank_management.save_all_customers()
                                                break
                                            except ValueError:
                                                print('⚠️ \033[1mInvalid Amount!\033[0m Try again.')
                                        
                                        # stay in withdraw menu after the withdraw process (success or failure)
                                        continue

                                    # Back
                                    case '3':
                                        break

                                    # Exit
                                    case '0':
                                        print('\n \033[1m-----------------------------------------------------------\033[0m')
                                        print('|           💸🏦 \033[1mThank you for use ACME Bank\033[0m 🏦💸           |')
                                        print(' \033[1m-----------------------------------------------------------\033[0m')
                                        sys.exit()

                                    # Default case
                                    case _:
                                        print('⚠️ \033[1mInvalid Choice!\033[0m Try again.')
                            
                            # Deposit Money into Account
                            case '2':
                                # --[ 3. Ask account type for deposit ]--
                                print('\n----💸 Deposit Money 💸----')
                                print('[1] Deposit into \033[1mChecking\033[0m Account') 
                                print('[2] Deposit into \033[1mSavings\033[0m Account')
                                print('[3] Back')
                                print('[0] Exit')
                                user_choice_deposit = input('- Enter Your Choice Number (0-3): ')
                                
                                match user_choice_deposit:
                                    # Deposit into Checking Account
                                    case '1':
                                        account_type = 'checking'
                                                                                
                                        # If customer does NOT has checking account, create it if he wants
                                        if not customer.has_checking_account():
                                            print('\n⚠️ \033[1mYou do NOT have a Checking Account!\033[0m')
                                            while True:
                                                user_want_open_account = input('- Do you want to open Checking Account?\n[1] Yes\n[2] No\n- Enter Your Choice Number (1 or 2):').strip()
                                                if user_want_open_account == '1':
                                                    # Update `balance_checking` from `None` to `0`
                                                    customer.balance_checking = 0
                                                    break
                                                elif user_want_open_account == '2':
                                                    break
                                                else:
                                                    print('\n⚠️ \033[1mInvalid Input!\033[0m Please Enter Your Choice Number (1 or 2)')
                                            continue  # return to Deposit menu
                                        
                                        print('\n----💸 Deposit into \033[1mChecking\033[0m Account 💸----')
                                        print(f'💳 Balance in checking account: \033[1m{customer.balance_checking}\033[0m$ 💳\n')
                                        
                                        # --[ 4. Ask the amount to deposit ]--
                                        while True:
                                            try:
                                                amount = float(input(f'- Enter Amount to Deposit into Checking Account: $'))
                                                success, message = account.deposit(amount, account_type)
                                                print(message)
                                                if success:
                                                    bank_management.save_all_customers()
                                                break
                                            except ValueError:
                                                print('\n⚠️ \033[1mInvalid Amount!\033[0m Try again.')
                                        
                                        # stay in deposit menu after the deposit process (success or failure)
                                        continue
                                    
                                    # Deposit into Savings Account
                                    case '2':
                                        account_type = 'savings'

                                        # If customer does NOT has savings account, create it if he wants
                                        if not customer.has_savings_account():
                                            print('\n⚠️ \033[1mYou do NOT have a Savings Account!\033[0m')
                                            while True:
                                                user_want_open_account = input('- Do you want to open Savings Account?\n[1] Yes\n[2] No\n- Enter Your Choice Number (1 or 2):').strip()
                                                if user_want_open_account == '1':
                                                    # Update `balance_savings` from `None` to `0`
                                                    customer.balance_savings = 0
                                                    break
                                                elif user_want_open_account == '2':
                                                    break
                                                else:
                                                    print('\n⚠️ \033[1mInvalid Input!\033[0m Please Enter Your Choice Number (1 or 2)')
                                            continue  # return to Deposit menu
                                        
                                        print('\n----💸 Deposit into \033[1mSavings\033[0m Account 💸----')
                                        print(f'💳 Balance in savings account: \033[1m{customer.balance_savings}\033[0m$ 💳\n')
                                        
                                        # --[ 4. Ask the amount to deposit ]--
                                        while True:
                                            try:
                                                amount = float(input(f'- Enter Amount to Deposit into Savings Account: $'))
                                                success, message = account.deposit(amount, account_type)
                                                print(message)
                                                if success:
                                                    bank_management.save_all_customers()
                                                break
                                            except ValueError:
                                                print('⚠️ \033[1mInvalid Amount!\033[0m Try again.')
                                        
                                        # stay in deposit menu after the deposit process (success or failure)
                                        continue
                                    
                                    # Back
                                    case '3':
                                        break
                                    
                                    # Exit
                                    case '0':
                                        print('\n \033[1m-----------------------------------------------------------\033[0m')
                                        print('|           💸🏦 \033[1mThank you for use ACME Bank\033[0m 🏦💸           |')
                                        print(' \033[1m-----------------------------------------------------------\033[0m')
                                        sys.exit()
                                    
                                    # Default case
                                    case _:
                                        print('⚠️ \033[1mInvalid Choice!\033[0m Try again.')
                           
                            # Transfer Money
                            case '3':
                                while True:
                                    # --[ 3. Ask the transfer between who's accounts ]--
                                    print('\n----💸 Transfer Money 💸----')
                                    print('[1] Transfer money between my accounts')
                                    print('[2] Transfer money to another customer')
                                    print('[3] Back')
                                    print('[0] Exit')
                                    user_choice_transfer = input('- Enter Your Choice Number (0-3): ')
                                
                                    match user_choice_transfer:
                                        # Transfer money between my accounts
                                        case '1':
                                            # --[ 4. Ask the transfer (from/to) ]--
                                            print('\n----💸 Transfer between my accounts 💸----')
                                            print('[1] Transfer from Checking to Savings')
                                            print('[2] Transfer from Savings to Checking')
                                            print('[3] Back')
                                            print('[0] Exit')
                                            user_choice_transfer_between = input('Enter Your Choice Number (0-3): ')
                                            
                                            match user_choice_transfer_between:
                                                # Transfer from Checking to Savings
                                                case '1':
                                                    # Check the existence of checking and savings accounts
                                                    if not customer.has_checking_account() or not customer.has_savings_account():
                                                        print('\n❗️ To Transfer between your accounts, you MUST have both checking and savings accounts ❗️')
                                                        
                                                        # If customer does NOT has checking account, create it if he wants
                                                        if not customer.has_checking_account():
                                                            print('\n⚠️ \033[1mYou do NOT have a Checking Account!\033[0m')
                                                            while True:
                                                                user_want_open_account = input('- Do you want to open Checking Account?\n[1] Yes\n[2] No\n- Enter Your Choice Number (1 or 2):').strip()
                                                                if user_want_open_account == '1':
                                                                    # Update `balance_checking` from `None` to `0`
                                                                    customer.balance_checking = 0
                                                                    print('✅ Checking Account Created ✅')
                                                                    break
                                                                elif user_want_open_account == '2':
                                                                    break
                                                                else:
                                                                    print('\n⚠️ \033[1mInvalid Input!\033[0m Please Enter Your Choice Number (1 or 2)')
                                                            continue  # return to transfer menu

                                                        # If customer does NOT has savings account, create it if he wants
                                                        elif not customer.has_savings_account():
                                                            print('\n⚠️ \033[1mYou do NOT have a Savings Account!\033[0m')
                                                            while True:
                                                                user_want_open_account = input('- Do you want to open Savings Account?\n[1] Yes\n[2] No\n- Enter Your Choice Number (1 or 2):').strip()
                                                                if user_want_open_account == '1':
                                                                    # Update `balance_savings` from `None` to `0`
                                                                    customer.balance_savings = 0
                                                                    print('✅ Savings Account Created ✅')
                                                                    break
                                                                elif user_want_open_account == '2':
                                                                    break
                                                                else:
                                                                    print('\n⚠️ \033[1mInvalid Input!\033[0m Please Enter Your Choice Number (1 or 2)')
                                                            continue  # return to transfer menu
                                                    
                                                    # the customer has both checking and savings accounts! So, let do the transfer
                                                    try:
                                                        # --[ 5. Ask the amount to transfer ]--
                                                        print(f'\n💳 Balance in Checking account: \033[1m{customer.balance_checking}\033[0m$ 💳')
                                                        print(f'💳 Balance in Savings account: \033[1m{customer.balance_savings}\033[0m$ 💳\n')
                                                        amount = float(input(f'- Enter Amount to Transfer from Checking to Savings : $'))
                                                        success, message = account.transfer(amount, 'checking', 'savings')
                                                        print(message)
                                                        if success:
                                                            bank_management.save_all_customers()
                                                    except ValueError:
                                                        print('\n⚠️ \033[1mInvalid Amount!\033[0m Try again.')

                                                # Transfer from Savings to Checking
                                                case '2':
                                                    # Check the existence of checking and savings accounts
                                                    if not customer.has_checking_account() or not customer.has_savings_account():
                                                        print('\n❗️ To Transfer between your accounts, you MUST have both checking and savings accounts ❗️')
                                                        
                                                        # If customer does NOT has checking account, create it if he wants
                                                        if not customer.has_checking_account():
                                                            print('\n⚠️ \033[1mYou do NOT have a Checking Account!\033[0m')
                                                            while True:
                                                                user_want_open_account = input('- Do you want to open Checking Account?\n[1] Yes\n[2] No\n- Enter Your Choice Number (1 or 2):').strip()
                                                                if user_want_open_account == '1':
                                                                    # Update `balance_checking` from `None` to `0`
                                                                    customer.balance_checking = 0
                                                                    print('✅ Checking Account Created ✅')
                                                                    break
                                                                elif user_want_open_account == '2':
                                                                    break
                                                                else:
                                                                    print('\n⚠️ \033[1mInvalid Input!\033[0m Please Enter Your Choice Number (1 or 2)')
                                                            continue  # return to transfer menu

                                                        # If customer does NOT has savings account, create it if he wants
                                                        elif not customer.has_savings_account():
                                                            print('\n⚠️ \033[1mYou do NOT have a Savings Account!\033[0m')
                                                            while True:
                                                                user_want_open_account = input('- Do you want to open Savings Account?\n[1] Yes\n[2] No\n- Enter Your Choice Number (1 or 2):').strip()
                                                                if user_want_open_account == '1':
                                                                    # Update `balance_savings` from `None` to `0`
                                                                    customer.balance_savings = 0
                                                                    print('✅ Savings Account Created ✅')
                                                                    break
                                                                elif user_want_open_account == '2':
                                                                    break
                                                                else:
                                                                    print('\n⚠️ \033[1mInvalid Input!\033[0m Please Enter Your Choice Number (1 or 2)')
                                                            continue  # return to transfer menu
                                                    
                                                    # the customer has both checking and savings accounts! So, let do the transfer
                                                    try:
                                                        # --[ 5. Ask the amount to transfer ]--
                                                        print(f'\n💳 Balance in Checking account: \033[1m{customer.balance_checking}\033[0m$ 💳')
                                                        print(f'💳 Balance in Savings account: \033[1m{customer.balance_savings}\033[0m$ 💳\n')
                                                        amount = float(input(f'- Enter Amount to Transfer from Savings to Checking : $'))
                                                        success, message = account.transfer(amount, 'savings', 'checking')
                                                        print(message)
                                                        if success:
                                                            bank_management.save_all_customers()
                                                    except ValueError:
                                                        print('\n⚠️ \033[1mInvalid Amount!\033[0m Try again.')

                                                # Back
                                                case '3':
                                                    break

                                                # Exit
                                                case '0':
                                                    print('\n \033[1m-----------------------------------------------------------\033[0m')
                                                    print('|           💸🏦 \033[1mThank you for use ACME Bank\033[0m 🏦💸           |')
                                                    print(' \033[1m-----------------------------------------------------------\033[0m')
                                                    sys.exit()

                                                # Default case
                                                case _:
                                                    print('⚠️ \033[1mInvalid Choice!\033[0m Try again.')

                                            break #if transfer between account is success return to the menu
                                        
                                        # Transfer money to another customer
                                        case '2':
                                            print('❌ Transfer to other customers coming soon!')
                                            
                                            break #if transfer between account is success return to the menu

                                        # Back
                                        case '3':
                                            break

                                        # Exit
                                        case '0':
                                            print('\n \033[1m-----------------------------------------------------------\033[0m')
                                            print('|           💸🏦 \033[1mThank you for use ACME Bank\033[0m 🏦💸           |')
                                            print(' \033[1m-----------------------------------------------------------\033[0m')
                                            sys.exit()

                                        # Default case
                                        case _:
                                            print('⚠️ \033[1mInvalid Choice!\033[0m Try again.')

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