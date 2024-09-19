from transaction import Transaction
from account import Account


class SavingsAccount(Account):

    def __init__(self, number):
        super().__init__(number)
        self._type = "Savings"
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
        if date in self._date_count:
            if self._date_count[date] == 2 or self._month_count[year_month] == 5:
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