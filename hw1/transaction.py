from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP


class Transaction:
    def __init__(self, date, amount):
        self._date = datetime.strptime(date, "%Y-%m-%d")
        self._amount = Decimal(amount)
    
    def __repr__(self):
        return f"{self._date.strftime('%Y-%m-%d')}, ${self._amount:,.2f}"

    def withdraw_or_deposit(self, account):
        balance_after_transaction = account._balance + self._amount
        account._balance = balance_after_transaction.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        return
   
