
from sqlalchemy.orm import Session
from sqlalchemy import func
from accounts import CheckingAccount, SavingsAccount, Account
from base import Base
import logging


class Bank(Base):
    def __init__(self, session):
        """Create a new account"""

        # self.accounts = []  # list to store all accounts
        self.session = session
        self.next_account_number = self.get_next_account_number()  # start for account numbers
    
    def get_next_account_number(self):
        max_account = self.session.query(func.max(Account.account_number)).scalar()
        # INCOMPLETE
        logging.debug(f"Loaded from bank.db")
        return max_account + 1 if max_account else 1

    def open_account(self, account_type):
        """Create and add a new Checking or Savings account."""

        # initialize a new account object of type account_type # with account number self.next_account_number
        if account_type == "checking":
            # initialize checking account
            new_account = CheckingAccount(self.next_account_number)
        elif account_type == "savings":
            # initialize savings account
            new_account = SavingsAccount(self.next_account_number)
        else:
            return None
        # append the account to the list of all accounts
        # self.accounts.append(new_account)
        self.session.add(new_account)
        self.session.commit()
        logging.debug(f"Saved to bank.db")
        logging.debug(f"Created account: {new_account.account_number}")
        # increment next account number 
        self.next_account_number += 1

    def summary(self):
        """Print information about each account in the bank"""
        accounts = self.session.query(Account).all()
        # INCOMPLETE
        logging.debug(f"Loaded from bank.db")
        for account in accounts:
            print(account.account_info())

    def select_account(self, account_number):
        """Retrieve an account by account number."""
        account = self.session.query(Account).filter_by(account_number=int(account_number)).first()
        # logging.debug() INCOMPLETE
        logging.debug(f"Loaded from bank.db")
        # print(type(account)) 
        return account
        # account_number = int(account_number)
        # for account in self.accounts:
        #     if account.account_number == account_number:
        #         return account
