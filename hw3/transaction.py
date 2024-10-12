from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP


class Transaction:
    """Represents a transaction, including a date and an amount. This class provides
    methods to apply the transaction to an account, updating the account's balance, and 
    format the transaction details."""
    def __init__(self, date, amount):
        """
        Initialize a Transaction object with the given date and amount.
        
        Args:
            date (str): The date of the transaction in the format 'YYYY-MM-DD'.
            amount (float or str): The transaction amount.
        """
        self._date = date
        self._amount = Decimal(amount)
    
    def __repr__(self):
        """
        Return a string representation of the transaction, including the date and amount.
        
        Returns:
            str: A formatted string representing the transaction.
        """
        return f"{self._date.strftime('%Y-%m-%d')}, ${self._amount:,.2f}"

    def withdraw_or_deposit(self, account):
        """
        Apply the transaction (withdraw or deposit) to the provided account by updating its balance.
        
        Args:
            account (Account): The account to which the transaction will be applied.
        
        Returns:
            None: Updates the account balance after applying the transaction.
        """
        balance_after_transaction = account._balance + self._amount
        account._balance = balance_after_transaction.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        return
   
