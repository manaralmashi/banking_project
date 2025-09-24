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
            pass
    
        # [2] Log In
        case '2':
            pass
        
        # [3] Exit
        case '3':
            pass
        
        # [_] Default case
        case _:
            pass