from transaction import Transaction
from decimal import Decimal, ROUND_HALF_UP
from overdraw_error import OverdrawError
import logging
from account import Account


class CheckingAccount(Account):
    """A class representing a checking account, inheriting from the Account class.
    """
    def __init__(self, number):
        """Initialize the CheckingAccount with the given account number. 
        Sets the account type to "Checking" and assigns an interest rate.
        
        Args:
            number (int): The account number.
        """
        super().__init__(number)
        self._type = "Checking"
        self.interest_rate = Decimal(0.0008)
    
    def verify_transaction(self, amount, date):
        """Verify if a transaction can be processed based on the account balance, 
        and if valid, apply the transaction to the account.
        
        Args:
            amount (str): The transaction amount.
            date (str): The date of the transaction.
        
        Returns:
            None: If the transaction is not verified, nothing happens. 
                  If verified, the transaction is applied to the account.
        """


        super().verify_transaction(amount, date)

         # create new transaction
        new_transaction = Transaction(date, amount)
        
        # apply it to the account
        new_transaction.withdraw_or_deposit(self)

        # add it to transactions list
        self._transactions.append(new_transaction)
        
  
    def interest_and_fees(self):
        """Apply interest to the account and deduct a fee if the balance is below $100.
        
        Returns:
            None: Applies interest and fees to the account.
        """
        interest_transaction = super().interest_and_fees()

        if self._balance < Decimal(100):
            self._apply_fee(interest_transaction._date)

    def _apply_fee(self, date):
        fee = Decimal(-5.44)
        fee_transaction = Transaction(date, fee)
        fee_transaction.withdraw_or_deposit(self)
        self._transactions.append(fee_transaction)
        logging.debug(f"Created transaction: {self._number}, {fee_transaction._amount}")
