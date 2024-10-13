from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP

from sqlalchemy import Column, Integer, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship, mapped_column
from base import Base



class Transaction(Base):
    """Represents a transaction, including a date and an amount. This class provides
    methods to apply the transaction to an account, updating the account's balance, and 
    format the transaction details."""
    __tablename__ = '_transactions'
    id = mapped_column(Integer, primary_key=True)
    account_number = mapped_column(Integer, ForeignKey('accounts.number'))
    _amount = mapped_column(Float(asdecimal=True))
    _date = mapped_column(DateTime)
    interest=mapped_column(Boolean)

    account = relationship("Account", back_populates="_transactions")
    
    
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
   
