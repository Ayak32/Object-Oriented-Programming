from sqlalchemy import Column, Integer, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship, mapped_column
from datetime import datetime, date as date_type, timedelta
from decimal import Decimal, ROUND_HALF_UP
from base import Base

class Transaction(Base):
    __tablename__ = 'transactions'
    id = mapped_column(Integer, primary_key=True)
    account_number = mapped_column(Integer, ForeignKey('accounts.account_number'))
    amount = mapped_column(Float(asdecimal=True))
    date = mapped_column(DateTime)
    interest=mapped_column(Boolean)

    account = relationship("Account", back_populates="transactions")

    def __init__(self, amount, date, interest=False):
        """Initialize a transaction"""

        # self.date = date
        if isinstance(date, str):
            self.date = datetime.strptime(date, "%Y-%m-%d")
        elif isinstance(date, date_type):
            self.date = datetime.combine(date, datetime.min.time())
        else:
            self.date = date

        self.amount = Decimal(str(amount))
        self.interest = interest

    def __str__(self):
        """String representation of the transaction."""

        # create a "display" version of amount that is a rounded amount
        display_amount = self.amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        date = self.date.strftime("%Y-%m-%d")
        return f"{date}, ${display_amount:,.2f}"
    
    def is_interest(self):
        return self.interest
    
    def in_same_day(self, other):
        "Takes in a date object and checks whether this transaction shares the same date"
        return self.date == other.date

    def in_same_month(self, other):
        "Takes in a date object and checks whether this transaction shares the same month and year"
        return self.date.month == other.date.month and self.date.year == other.date.year

    def __radd__(self, other):
        return other + self.amount

    def check_balance(self, balance):
        # if (self.amount >= 0 or balance >= abs(self.amount)):
        #     return True
        # else:
        #     raise OverdrawError()
        if self.interest:
            return True
        return self.amount >= 0 or balance >= abs(self.amount)
    
    def __lt__(self, value):
        return self.date < value.date
    
    def last_day_of_month(self):
        "Returns a date corresponding to the last day in the same month as this transaction"
        # first_of_next_month = date(self.date.year + self.date.month // 12,
        #                         self.date.month % 12 + 1, 1)
        # return first_of_next_month - timedelta(days=1)

        first_of_next_month = self.date.replace(day=28) + timedelta(days=4)
        return first_of_next_month - timedelta(days=first_of_next_month.day)

