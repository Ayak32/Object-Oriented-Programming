from datetime import datetime
from transaction import Transaction
from decimal import Decimal
import calendar

class Account:
    def __init__(self, number):
        # keep list of each transaction
        self._transactions = []
        self._balance = 0
        self._number = number
    
    def number_matches(self, number):
        return int(number) == self._number

    def format_account(self):
        type = self._type.capitalize()
        number = self._number
        balance = self._balance
        # Pad the account number to 9 digits
        padded_account_number = f"{number:09}"
        # Format the balance with commas and 2 decimal places
        formatted_balance = f"${balance:,.2f}"
        return f"{type}#{padded_account_number},\tbalance: {formatted_balance}"
  
    def list_transactions(self):
        # sort by date
        sorted_transactions = sorted(self._transactions, key=lambda x: x._date)
        for tran in sorted_transactions:
            print(tran)

    def verify_transaction(self, amount, date):
        current_balance = self._balance
        decimal_amount = Decimal(amount)
        balance_after_transaction = current_balance + decimal_amount
        # prevents transactions from overdrawing 
        # but also also for checking fees to cause a negative balance
        if current_balance > 0 and balance_after_transaction < 0:
            return False
        return True

    def get_last_day(self):
        latest_month, latest_year = self._transactions[-1]._date.month, self._transactions[-1]._date.year
        day = calendar.monthrange(latest_year, latest_month)[1]
        return str(latest_year) + "-" + str(latest_month) + "-" + str(day)
    
    def interest_and_fees(self):
        current_balance = self._balance
        interest_rate = self._interest_rate

        interest_amount = current_balance * interest_rate
        interest_date = self.get_last_day()

        if current_balance < 0:
            negative_interest = -interest_amount
            print("in negative")
            interest_transaction = Transaction(interest_date, negative_interest)
        else: 
            interest_transaction = Transaction(interest_date, interest_amount)

        interest_transaction.withdraw_or_deposit(self)

        self._transactions.append(interest_transaction)
        return interest_date