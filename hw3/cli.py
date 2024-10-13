import sys
import pickle
from datetime import datetime
from decimal import Decimal, InvalidOperation
from overdraw_error import OverdrawError
from transaction_sequence_error import TransactionSequenceError
from transaction_limit_error import TransactionLimitError
import logging
from bank import Bank

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base



# Base = declarative_base()

logging.basicConfig(filename='bank.log', level=logging.DEBUG, format='%(asctime)s|%(levelname)s|%(message)s',
        datefmt='%Y-%m-%d %H:%M:%S')


class BankCLI:
    """Display a menu and respond to choices when run"""

    def __init__(self):
        engine = create_engine("sqlite:///bank.db")
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self._session = Session()
        logging.debug(f"Saved to bank.db")


        self._bank = Bank(self._session)

        # stores the current account as a string to be printed in menu
        self._current_account_formated = "None"

        # later replaced with an account
        self._current_account = ""

        self._choices = {
            "1": self._open_account,
            "2": self._summary,
            "3": self._select_account,
            "4": self._add_transaction,
            "5": self._list_transactions,
            "6": self._interest_and_fees,
            "7": self._save,
            "8": self._load,
            "9": self._quit
        }

    def _display_menu(self):
        print(
"""--------------------------------
Currently selected account: """ + self._current_account_formated +
"""
Enter command
1: open account
2: summary
3: select account
4: add transaction
5: list transactions
6: interest and fees
7: save
8: load
9: quit""", 
        )

    def run(self):
        """Display the menu and respond to choices."""
        # current_account = "None"
        while True:
            self._display_menu()
            choice = input(">")
            action = self._choices.get(choice)
            if action:
                action()
            else:
                print("{0} is not a valid choice".format(choice))
    
    def _open_account(self):
        print("Type of account? (checking/savings)")
        account_type = input(">")
        account = self._bank.new_account(account_type)
        account_number = account.number
        logging.debug(f"Created account: {account_number}")


    def _summary(self):
        accounts = self._bank.all_accounts()
        for account in accounts:
            print(account)

    def _select_account(self):
        print("Enter account number")
        account_number = input(">")

        selected_account = self._bank.select_account(account_number) 
        # retrieve account from account list
        # selected_account = self._bank.fetch_account(account_number)

        # check if account does not exist
        if not selected_account:
            return
        
        # format account info (type, number, balance) to be printed in menu
        selected_account_formated = self._bank.format_account(selected_account)

        # update current account variables
        self._current_account = selected_account
        self._current_account_formated = selected_account_formated

    def _add_transaction(self):

        # program prompts user for Amount until provide a valid dollar amount
        while True:
            print("Amount?")
            amount = input(">")
            try:
                amount = Decimal(amount)
                break
            except InvalidOperation:
                print("Please try again with a valid dollar amount.")

        # program prompts user for Date until provide a valid date in the format YYYY-MM-DD
        while True:
            print("Date? (YYYY-MM-DD)")
            date = input(">")
            try:
                date = datetime.strptime(date, "%Y-%m-%d")
                break
            except ValueError:
                print("Please try again with a valid date in the format YYYY-MM-DD.")
            
        # program attempts to add a new transaction and checks for exceptions related to this action
        try:
            self._bank.new_transaction(amount, date, self._current_account)
            self._session.commit()
            logging.debug(f"Saved to bank.db")
        except AttributeError:
            print("This command requires that you first select an account.")
            return
        except OverdrawError:
            print("This transaction could not be completed due to an insufficient account balance.")
            return
        except TransactionLimitError as e:
            if e.limit == "daily":
                print("This transaction could not be completed because this account already has 2 transactions in this day.")
            else:
                print("This transaction could not be completed because this account already has 5 transactions in this month.")
        except TransactionSequenceError as s:
            if s.error == "normalSequenceError":
                print(f"New transactions must be from {s.latest_date.strftime('%Y-%m-%d')} onward.")

        logging.debug(f"Created transaction: {self._current_account.number}, {amount}")



        # update current account string with new balance
        self._current_account_formated = self._bank.format_account(self._current_account)

    def _list_transactions(self):
        try:
            sorted_transactions = self._bank.list_transactions(self._current_account)
            for tran in sorted_transactions:
                print(tran)
        except AttributeError:
            print("This command requires that you first select an account.")

        
    def _interest_and_fees(self):
        try:
            self._bank.interest_and_fees(self._current_account)
            self._session.commit()
            logging.debug(f"Saved to bank.db")
        except AttributeError:
            print("This command requires that you first select an account.")
        except TransactionSequenceError as s:
            print(f"Cannot apply interest and fees again in the month of {s.latest_date}.")

        logging.debug("Triggered interest and fees")
        # update current account string with new balance
        self._current_account_formated = self._bank.format_account(self._current_account)

    def _save(self):
        # store current account to be re-set after saving the file
        current_account = self._current_account
        current_format = self._current_account_formated

        # reset current account variables to reflect no account selected when file is loaded
        self._current_account = ""
        self._current_account_formated = "None"
        with open("bank_save.pickle", "wb") as f:
            pickle.dump(self._bank, f)
            logging.debug("Saved to bank.pickle")

        # restore current account
        self._current_account = current_account
        self._current_account_formated = current_format

    def _load(self):
        with open("bank_save.pickle", "rb") as f:   
            self._bank = pickle.load(f)
            logging.debug("Loaded from bank.pickle")
    
    def _quit(self):
        self._session.close()
        sys.exit(0)

if __name__ == "__main__":
    try:
        BankCLI().run()

    except Exception as e:
        # handles  non-system exceptions
        print(f"Sorry! Something unexpected happened. Check the logs or contact the developer for assistance.")
        
        # Log the exception type and message
        exception_type = type(e).__name__
        exception_message = repr(e).replace('\n', '\\n')
        logging.error(f"{exception_type}: {exception_message}")
        sys.exit(0)