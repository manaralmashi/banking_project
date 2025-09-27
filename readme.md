# 🏦 Banking Projact (ASRM Bank CLI) 🏦

ASRM Bank CLI is a Python-based command-line application that provides a simulation of essential banking operations, text-based environment.  
This project showcases how core banking logic can be implemented in a clean, object-oriented design.


## 🌟 Features
### 🔹 Account Management
- **Create New Account**: Register with checking, savings, or both account types
- **Login Security**: Access your account with automatically generated ID and password
- **Account Status**: View active/deactivated status with reactivation options

### 🔹 Banking Operations
- **Withdraw Money**: From checking or savings accounts
- **Deposit Money**: Into existing or new accounts
- **Transfer Funds**: Between your accounts or to other customers
- **Check Balance**: Display current account balances in card
- **Account Information**: Display detailed account info in card

### 🔹 Security Features
- **Password Validation**: Strong password requirements (8-15 characters with uppercase, lowercase, numbers, and symbols)
- **Overdraft Protection**: Fees and limits for checking accounts
- **Account Reactivation**: Pay fees to restore access

## 🚀 Getting Started

### 🔹 Dependencies
* No extra dependencies are required — just Python 3.x.

### 🔹 Installing
* Clone the repository:
```bash
git clone https://github.com/manaralmashi/banking_project.git
````

* Navigate into the project folder:
```bash
cd banking_project
````

### 🔹 Executing program
* Run the application from the terminal:
```bash
python3 main.py
```

## 🏗️ Architecture
>The system follows a clean object-oriented design:
>- **Customer Class**
>- **Account Class**
>- **BankManagement Class**
>- **Main Application**: User interface with intuitive menu navigation and error handling


## 📋 Main Menu Options
>1. **Add New Customer** - Create bank account with initial deposit
>2. **Login Account** - Access your existing account, After Login Features:
>>    - **1. Withdraw Money** - Take money from your accounts
>>    - **2. Deposit Money** - Add money to your accounts  
>>    - **3. Transfer Money** - Send money between accounts or to others
>>    - **4. Reactivate Account** - Restore access if deactivated
>>    - **5. Check Balance** - View your current balances
>>    - **6. Display Account Info** - See detailed account information
>>    - **7. Exit** - Return to main menu
>3. **Exit** - Close the application


## ✏️ What I Learned
* **Error handling and validation:** Managing invalid inputs and protecting against overdrafts.
* **Test Driven Development (TDD):** Writing unit tests to ensure critical operations work as expected.
* **Object Oriented Programming (OOP):** Creating classes for customers, accounts, and bank management to keep code modular and scalable.
* **Banking systems logic:** Gained an understanding of how real banking systems work, this was both extremely useful and enjoyable.

## 🔓 Contributing 

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## 💡 Example of code I’m proud of

Here’s a piece of code I’m proud of, because it taught me a lot and helped me grow as a developer:
```bash
def reactivate(self, user_reactivate_amount, bank_management = None):
    if self.customer.is_active:
        return True, "✅ Account is already active"
    
    # calculate required amount to reactivate account
    checking_balance = self.customer.balance_checking or 0
    if checking_balance >= 0:
        balance_to_cover = 0
    else:
        balance_to_cover = abs(checking_balance)

    total_fees = self.customer.overdraft_count * self.customer.overdraft_fee
    total_required = balance_to_cover + total_fees
    
    if user_reactivate_amount >= total_required:
        # deposit amount
        if self.customer.balance_checking is not None:
            self.customer.balance_checking += user_reactivate_amount
        
        # reactivate
        self.customer.is_active = True
        self.customer.overdraft_count = 0
        
        # save to csv file
        if bank_management:
            bank_management.update_customer(self.customer)

        return True, f"✅ Account reactivated! Overdraft count reset to zero.\n💳 New Balance: ${(self.customer.balance_checking or 0):.2f}"
    else:
        return False, f"⚠️ Insufficient amount. Required: ${total_required:.2f}"
```

## 💻 Author
**Manar AlMashi** - Software Engineer & Full Stack Developer
- X: [@manaralmashi](https://x.com/manaralmashi)
- GitHub: [@manaralmashi](https://github.com/manaralmashi)
- LinkedIn: [@manaralmashi](https://linkedin.com/in/manaralmashi)
- Email: manar.almashii@gmail.com   

---

*Banking System Project - Python CLI Application*