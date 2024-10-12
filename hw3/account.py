from datetime import datetime
from transaction import Transaction
from decimal import Decimal
from overdraw_error import OverdrawError
from transaction_sequence_error import TransactionSequenceError
import logging
import calendar

class Account:
    """An abstract class that represents a generic bank account. The account tracks transactions, maintains a balance, 
    and provides methods for verifying and listing transactions, applying interest and fees, 
    and formatting account details."""
    def __init__(self, number):
        """Initialize the Account with a given account number, an empty transaction list, 
        and a starting balance of 0.
        
        Args:
            number (int): The account number.
        """

        self._transactions = []
        self._balance = 0
        self._number = number
        self._interest_fees_month = None
    
    def number_matches(self, number):
        """Check if the provided account number matches this account's number.
        
        Args:
            number (int): The account number to check.
        
        Returns:
            bool: True if the account numbers match, False otherwise.
        """
        return int(number) == self._number

    def format_account(self):
        """Format the account details as a string with the account type, padded account number,
        and the current balance.
        
        Returns:
            str: A formatted string representing the account details.
        """
        type = self._type.capitalize()
        number = self._number
        balance = self._balance
        # Pad the account number to 9 digits
        padded_account_number = f"{number:09}"
        # Format the balance with commas and 2 decimal places
        formatted_balance = f"${balance:,.2f}"
        return f"{type}#{padded_account_number},\tbalance: {formatted_balance}"
  
    def list_transactions(self):
        """List all transactions for this account, sorted by date.
        
        Prints:
            Each transaction in chronological order.
        """
        # Sort by date
        sorted_transactions = sorted(self._transactions, key=lambda x: x._date)
        for tran in sorted_transactions:
            print(tran)

    def verify_sequence(self, date):
        # if no previous transactions, no need to sort or verify sequence
        if len(self._transactions) == 0:
            return

        # sorts transactions from the latest to the earliest
        sorted_transactions = sorted(self._transactions, key=lambda transaction: transaction._date, reverse=True)
        latest_date = sorted_transactions[0]._date
        if date < latest_date:
            raise TransactionSequenceError("normalSequenceError", latest_date)

    def verify_transaction(self, amount, date):
        """Verify if a transaction can be applied to the account based on the balance.
        Prevents overdrawing except for when fees are applied to a checking account.
        
        Args:
            amount (str): The transaction amount.
            date (str): The transaction date.
        
        Returns:
            bool: True if the transaction is valid, False otherwise.
        """
        
        current_balance = self._balance

        balance_after_transaction = current_balance + amount
        # prevents transactions from overdrawing 
        # but also allows for checking fees to cause a negative balance
        if current_balance >= 0 and balance_after_transaction < 0:
            raise OverdrawError
        
        self.verify_sequence(date)

        return True


    def _get_last_day(self):
        latest_month, latest_year = self._transactions[-1]._date.month, self._transactions[-1]._date.year
        day = calendar.monthrange(latest_year, latest_month)[1]
        return datetime(latest_year, latest_month, day)
    
    def interest_and_fees(self):
        """Apply interest or fees based on the account balance. If the balance is positive, 
        interest is added; if the balance is negative, the interest becomes negative and a fee is charged.
        
        Returns:
            str: The date when the interest or fee was applied.
        """
        interest_date = self._get_last_day()

        if self._interest_fees_month is not None:
            # if the day we're applying interest is before recent than the last month we applied interest, raise exception
            if interest_date <= self._interest_fees_month:
                raise TransactionSequenceError("interestError", interest_date)

        self._interest_fees_month = interest_date


        current_balance = self._balance
        interest_rate = self.interest_rate

        interest_amount = current_balance * interest_rate

        if current_balance < 0:
            negative_interest = -interest_amount
            interest_transaction = Transaction(interest_date, negative_interest)
        else: 
            interest_transaction = Transaction(interest_date, interest_amount)

        interest_transaction.withdraw_or_deposit(self)

        self._transactions.append(interest_transaction)
        logging.debug(f"Created transaction: {self._number}, {interest_transaction._amount}")
        return interest_transaction