from savings_account import SavingsAccount 
from checking_account import CheckingAccount 
from account import Account
from base import Base
from sqlalchemy.orm import Session
from sqlalchemy import func
import logging


class Bank():
    """Manages a collection of savings and checking accounts. It supports
    creating new accounts, handling transactions, applying interest and fees, and fetching 
    or formatting account information."""
    # def __init__(self):
    #     """Initialize the Bank class with an empty list of accounts and a counter for account numbers."""
    #     self._accounts = []
    #     self._count = 0
 

    def __init__(self, session):
        self.session = session
        self._count = self._increment_count()  

    def _increment_count(self):
        current_count = self.session.query(func.max(Account.number)).scalar()

        logging.debug(f"Loaded from bank.db")
        if current_count:
            return current_count + 1
        else:
            return 1


    def new_account(self, account_type):
        """Create a new account of the specified type (savings or checking).
        
        Args:
            account_type (str): The type of account to create ("savings" or "checking").
        """
        # Increment count to allow for a unique account number
        
        if account_type == "savings":
            # self._count += 1
            new_account = SavingsAccount(self._count)
        elif account_type == "checking":
            # self._count += 1
            new_account = CheckingAccount(self._count)
        else:
            return None

        self.session.add(new_account)
        self.session.commit()
        logging.debug(f"Saved to bank.db")
        logging.debug(f"Created account: {new_account.number}")
        self._count += 1
        return new_account
        


    def new_transaction(self, amount, date, account):
        """Add a new transaction to the selected account.
        
        Args:
            amount (str): The transaction amount.
            date (str): The date of the transaction.
            account (Account): The account object where the transaction will occur.
        """
    
        account.verify_transaction(amount, date)



    def list_transactions(self, account):
        """List all transactions for the selected account.
        
        Args:
            account (Account): The account object whose transactions will be listed.
        """
        return account.list_transactions()

    def interest_and_fees(self, account):
        """Apply interest and fees for the selected account.
        
        Args:
            account (Account): The account object to which interest and fees will be applied.
        """
        account.interest_and_fees()
        
        
    def fetch_account(self, account_number):
        """Fetch the account object for the given account number.
        
        Args:
            account_number (str): The number of the account to retrieve.
        
        Returns:
            Account: The account object if found, None if the account does not exist.
        """
        # Check for invalid account number
        if int(account_number) > self._count or int(account_number) <= 0:
            print("Account Does Not Exist")
            return
        for account in self._accounts:
            if account.number_matches(account_number):
                return account

    def format_account(self, account):
        """Format and return the account details as a string.
        
        Args:
            account (Account): The account object to format.
        
        Returns:
            str: The formatted account details.
        """
        return account.format_account()
    
    def select_account(self, account_number):
        logging.debug(f"Loaded from bank.db")
        return self.session.query(Account).filter_by(number=int(account_number)).first()

    def all_accounts(self):
        """Format and return a list of all accounts in the bank.
        
        Returns:
            list: A list of formatted account details (type, number, balance).
        """
        accounts = self.session.query(Account).all()
        logging.debug(f"Loaded from bank.db")
        formated_accounts_list = []
        for account in accounts:
            # Format account and add to list
            formated_accounts_list.append(account.format_account())

        return formated_accounts_list
