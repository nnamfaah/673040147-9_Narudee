"""
Narudee Chakitdee
673040147-9
Lab4-1 P2
"""
from bank_acc import BankAccount

john = BankAccount("John", "saving", 500)
tim = BankAccount("Tim", "loan", -1000000)
sarah = BankAccount("Sarah", "saving")

# John deposit 3,000 and check balance
john.deposit(3000)
print(f"John balance: {john.get_balance():,}\n")

# Tim check loan and pay half of the balance
print(f"Tim loan: {tim.get_balance():,}")
tim.pay_loan((tim.get_balance()) / 2)
print(f"After payment: {tim.get_balance():,}\n")

# Sarah deposit 50,000,000
sarah.deposit(50000000)

# Sarah open loan account
sarah_loan = BankAccount("Sarah", "loan", -100000000)

# show print_customer
john.print_customer()
print()
tim.print_customer()
print()
sarah.print_customer()
print()
sarah_loan.print_customer()