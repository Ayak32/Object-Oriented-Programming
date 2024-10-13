from transaction import Transaction
from account import Account
from decimal import Decimal
from transaction_limit_error import TransactionLimitError

from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship, mapped_column

import logging

class SavingsAccount(Account):
    """A class representing a savings account, inheriting from the Account class.
    """
    __tablename__ = 'savings_accounts'

    number = mapped_column(Integer, ForeignKey('accounts.number'), primary_key=True)
    interest_rate = mapped_column(Float(asdecimal=True))
    # daily_limit = mapped_column(Integer)
    # monthly_limit = mapped_column(Integer)

    __mapper_args__ = {
        'polymorphic_identity': 'Savings'
    }

    def __init__(self, number):
        """
        Initialize a SavingsAccount with a unique account number, interest rate, 
        and counters for daily and monthly transaction limits.
        
        Args:
            number (int): The account number.
        """
        super().__init__(number)
        self._type = "Savings"
        self.interest_rate = Decimal(0.0041)
        self._date_count = {}
        self._month_count = {}

    def verify_transaction(self, amount, date):
        """
        Verify if a transaction can be applied to the savings account based on the account balance
        and daily/monthly transaction limits. Allows up to two transactions per day and five 
        transactions per month.
        
        Args:
            amount (str): The transaction amount.
            date (str): The date of the transaction in 'YYYY-MM-DD' format.
        
        Returns:
            None: Does not apply the transaction if any of the limits or balance constraints are exceeded.
        """
        # checks that the transaction would not overdraw the account
        super().verify_transaction(amount, date)

        # extract the year and month from date to check count of monthly transactions
        year_month = (date.year, date.month)



        # Check if the limit for daily transactions has been reached
        if self._date_count.get(date, 0) >= 2:
            raise TransactionLimitError("daily")

        # Check if the limit for monthly transactions has been reached
        if self._month_count.get(year_month, 0) >= 5:
            raise TransactionLimitError("monthly")
            

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
    
