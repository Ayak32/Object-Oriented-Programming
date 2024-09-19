from transaction import Transaction
from decimal import Decimal, ROUND_HALF_UP
from account import Account


class CheckingAccount(Account):

# but in both cases you cannot make a transaction that would overdraw the account (make the balance negative).
    def __init__(self, number):
        super().__init__(number)
        self._type = "Checking"
    
    def verify_transaction(self, amount, date):
        verified = super().verify_transaction(amount, date)
        if not verified:
            return 

         # create new transaction
        new_transaction = Transaction(date, amount)
        
        # apply it to the account
        new_transaction.withdraw_deposit(self)

        # add it to transactions list
        self._transactions.append(new_transaction)
        


        self._balance = balance_after_transaction.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


    