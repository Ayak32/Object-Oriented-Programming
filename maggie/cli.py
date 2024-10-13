import sys
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from bank import Bank
from base import Base
from datetime import datetime
from decimal import InvalidOperation
from accounts import OverdrawError, TransactionLimitError, TransactionSequenceError


# repl parts modeled off notebook example from class

class BankCLI:
    """Display a menu and respond to choices when run."""

    def __init__(self):
        engine = create_engine("sqlite:///bank.db")
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self._session = Session()
        logging.debug(f"Saved to bank.db")

        self.bank = Bank(self._session)
        self.current_account = None
        self.choices = {
            "1": self.open_account,
            "2": self.summary,
            "3": self.select_account,
            "4": self.add_transaction,
            "5": self.list_transactions,
            "6": self.interest_and_fees,
            "7": self.quit,
        }

    def display_menu(self):
        """Display the bank menu options """

        print("--------------------------------")
        if self.current_account != None:
            print("Currently selected account: " + self.current_account.account_info())
        else:
            print("Currently selected account: None")
        print(

"""Enter command
1: open account
2: summary
3: select account
4: add transaction
5: list transactions
6: interest and fees
7: quit
>""", end='')

    def run(self):
        """Display the menu and respond to choices."""

        while True:
            self.display_menu()
            choice = input("")
            action = self.choices.get(choice)
            if action:
                action()
            else:
                print("{0} is not a valid choice".format(choice))

    def open_account(self):
        """Open a new account of type checking or savings"""

        type = input("Type of account? (checking/savings)\n>")
        # if type:
        self.bank.open_account(type)
        # else:
            # print("{0} is not a valid type".format(type))

    def summary(self):
        """Print a summary of all accounts in the bank with their current balance"""

        self.bank.summary()

    def select_account(self):
        """Change the current account to the account with number entered by user"""

        acc_num = input("Enter account number\n>")
        account = self.bank.select_account(acc_num)
        self.current_account = account

    def add_transaction(self):
        """Add a transaction with a user-specified date and amount to currently selected account"""
        while True:
            try:
                amount = float(input("Amount?\n>"))
                # print(amount)
                break
            except (ValueError, InvalidOperation):
                print("Please try again with a valid dollar amount.")

        while True:
            try:
                date = input("Date? (YYYY-MM-DD)\n>")
                date = datetime.strptime(date, "%Y-%m-%d").date()
                break
            except ValueError:
                print("Please try again with a valid date in the format YYYY-MM-DD.")
        try:
            self.current_account.add_transaction(amount, date)
            self._session.commit()
            logging.debug(f"Saved to bank.db")
        except AttributeError:
            print("This command requires that you first select an account.")
        except OverdrawError as err:
            print(err.message)
        except TransactionLimitError as err:
            print(err.message + err.limit)
        except TransactionSequenceError as err:
            date = err.latest_date.strftime("%Y-%m-%d")
            print(f"New transactions must be from {date} onward.")

    def list_transactions(self):
        """Print a list of all transactions on the currently selected account"""

        try:
            self.current_account.list_transactions()
        except AttributeError:
            print("This command requires that you first select an account.")

    def interest_and_fees(self):
        """Apply 1 month of interest to the currently selected account"""

        try:
            logging.debug("Triggered interest and fees")
            self.current_account.interest_and_fees()
            self._session.commit()
            logging.debug(f"Saved to bank.db")
        # except AttributeError:
        #     print("This command requires that you first select an account.")
        # except AttributeError:
        #     print("This command requires that you first select an account.")
        except TransactionSequenceError as err:
            month = err.latest_date.strftime("%B")
            print(f"Cannot apply interest and fees again in the month of {month}.")


    # def save(self):
    #     """Store the current bank details into a pickle file"""

    #     with open("bank.pickle", "wb") as f:
    #         pickle.dump(self.bank, f)
    #         logging.debug("Saved to bank.pickle")

    # def load(self):
    #     """Load the stored bank information from the pickle file"""

    #     with open("bank.pickle", "rb") as f:   
    #         self.bank = pickle.load(f)
    #         logging.debug("Loaded from bank.pickle")

    def quit(self):
        """Quit the bank program."""
        self._session.close()
        sys.exit(0)


if __name__ == "__main__":
    # logging.basicConfig(filename='bank.log', level=logging.DEBUG, format='%(asctime)s|%(levelname)s|%(message)s')
    logging.basicConfig(
        filename='bank.log', 
        level=logging.DEBUG, 
        format='%(asctime)s|%(levelname)s|%(message)s',
        datefmt='%Y-%m-%d %H:%M:%S' 
    )
    try:
        BankCLI().run()
    except (Exception, KeyboardInterrupt) as e:
        error = str(e).replace('\n', '\\n')
        logging.error(f'{type(e).__name__}: {error}')

        # log_message = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}|ERROR|{type(e).__name__}: {error}"

        # logging.error(f'{datetime.now()}{type(e).__name__}: {error}')
        print("Sorry! Something unexpected happened. Check the logs or contact the developer for assistance.")
        # log message however we do that
        # logging.error()
        sys.exit(0)