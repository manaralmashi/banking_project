import sys      # needed for sys.exit()
import csv_bank

from bank.bank_management import BankManagement
from bank.customer import Customer

bank_management = BankManagement()

# Learned text colored from `https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal`
def titleFormat(title, emoji):
    print(f'\n\n \033[34m\033[1m---------(\033[0m\033[0m{emoji} {title} {emoji}\033[34m\033[1m)---------\033[0m\033[0m\n')

def exitMassageFormat():
    print('\n\n\n \033[36m\033[1m-----------------------------------------------------------\033[0m\033[0m')
    print('\033[36m\033[1m|\033[0m\033[0m           💸🏦 \033[1mThank you for use ACME Bank\033[0m 🏦💸           \033[36m\033[1m|\033[0m\033[0m')
    print(' \033[36m\033[1m-----------------------------------------------------------\033[0m\033[0m\n\n')

try:
    while True:
        # Learn (print bold text) from `https://www.reddit.com/r/learnpython/comments/mxhxgm/how_do_i_print_bold_text/`
        print('\n \033[34m\033[1m-----------------------------------------------------------\033[0m\033[0m')
        print('\033[34m\033[1m|\033[0m\033[0m               💸🏦 Welcome To ACME Bank 🏦💸              \033[34m\033[1m|\033[0m\033[0m')
        print(' \033[34m\033[1m-----------------------------------------------------------\033[0m\033[0m')
        print('[1] Add New Customer')
        print('[2] Login Account')
        print('[0] Exit')
        print(' \033[1m-----------------------------------------------------------\033[0m')
        user_choice_main = input('🔸 Enter Your Choice Number (0-2): ')
        
        match user_choice_main:
            # [1] Add New Customer
            case '1':
                titleFormat('Create New Customer', '👤')
                
                # --[ 1. Ask the FullName ]--
                while True:
                    first_name = input('🔸 Enter First Name: ').strip().capitalize()
                    last_name = input('🔸 Enter Last Name: ').strip().capitalize()
                    
                    # name validation
                    if first_name.replace(" ", "").isalpha() and last_name.replace(" ", "").isalpha():
                        break
                    else:
                        print('⚠️ Sorry, you have to write your name with only letters!')
                
                # --[ 2. Ask the Password ]--
                while True:
                    # password validation
                    password = input('🔸 Enter Password (8-15 chars, with upper/lower/digit/special): ')
                    temp_customer = Customer('temp', 'temp', 'temp', password)
                    
                    is_valid_password = temp_customer.is_valid_password()
                    if is_valid_password:
                        # -[ 3. Ask for Confirm password ]-
                        while True:
                            confirm_password = input('🔸 Confirm Password: ')
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
                    account_type_choice = input('🔸 Enter Account Type you want to open (1-3): ')
                    # validate choice
                    if account_type_choice in ['1', '2', '3']:
                        break
                    print('⚠️ \033[1mInvalid Choice!\033[0m Try again.')
                
                # --[ 5. Initial Deposit to an account (Checking/Savings) ]--
                try:
                    initial_deposit_checking = None
                    initial_deposit_savings = None
                    
                    if account_type_choice == '1':
                        initial_deposit_checking = float(input('🔸 Enter \033[1mInitial Deposit Amount\033[0m for Checking Account: $'))
                    elif account_type_choice == '2':
                        initial_deposit_savings = float(input('🔸 Enter \033[1mInitial Deposit Amount\033[0m for Savings Account: $'))
                    elif account_type_choice == '3':
                        initial_deposit_checking = float(input('🔸 Enter \033[1mInitial Deposit Amount\033[0m for Checking Account: $'))
                        initial_deposit_savings = float(input('🔸 Enter \033[1mInitial Deposit Amount\033[0m for Savings Account: $'))
                    
                    if initial_deposit_checking is not None and initial_deposit_checking < 0:
                        print('⚠️ Initial Deposit Amount for Checking Account cannot be Negative!')
                    elif initial_deposit_savings is not None and initial_deposit_savings < 0:
                        print('⚠️ Initial Deposit Amount for Savings Account cannot be Negative!')
                        
                except ValueError:
                    print('⚠️ \033[1mInvalid Amount!\033[0m Try again.')
                
                # Create Customer Account
                new_account_id = bank_management.add_new_customer(first_name, last_name, password, account_type_choice, initial_deposit_checking, initial_deposit_savings)
                print(f'✅ Customer Account Created Successfully! You can Login with Your ID: {new_account_id}')

        
            # [2] Log In
            case '2':
                titleFormat('    Login Account    ', '🚪')
                
                while True:
                    # --[ 1. Ask the account ID & password ]--
                    account_id = input('🔸 Enter your Account ID (ex. \'2025###\'): ').strip()
                    password = input('🔸 Enter your Password: ').strip()
                    
                    if account_id.lower() in ('b', 'back') or password.lower() in ('b', 'back'):
                        break # back to the main menu

                    customer = bank_management.login(account_id, password)
                    if customer:
                        # Customer Account
                        account = bank_management.create_customer_account(customer)

                        while True:
                            titleFormat(f'Welcome Back \033[1m{customer.get_fullname()}\033[0m', '🌟🏦🌟')
                            
                            # Account Status display
                            status = "🟢 ACTIVE" if customer.is_active else "🔴 DEACTIVATED"
                            print(f"Account Status: {status}")

                            if not customer.is_active:
                                print("# Use [4] to reactivate your account\n")
                            
                            # --[ 2. Ask the operation ]--
                            print('\n[1] \033[1mWithdraw\033[0m Money from Account') 
                            print('[2] \033[1mDeposit\033[0m Money into Account')
                            print('[3] \033[1mTransfer\033[0m Money Between Accounts')
                            print('[4] \033[1mReactivate My Account\033[0m')
                            print('[5] \033[1mCheck Balance\033[0m')
                            print('[6] \033[1mDisplay Account Info\033[0m')
                            print('[0] Exit')
                            user_choice_login = input('🔸 Enter Your Choice Number (0-3): ')
                            
                            match user_choice_login:
                                # Withdraw Money from Account
                                case '1':
                                    # --[ 3. Ask account type for withdraw ]--
                                    titleFormat(f'   Withdraw Money   ', '💸')
                                    print('[1] Withdraw from \033[1mChecking\033[0m Account') 
                                    print('[2] Withdraw from \033[1mSavings\033[0m Account')
                                    print('[3] Back')
                                    print('[0] Exit')
                                    user_choice_withdraw = input('🔸 Enter Your Choice Number (0-3): ')
                                    
                                    match user_choice_withdraw:
                                        # Withdraw from Checking Account
                                        case '1':
                                            account_type = 'checking'

                                            # if account is Deavtive
                                            if not customer.is_active:
                                                print("⚠️ Opps, The Account is \033[1mDeactive\033[0m ⚠️ To withdraw money from Checking you should reactivate checking account from the main menu!")
                                                continue

                                            # If customer does NOT has checking account, create it if he wants
                                            if not customer.has_checking_account():
                                                print('⚠️ \033[1mYou do NOT have a Checking Account!\033[0m')
                                                continue  # return to Withdraw menu
                                            
                                            titleFormat(f'Withdraw from \033[1mChecking\033[0m Account', '💸')
                                            print(f'💳 Balance in checking account: \033[1m{customer.balance_checking}\033[0m$ 💳')
                                            
                                            if customer.balance_checking < 0:
                                                print(f'✴️ Overdraft Protection Active ✴️')
                                                print(f'   • Max withdrawal: ${customer.max_overdraft_withdrawal}')
                                                print(f'   • Min balance limit: ${customer.max_overdraft_limit}')
                                                print(f'   • Overdraft count: {customer.overdraft_count}')
                                                print(f'   • Overdraft fee: ${customer.overdraft_fee}')
        
                                            # --[ 4. Ask the amount to withdraw ]--
                                            while True:
                                                try:
                                                    amount = float(input(f'🔸 Enter Amount to Withdraw from Checking Account: $'))
                                                    success, message = account.withdraw(amount, account_type, bank_management)
                                                    print(message)
                                                    if success:
                                                        bank_management.save_all_customers()
                                                        # Save immediately if account gets deactivated
                                                        if not customer.is_active:
                                                            bank_management.save_all_customers()
                                                            print("Account status saved to database.")
                                                    break
                                                except ValueError:
                                                    print('\n⚠️ \033[1mInvalid Amount!\033[0m Try again.')
                                            
                                            # stay in withdraw menu after the withdraw process (success or failure)
                                            continue
                                        
                                        # Withdraw from Savings Account
                                        case '2':
                                            account_type = 'savings'
                                            
                                            # if account is Deavtive
                                            if not customer.is_active:
                                                print("⚠️ Opps, The Account is \033[1mDeactive\033[0m ⚠️ To withdraw money from Savings you should reactivate checking account from the main menu!")
                                                continue

                                            # If customer does NOT has savings account, create it if he wants
                                            if not customer.has_savings_account():
                                                print('⚠️ \033[1mYou do NOT have a Savings Account!\033[0m')
                                                continue  # return to Withdraw menu
                                            
                                            titleFormat(f'Withdraw from \033[1mSavings\033[0m Account', '💸')
                                            print(f'💳 Balance in savings account: \033[1m{customer.balance_savings}\033[0m$ 💳')
                                            
                                            # --[ 4. Ask the amount to withdraw ]--
                                            while True:
                                                try:
                                                    amount = float(input(f'🔸 Enter Amount to Withdraw from Savings Account: $'))
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
                                            exitMassageFormat() # Exit massage
                                            sys.exit()

                                        # Default case
                                        case _:
                                            print('⚠️ \033[1mInvalid Choice!\033[0m Try again.')
                                
                                # Deposit Money into Account
                                case '2':
                                    # --[ 3. Ask account type for deposit ]--
                                    titleFormat(f'    Deposit Money    ', '💸')
                                    print('[1] Deposit into \033[1mChecking\033[0m Account') 
                                    print('[2] Deposit into \033[1mSavings\033[0m Account')
                                    print('[3] Back')
                                    print('[0] Exit')
                                    user_choice_deposit = input('🔸 Enter Your Choice Number (0-3): ')
                                    
                                    match user_choice_deposit:
                                        # Deposit into Checking Account
                                        case '1':
                                            account_type = 'checking'
                                            
                                            # if account is Deavtive
                                            if not customer.is_active:
                                                print("⚠️ Opps, The Account is \033[1mDeactive\033[0m ⚠️ To Deposit into Checking Account you should reactivate from the main menu!")
                                                continue

                                            # If customer does NOT has checking account, create it if he wants
                                            if not customer.has_checking_account():
                                                print('\n⚠️ \033[1mYou do NOT have a Checking Account!\033[0m')
                                                while True:
                                                    user_want_open_account = input('🔸 Do you want to open Checking Account?\n[1] Yes\n[2] No\n- Enter Your Choice Number (1 or 2):').strip()
                                                    if user_want_open_account == '1':
                                                        # Update `balance_checking` from `None` to `0`
                                                        customer.balance_checking = 0
                                                        break
                                                    elif user_want_open_account == '2':
                                                        break
                                                    else:
                                                        print('\n⚠️ \033[1mInvalid Input!\033[0m Please Enter Your Choice Number (1 or 2)')
                                                continue  # return to Deposit menu
                                            
                                            titleFormat(f'Deposit into \033[1mChecking\033[0m Account', '💸')
                                            print(f'💳 Balance in checking account: \033[1m{customer.balance_checking}\033[0m$ 💳\n')
                                            
                                            # --[ 4. Ask the amount to deposit ]--
                                            while True:
                                                try:
                                                    amount = float(input(f'🔸 Enter Amount to Deposit into Checking Account: $'))
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

                                            # if account is Deavtive
                                            if not customer.is_active:
                                                print("⚠️ Opps, The Account is \033[1mDeactive\033[0m ⚠️ To Deposit into Savings Account you should reactivate from the main menu!")
                                                continue

                                            # If customer does NOT has savings account, create it if he wants
                                            if not customer.has_savings_account():
                                                print('\n⚠️ \033[1mYou do NOT have a Savings Account!\033[0m')
                                                while True:
                                                    user_want_open_account = input('🔸 Do you want to open Savings Account?\n[1] Yes\n[2] No\n- Enter Your Choice Number (1 or 2):').strip()
                                                    if user_want_open_account == '1':
                                                        # Update `balance_savings` from `None` to `0`
                                                        customer.balance_savings = 0
                                                        break
                                                    elif user_want_open_account == '2':
                                                        break
                                                    else:
                                                        print('\n⚠️ \033[1mInvalid Input!\033[0m Please Enter Your Choice Number (1 or 2)')
                                                continue  # return to Deposit menu
                                            
                                            titleFormat(f'Deposit into \033[1mSavings\033[0m Account', '💸')
                                            print(f'💳 Balance in savings account: \033[1m{customer.balance_savings}\033[0m$ 💳\n')
                                            
                                            # --[ 4. Ask the amount to deposit ]--
                                            while True:
                                                try:
                                                    amount = float(input(f'🔸 Enter Amount to Deposit into Savings Account: $'))
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
                                            exitMassageFormat() # Exit massage
                                            sys.exit()
                                        
                                        # Default case
                                        case _:
                                            print('⚠️ \033[1mInvalid Choice!\033[0m Try again.')
                            
                                # Transfer Money
                                case '3':
                                    while True:
                                        # --[ 3. Ask the transfer between who's accounts ]--
                                        titleFormat(f'    Transfer Money    ', '💸')
                                        print('[1] Transfer money between my accounts')
                                        print('[2] Transfer money to another customer')
                                        print('[3] Back')
                                        print('[0] Exit')
                                        user_choice_transfer = input('🔸 Enter Your Choice Number (0-3): ').strip()
                                    
                                        match user_choice_transfer:
                                            # Transfer money between my accounts
                                            case '1':
                                                # if account is Deavtive
                                                if not customer.is_active:
                                                    print("⚠️ Opps, The Account is \033[1mDeactive\033[0m ⚠️ To Transfer money between your accounts you should reactivate from the main menu!")
                                                    continue

                                                # --[ 4. Ask the transfer (from/to) ]--
                                                titleFormat(f'  Transfer between my accounts  ', '💸')
                                                print('[1] Transfer from Checking to Savings')
                                                print('[2] Transfer from Savings to Checking')
                                                print('[3] Back')
                                                print('[0] Exit')
                                                user_choice_transfer_between = input('🔸 Enter Your Choice Number (0-3): ')
                                                
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
                                                                    user_want_open_account = input('🔸 Do you want to open Checking Account?\n[1] Yes\n[2] No\n- Enter Your Choice Number (1 or 2):').strip()
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
                                                                    user_want_open_account = input('🔸 Do you want to open Savings Account?\n[1] Yes\n[2] No\n- Enter Your Choice Number (1 or 2):').strip()
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
                                                            amount = float(input(f'🔸 Enter Amount to Transfer from Checking to Savings : $'))
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
                                                                    user_want_open_account = input('🔸 Do you want to open Checking Account?\n[1] Yes\n[2] No\n- Enter Your Choice Number (1 or 2):').strip()
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
                                                                    user_want_open_account = input('🔸 Do you want to open Savings Account?\n[1] Yes\n[2] No\n- Enter Your Choice Number (1 or 2):').strip()
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
                                                            amount = float(input(f'🔸 Enter Amount to Transfer from Savings to Checking : $'))
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
                                                        exitMassageFormat() # Exit massage
                                                        sys.exit()

                                                    # Default case
                                                    case _:
                                                        print('⚠️ \033[1mInvalid Choice!\033[0m Try again.')

                                                break #if transfer between account is success return to the menu
                                            
                                            # Transfer money to another customer
                                            case '2':
                                                # if account is Deavtive
                                                if not customer.is_active:
                                                    print("⚠️ Opps, The Account is \033[1mDeactive\033[0m ⚠️ To Transfer money to another customer you should reactivate from the main menu!")
                                                    continue

                                                from_account_choice = ''
                                                while True:
                                                    # --[ 4. Ask from which account to transfer ]--
                                                    titleFormat(f'  Transfer to another customer  ', '💸')
                                                    print('[1] Transfer from Checking Account')
                                                    print('[2] Transfer from Savings Account')
                                                    print('[3] Back')
                                                    print('[0] Exit')
                                                    from_account_choice = input('🔸 Enter Your Choice Number (0-3): ').strip()
                                                    
                                                    match from_account_choice:
                                                        # Transfer from Checking Account
                                                        case '1':
                                                            from_account = "checking"
                                                            # Check the existence of checking accounts
                                                            if not customer.has_checking_account():
                                                                print('⚠️ \033[1mYou do NOT have a Checking Account!\033[0m')
                                                                continue
                                                            break
                                                        
                                                        # Transfer from Savings Account
                                                        case '2':
                                                            from_account = "savings"
                                                            # Check the existence of savings accounts
                                                            if not customer.has_savings_account():
                                                                print('⚠️ \033[1mYou do NOT have a Savings Account!\033[0m')
                                                                continue
                                                            break
                                                            
                                                        # Back
                                                        case '3':
                                                            break
                                                            
                                                        # Exit
                                                        case '0':
                                                            exitMassageFormat() # Exit massage
                                                            sys.exit()
                                                            
                                                        # Default case
                                                        case _:
                                                            print('⚠️ \033[1mInvalid Choice!\033[0m Try again.')
                                                            continue
                                                    
                                                if from_account_choice in ['1', '2']:
                                                    # --[ 5. Ask for recipient customer ID ]--
                                                    while True:
                                                        try:
                                                            recipient_customer_id = input('🔸 Enter Recipient Customer ID (ex. \'2025###\'): ').strip()
                                                            
                                                            if recipient_customer_id.lower() in ('b', 'back'):
                                                                break
                                                            
                                                            # Is the customer exist or not
                                                            if not bank_management.customer_exists(recipient_customer_id):
                                                                print('⚠️ \033[1mRecipient customer NOT found!\033[0m Please check the ID.')
                                                                continue

                                                            # search on recipient customer ID
                                                            recipient_customer = bank_management.search_customer(recipient_customer_id)
                                                            
                                                            if not recipient_customer:
                                                                print('⚠️ \033[1mRecipient customer NOT found!\033[0m Please check the ID.')
                                                                continue
                                                            
                                                            if recipient_customer_id == customer.account_id:
                                                                print('⚠️ \033[1mYou can NOT transfer to yourself!\033[0m')
                                                                continue
                                                            
                                                            if not recipient_customer.is_active:
                                                                print('⚠️ \033[1mRecipient account is Deactivated!\033[0m')
                                                                continue
                                                            
                                                            # --[ 6. Ask for amount to transfer ]--
                                                            if from_account == "checking":
                                                                print(f'\n💳 Balance in Checking Account: \033[1m{customer.balance_checking}\033[0m$ 💳')
                                                            elif from_account == "savings":
                                                                print(f'\n💳 Balance in Savings Account: \033[1m{customer.balance_savings}\033[0m$ 💳')
                                                            
                                                            amount = float(input(f'🔸 Enter Amount to Transfer from your {from_account} account: $'))
                                                            
                                                            # Transfer from your account to recipient customer
                                                            success, message = account.transfer(amount, from_account, "checking", recipient_customer_id, bank_management)
                                                            print(message)
                                                            
                                                            if success:
                                                                bank_management.save_all_customers()
                                                            
                                                            break
                                                            
                                                        except ValueError:
                                                            print('⚠️ \033[1mInvalid Amount!\033[0m Try again.')
                                                        except Exception as e:
                                                            print(f'⚠️ \033[1mError: {e}\033[0m')
                                                    
                                                    break  # return to the transfer menu

                                                break  # return to the main menu


                                                break #if transfer between account is success return to the menu

                                            # Back
                                            case '3':
                                                break

                                            # Exit
                                            case '0':
                                                exitMassageFormat() # Exit massage
                                                sys.exit()

                                            # Default case
                                            case _:
                                                print('⚠️ \033[1mInvalid Choice!\033[0m Try again.')

                                # Reactivate Account
                                case '4':
                                    if customer.is_active:
                                        print("✅ Your account is already active!")
                                        print(f"- Current overdraft count: {customer.overdraft_count}")
                                    else:
                                        print(f"\n---- Reactivate Account ----")
                                        titleFormat(f'   Reactivate Account   ', '↩️')
                                        print(f"🔹 Overdraft count: {customer.overdraft_count}")
                                        print(f"🔹 Total overdraft fees: ${customer.overdraft_count * customer.overdraft_fee:.2f}")
                                        
                                        # calculate required amount
                                        checking_balance = customer.balance_checking or 0
                                        
                                        if checking_balance < 0:
                                            balance_to_cover = -checking_balance  # convert nigative to positive
                                            print(f"🔹 Negative balance to cover: ${balance_to_cover:.2f}")
                                        else:
                                            balance_to_cover = 0
                                            print("✅ No negative balance to cover")
                                        
                                        overdraft_fees = customer.overdraft_count * customer.overdraft_fee
                                        total_required = balance_to_cover + overdraft_fees
                                        
                                        print(f"🔹 Overdraft fees: ${overdraft_fees:.2f}")
                                        print(f"🔹 \033[1mTotal required to reactivate\033[0m: ${total_required:.2f}")
                                        while True:
                                            try:
                                                user_reactivate_amount = float(input("🔸 Enter payment amount: $"))
                                                success, message = account.reactivate(user_reactivate_amount, bank_management)
                                                print(message)
                                                if success:
                                                    bank_management.save_all_customers()
                                                break
                                            except ValueError:
                                                print("⚠️ Invalid amount!")
                                
                                # Check Balance
                                case '5':
                                    print(account.get_balance_card(customer))
                                    check_balance = input("\n🔸 Press Enter to return to main menu :..")
                                    
                                # Display Account Info
                                case '6':
                                    print(bank_management.get_account_info_card(customer))
                                    account_info = input("\n🔸 Press Enter to return to main menu :..")

                                # Exit
                                case '0':
                                    exitMassageFormat() # Exit massage
                                    sys.exit()
                                
                                # Default case
                                case _:
                                    print('⚠️ \033[1mInvalid Choice!\033[0m Try again.')
                    else:
                        print('\n⚠️ Invalid account ID or password!\n!!! Don\'t have an account? Return to the main menu by typing "back or b" !!!\n')

            # [3] Exit
            case '0':
                exitMassageFormat() # Exit massage
                sys.exit()
            
            # [_] Default case
            case _:
                print('⚠️ \033[1mInvalid Choice!\033[0m Try again.')

except KeyboardInterrupt:
    #EX: If user enter ^C 
    exitMassageFormat()
    sys.exit()