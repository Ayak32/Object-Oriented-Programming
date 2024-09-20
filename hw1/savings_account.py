from transaction import Transaction
from account import Account
from decimal import Decimal


class SavingsAccount(Account):

    def __init__(self, number):
        super().__init__(number)
        self._type = "Savings"
        self.interest_rate = Decimal(0.0041)
        self._date_count = {}
        self._month_count = {}

    def verify_transaction(self, amount, date):
        # checks that the transaction would not overdraw the account
        verified = super().verify_transaction(amount, date)

        # extract the year and month from date to check count of monthly transactions
        year_month = date[:7]

        # ignore transacation if:
        # the transaction would overdraw
        # two transactions have already occured on that day
        # five transactions have already occured that month
        if not verified:
            return 

        # Check if the limit for daily transactions has been reached
        if self._date_count.get(date, 0) >= 2:
            return 

        # Check if the limit for monthly transactions has been reached
        if self._month_count.get(year_month, 0) >= 5:
            return
            

        # create new transaction
        new_transaction = Transaction(date, amount)
        
        # apply it to the account
        new_transaction.withdraw_or_deposit(self)

        # add it to transactions list
        self._transactions.append(new_transaction)

        # add date to to date_count
        if date in self._date_count:
            self._date_count[date] += 1
        else:
            self._date_count[date] = 1

        # add year_month to to month_count
        if year_month in self._month_count:
            self._month_count[year_month] += 1
        else:
            self._month_count[year_month] = 1
    
    # Our savings accounts should have a monthly interest rate of .41% (roughly 5% APY) 
    #  the currently selected account adds a transaction for the total balance times the interest rate. 
    # The date for this transaction should be the last day of the month that had the latest user created transaction.
    # This transaction bypasses transaction limits on savings accounts. 