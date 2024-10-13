from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy.orm import DeclarativeBase
from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime
from transaction import Transaction
from base import Base

import logging

# class Base(DeclarativeBase):
#     pass

class Account(Base):
    __tablename__ = 'accounts'

    account_number = mapped_column(Integer, primary_key=True)
    balance = mapped_column(Float(asdecimal=True))
    account_type = mapped_column(String(50))

    transactions = relationship("Transaction", back_populates="account")
    
    __mapper_args__ = {
        'polymorphic_identity': 'account',
        'polymorphic_on': account_type
    }

    def __init__(self, account_number):
        """Initialize an account with 0 balance"""

        self.account_number = account_number
        self.balance = Decimal('0')
        # self.transactions = []  # List of Transaction objects

    def __str__(self):
        return f"#{self.account_number:09},\tbalance: ${self.get_balance():,.2f}"

    def update_balance(self):
        """Sum all transactions and update account with total balance"""

        balance = 0
        for t in self.transactions:
            balance += t.amount
        self.balance = balance

    def get_balance(self):
        """Returns the current account balance"""
        # getter
        return self.balance
    
    def sort_transactions(self):
        """Return a stably sorted list of transactions by date"""

        # sort with a lambda function that compares dates as datetime objects
        sorted_transactions = sorted(self.transactions)
        return sorted_transactions

    def list_transactions(self):
        """Print a list of all transactions, sorted."""

        sorted_transactions = self.sort_transactions()
        for t in sorted_transactions:
            print(t)

    def get_latest_transaction(self):
        """Return the most recent transaction in terms of transaction date"""

        # last index of array
        return self.sort_transactions()[-1]
    
    def add_transaction(self, amt, date, interest=False):
        if isinstance(date, str):
            date = datetime.strptime(date, "%Y-%m-%d")
        t = Transaction(amt, date, interest=interest)

        if not interest:
            balance_ok = self.check_balance(t)
            if not balance_ok:
                raise OverdrawError
            
        limits_ok = self.check_limits(t)
        date_ok = self.check_date(t)
    
        if t.is_interest() or interest or (balance_ok and limits_ok and date_ok):
            logging.debug(f"Created transaction: {self.account_number}, {t.amount}")
            self.transactions.append(t)
            self.update_balance()
    # def get_transactions(self):
    #     return sorted(self.transactions)
    def check_balance(self, t):
        return t.check_balance(self.get_balance())
    
    def check_limits(self, t):
        return True
    
    def check_date(self, t):
        if len(self.transactions) > 0:
            latest_transaction = self.get_latest_transaction()
            if t.date < latest_transaction.date:
                raise TransactionSequenceError(latest_transaction.date)
            else:
                return True
        else:
            return True
        
    def assess_interest(self, latest_transaction):
        self.add_transaction(self.get_balance() * self.interest_rate, 
                        date=latest_transaction.last_day_of_month(), 
                        interest=True)
        
    def assess_fees(self, latest_transaction):
        pass

    def interest_and_fees(self):
        """Used to apply interest and/or fees for this account"""
        latest_transaction = self.get_latest_transaction()
        # if latest transaction is interest, then interest cannot be applied again
        if latest_transaction.is_interest():
            raise TransactionSequenceError(latest_transaction.date)
        self.assess_interest(latest_transaction)
        self.assess_fees(latest_transaction)

class CheckingAccount(Account):
    __tablename__ = 'checking_accounts'
    account_number = mapped_column(Integer, ForeignKey('accounts.account_number'), primary_key=True)
    interest_rate = mapped_column(Float(asdecimal=True))
    low_balance_fee = mapped_column(Float(asdecimal=True))
    balance_threshold = mapped_column(Float(asdecimal=True))

    __mapper_args__ = {
        'polymorphic_identity': 'checking'
    }
    
    def __init__(self, account_number):
        """Initialize a checking account"""

        super().__init__(account_number)
        self.interest_rate = Decimal('.0008')
        self.low_balance_fee = Decimal("-5.44")
        self.balance_threshold = 100

    def __str__(self):
        return "Checking" + super().__str__()
    
    def assess_fees(self, latest_transaction):
        if self.get_balance() < self.balance_threshold:
            self.add_transaction(self.low_balance_fee,
                                 date=latest_transaction.last_day_of_month(), 
                                 interest=True)

    def account_info(self):
        """Return a formatted string displaying account information"""
        # create a "display" version of balance that is a rounded account balance
        display_amount = self.balance.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        return f"Checking#{self.account_number:09d},\tbalance: ${display_amount:,.2f}"
    
    # def check_interest(self, latest_date):


    # def add_transaction(self, amount, date, interest=False):
        """Adds a transaction to the current account"""

        if not interest:
            if self.balance + Decimal(str(amount)) < 0:
                raise OverdrawError()
            else:
                transaction = Transaction(amount, date)
                self.transactions.append(transaction)
                self.update_balance()
        # apply interest transactions no matter what
        else:
            transaction = Transaction(amount, date)
            self.transactions.append(transaction)
            self.update_balance()

    # def apply_interest(self):
        """Applies an interest transaction to an account and asseses if a fee needs to be applied"""

        interest = self.get_balance() * self.interest_rate
        latest_transaction = self.get_latest_transaction()

        if not self.check_interest(latest_transaction.date):
            raise TransactionSequenceError(latest_transaction.date)
        # break down string components of latest transaction date and use them as components in a new datetime object
        date = datetime(int(latest_transaction.date[:4]), int(latest_transaction.date[5:7]), int(latest_transaction.date[8:]))
        # find the next month
        nxt_mnth = date.replace(day=28) + timedelta(days=4)
        # move back to last day of previous month
        res = nxt_mnth - timedelta(days=nxt_mnth.day)
        last_day = res.day
        interest_date = f"{latest_transaction.date[:8]}{last_day}"

        self.add_transaction(interest, interest_date, True)

        # check if fee must be applied
        if self.get_balance() < Decimal(100.00):
            self.add_transaction(-5.44, interest_date, True)
        

class SavingsAccount(Account):
    __tablename__ = 'savings_accounts'

    account_number = mapped_column(Integer, ForeignKey('accounts.account_number'), primary_key=True)
    interest_rate = mapped_column(Float(asdecimal=True))
    daily_limit = mapped_column(Integer)
    monthly_limit = mapped_column(Integer)

    __mapper_args__ = {
        'polymorphic_identity': 'savings'
    }
    
    def __init__(self, account_number):
        """Initializes a savings account"""

        super().__init__(account_number)
        self.interest_rate = Decimal('.0041')
        self.daily_limit = 2
        self.monthly_limit = 5
        
    
    def __str__(self):
        return "Savings" + super().__str__()
    
    def check_limits(self, t1):
        if not t1.is_interest():
            num_today = len(
                [t2 for t2 in self.transactions if not t2.is_interest() and t2.in_same_day(t1)])
            num_this_month = len(
                [t2 for t2 in self.transactions if not t2.is_interest() and t2.in_same_month(t1)])
            if num_today >= self.daily_limit:
                raise TransactionLimitError("2 transactions in this day.")
            elif num_this_month >= self.monthly_limit:
                raise TransactionLimitError("5 transactions in this month.")
            return num_today < self.daily_limit and num_this_month < self.monthly_limit
    
    def account_info(self):
        """Returns a formatted string containing account information"""
        # calculate a "display" amount that is a formatted version of the balance
        display_amount = self.balance.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        return f"Savings#{self.account_number:09d},\tbalance: ${display_amount:,.2f}"

    # def add_transaction(self, amount, date, interest=False):
    #     """Adds a transaction to a savings account, ensuring it's for a valid date"""

    #     if interest: 
    #         transaction = Transaction(amount, date)
    #         self.transactions.append(transaction)
    #         self.update_balance()
    #     else:
    #         if self.balance + Decimal(amount) < 0:
    #             raise OverdrawError()
            
    #         transactions_day = 0
    #         transactions_month = 0
    #         current_month = date[:7] 
    #         current_day = date

    #         for t in self.transactions:
    #             if t.interest:
    #                 continue
    #             transaction_month = t.date[:7] # E=extract month
    #             transaction_day = t.date

    #             # tally transactions on a certain day or in a certain month
    #             if current_month == transaction_month:
    #                 transactions_month += 1
    #             if current_day == transaction_day:
    #                 transactions_day += 1

    #         if transactions_month >= 5 or transactions_day >= 2:
    #             return
            
    #         # add a transaction as long as no limits have been reached
    #         transaction = Transaction(amount, date)
    #         self.transactions.append(transaction)
    #         self.update_balance()
    #         return

    # def apply_interest(self):
        """Applies one month of interest to an account"""
        if not self.check_interest():
            raise TransactionSequenceError()

        interest = self.get_balance() * self.interest_rate
        latest_transaction = self.get_latest_transaction()
        # create a datetime object, breaking up the month, day, and year values from the latest_transaction.date string
        date = datetime(int(latest_transaction.date[:4]), int(latest_transaction.date[5:7]), int(latest_transaction.date[8:]))
        # move to next month
        nxt_mnth = date.replace(day=28) + timedelta(days=4)
        # subtract back to get last day of month
        res = nxt_mnth - timedelta(days=nxt_mnth.day)
        last_day = res.day
        interest_date = f"{latest_transaction.date[:8]}{last_day}"

        self.add_transaction(interest, interest_date, True)

class OverdrawError(Exception):
    """Exception raised when a transaction would overdraw an account"""
    def __init__(self, message="This transaction could not be completed due to an insufficient account balance."):
        self.message = message
        super().__init__(self.message)

class TransactionLimitError(Exception):
    """Exception raised when a transaction would exceed monthly/daily limit"""
    def __init__(self, limit, message="This transaction could not be completed because this account already has "):
        self.message = message
        self.limit = limit
        super().__init__(self.message)

class TransactionSequenceError(Exception):
    def __init__(self, latest_date, message=""):
        self.message = message
        self.latest_date = latest_date
        super().__init__(self.message)

    # def __str__(self):
    #     return f"New transactions must be from {self.latest_date} onward"