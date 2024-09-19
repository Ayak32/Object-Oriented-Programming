import sys
import pickle
from bank import Bank


class BankCLI:
    """Display a menu and respond to choices when run"""

    def __init__(self):
        self._bank = Bank()
        self._current_account_formated = "None"
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

        selected_account = self._bank.fetch_account(account_number)
        selected_account_formated = self._bank.format_account(selected_account)

        self._current_account = selected_account
        self._current_account_formated = selected_account_formated


    # FIX
    def _add_transaction(self):
        print("Amount?")
        amount = input(">")
        print("Date? (YYYY-MM-DD)")
        date = input(">")
        
        self._bank.new_transaction(amount, date, self._current_account)
        self._current_account_formated = self._bank.format_account(self._current_account)

    def _list_transactions(self):
        self._bank.list_transactions(self._current_account)

    def _interest_and_fees(self):
        return


    def _save(self):
        self._current_account = ""
        self._current_account_formated = "None"
        with open("bank_save.pickle", "wb") as f:
            pickle.dump(self._bank, f)

    def _load(self):
        with open("bank_save.pickle", "rb") as f:   
            self._bank = pickle.load(f)
    
    def _quit(self):
        sys.exit(0)

if __name__ == "__main__":
    BankCLI().run()