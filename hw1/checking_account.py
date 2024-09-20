from transaction import Transaction
from decimal import Decimal, ROUND_HALF_UP

from account import Account


class CheckingAccount(Account):

    def __init__(self, number):
        super().__init__(number)
        self._type = "Checking"
        self._interest_rate = Decimal(0.0008)
    
    def verify_transaction(self, amount, date):
        verified = super().verify_transaction(amount, date)
        if not verified:
            return 

         # create new transaction
        new_transaction = Transaction(date, amount)
        
        # apply it to the account
        new_transaction.withdraw_or_deposit(self)

        # add it to transactions list
        self._transactions.append(new_transaction)
        
# checking accounts have a monthly interest rate of 0.08%.
# After applying interest, checking accounts add a transaction for a $5.44 fee 
# if the balance was not greater or equal to a threshold of $100.   
    def interest_and_fees(self):
        interest_date = super().interest_and_fees()

        if self._balance < Decimal(100):
            self.apply_fee(interest_date)

    def apply_fee(self, date):
        fee = Decimal(-5.44)
        fee_transaction = Transaction(date, fee)
        fee_transaction.withdraw_or_deposit(self)
        self._transactions.append(fee_transaction)



    # Unlike a user's withdrawals, this can allow the balance to become negative meaning that the user owes the bank money
    # If interest and fees are applied to an account with a negative balance, 
    # the interest would also be negative since the bank wants interest on the amount owed to them. The $5.44 fee would also be applied again (this bank is ruthless!).