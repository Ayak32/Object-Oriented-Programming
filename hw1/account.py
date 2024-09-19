from datetime import datetime

# should be an abstract class

# Base class for bank accounts
# maintains a list of transactions in the account
# methods support default behavior, but may be overridden by these next two classes...
class Account:
    def __init__(self, number, type):
        self._transactions = []
        self._balance = 0
        self._number = number
        self._type = type

    
    def number_matches(self, number):
        return int(number) == self._account_number

    def format_account(self):
        type = self._account_type
        number = self._account_number
        balance = self._account_balance
        # Pad the account number to 9 digits
        padded_account_number = f"{number:09}"
        # Format the balance with commas and 2 decimal places
        formatted_balance = f"${balance:,.2f}"
        return f"{type}#{padded_account_number},\t balance: {formatted_balance}"
  
    def list_transactions(self):
        sorted_transactions = sorted(self._transactions, key=lambda x: x.date)
        for tran in sorted_transactions:
            print(tran)

    def interest(self):
        pass

    def fee(self):
        pass