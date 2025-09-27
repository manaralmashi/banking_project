# 🏦 Banking Projact (ASRM Bank CLI) 🏦

ASRM Bank CLI is a Python-based command-line application that provides a simulation of essential banking operations, text-based environment.  
This project showcases how core banking logic can be implemented in a clean, object-oriented design.


## 🔹 Features

- **Add New Customer**
  - A customer can have:
    - Checking account
    - Savings account
    - Or both.
  - A customer can open and deposit initial amount:
    - into Checking account
    - into Savings account
    - Or both.

- **Account Operations (Login Required)**
  1. **Withdraw Money**
    - From savings or checking
  2. **Deposit Money**
    - Into savings or checking
  3. **Transfer Money**
    - From savings to checking
    - From checking to savings
    - From checking or savings to **another customer’s account**
  4. **Overdraft Protection**
  5. **Reactivate Account**
  6. **Check Balance**
  7. **Display Account Information**

## 🔹 Installation

Clone the repository and navigate into the project folder:

```bash
git clone [https://github.com/manaralmashi/banking_project.git]
cd banking_project
````

No extra dependencies are required—just Python 3.x.

## 🔹 Usage

Run the application from the terminal:

```bash
python3 main.py
```

Follow the on-screen menu to create customers, login to account, and perform operations.

## 🔹 What I Learned

* **Error handling and validation:** Managing invalid inputs and protecting against overdrafts.
* **Test-driven development mindset:** Writing unit tests to ensure critical operations work as expected.
* **Object-oriented design:** Creating classes for customers, accounts, and bank_management to keep code modular and scalable.
**Banking systems logic:** Gained an understanding of how real banking systems work—this was both extremely useful and enjoyable.

## 🔹 Contributing 

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
Please update tests as appropriate.
