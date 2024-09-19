from transaction import Transaction
from account import Account


class SavingsAccount(Account):

# If you try to add more than 2 transactions in the same day 
# or more than 5 in the same month to a savings account, 
# then the transaction will not be saved. 

# in both cases you cannot make a transaction that would overdraw the account (make the balance negative).
    def add_transaction():
        