import sys
import pickle
from datetime import datetime
from decimal import Decimal, InvalidOperation
from overdraw_error import OverdrawError
from bank import Bank


class BankCLI:
    """Display a menu and respond to choices when run"""

    def __init__(self):
        self._bank = Bank()

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
        current_account = "None"
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
        self._bank.new_account(account_type)


    def _summary(self):
        accounts = self._bank.all_accounts()
        for account in accounts:
            print(account)

    def _select_account(self):
        print("Enter account number")
        account_number = input(">")

        # retrieve account from account list
        selected_account = self._bank.fetch_account(account_number)
        
        # check if account does not exist
        if not selected_account:
            return
        
        # format account info (type, number, balance) to be printed in menu
        selected_account_formated = self._bank.format_account(selected_account)

        # update current account variables
        self._current_account = selected_account
        self._current_account_formated = selected_account_formated

    def _add_transaction(self):

        while True:
            print("Amount?")
            amount = input(">")
            try:
                amount = Decimal(amount)
                break
            except InvalidOperation:
                print("Please try again with a valid dollar amount.")


        while True:
            print("Date? (YYYY-MM-DD)")
            date = input(">")
            try:
                datetime.strptime(date, "%Y-%m-%d")
                break
            except ValueError:
                print("Please try again with a valid date in the format YYYY-MM-DD")
            
        
        try:
            self._bank.new_transaction(amount, date, self._current_account)
        except AttributeError:
            print("This command requires that you first select an account")
            return
        except OverdrawError:
            print("This transaction could not be completed due to an insufficent account balance.")
            return


        # update current account string with new balance
        self._current_account_formated = self._bank.format_account(self._current_account)

    def _list_transactions(self):
        try:
            self._bank.list_transactions(self._current_account)
        except AttributeError:
            print("This command requires that you first select an account")

    def _interest_and_fees(self):
        try:
            self._bank.interest_and_fees(self._current_account)
        except AttributeError:
            print("This command requires that you first select an account")

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

        # restore current account
        self._current_account = current_account
        self._current_account_formated = current_format

    def _load(self):
        with open("bank_save.pickle", "rb") as f:   
            self._bank = pickle.load(f)
    
    def _quit(self):
        sys.exit(0)

if __name__ == "__main__":
    BankCLI().run()