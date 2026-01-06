"""
Narudee Chakitdee
673040147-9
Lab4-1 P2
"""
class BankAccount:
    saving_run = 0
    loan_run = 0
    branch_number = 1724
    branch_name = "KKU Complex"
    
    def __init__(self, name, acc_type='saving', balance=0): # constructor
        self.name = name
        self.type = acc_type
        self.balance = balance
        
        if self.type == 'saving':
            BankAccount.saving_run += 1
            self.runing = f"{BankAccount.branch_number}-1-{BankAccount.saving_run}"
        else:
            BankAccount.loan_run += 1
            self.runing = f"{BankAccount.branch_number}-2-{BankAccount.loan_run}"

    def print_customer(self):
        print("----- Customer Record -----")
        print(f"Name: {self.name}")
        print(f"Account number: {self.runing}")
        print(f"Account type: {self.type}")
        print(f"Balance: {self.balance:,}")
        print("----- End Record -----")

    def deposit(self, amount = 0):
        self.balance += amount
        return self.balance
    
    def get_balance(self):
        return self.balance
    
    def pay_loan(self, amount = 0):
        self.balance += amount
        return self.balance


                