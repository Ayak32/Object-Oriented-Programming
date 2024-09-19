from transaction import Transaction
from account import Account

class CheckingAccount(Account):

#FIX
# but in both cases you cannot make a transaction that would overdraw the account (make the balance negative).
    def add_transaction(self, amount, date):
        current_balance = self._balance
        balance_after_transaction = current_balance + int(amount)
        if balance_after_transaction < 0:
            return 
        self._balance = balance_after_transaction


    