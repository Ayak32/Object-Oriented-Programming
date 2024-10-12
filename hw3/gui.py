import tkinter as tk
from tkinter import ttk
from account_button import AccountButton

import sys
from datetime import datetime
from decimal import Decimal, InvalidOperation
from overdraw_error import OverdrawError
from transaction_sequence_error import TransactionSequenceError
from transaction_limit_error import TransactionLimitError
import logging
from bank import Bank


logging.basicConfig(filename='bank.log', level=logging.DEBUG, format='%(asctime)s|%(levelname)s|%(message)s',
        datefmt='%Y-%m-%d %H:%M:%S')


class BankGUI:
    """Display a menu and respond to choices when run"""

    def __init__(self):

        self._window = tk.Tk()
        self._window.title("MY BANK")
        

        self._bank = Bank()
        self._options_frame = tk.Frame(self._window)
        self._window.geometry("500x200")


        # stores the current account as a string to be printed in menu
        self._current_account_formatted = "None"

        # later replaced with an account
        self._current_account = ""

        tk.Button(self._options_frame, text="Open Account", command=self._open_account).grid(row=1, column=1)
        tk.Button(self._options_frame, text="Add Transaction", command=self._add_transaction).grid(row=1, column=2)
        tk.Button(self._options_frame, text="Interests and Fees", command=self._interest_and_fees).grid(row=1, column=3)
        
        self._list_frame = tk.Frame(self._window)
        self._options_frame.grid(row=0, column=1,columnspan=2)
        self._list_frame.grid(row=1, column=1, columnspan=1, sticky="w")

        self._window.mainloop()

    def _open_account(self):  
        # Callback function for the "Enter" button
        def add_callback():
            selected_account_type = dropdown_var.get()
            if selected_account_type == "Select Account Type":
                return

            # Simulate the process of opening an account (you can modify this part)
            account = self._bank.new_account(selected_account_type)
            AccountButton(self._list_frame, account).pack()
            
            
            logging.debug(f"Created account: {account._number}")

            # Remove the dropdown and buttons after opening the account
            account_frame.grid_forget()
        
        # Callback function for the "Cancel" button
        def cancel_callback():
            account_frame.grid_forget()

        
        # Create a frame for the dropdown and buttons
        account_frame = tk.Frame(self._options_frame, relief="solid", bd=1)
        account_frame.grid(row=2, column=0, columnspan=3, padx=5, pady=5)

        # Variable for the dropdown selection
        dropdown_var = tk.StringVar(self._window)
        dropdown_var.set("Select Account Type")  # Set default value

        # Options for the dropdown menu
        options = ["checking", "savings"]

        # Create the dropdown menu
        dropdown = tk.OptionMenu(account_frame, dropdown_var, *options)
        dropdown.grid(row=0, column=0, padx=5, pady=5) 

        # "Enter" button to confirm the action
        enter_b = tk.Button(account_frame, text="Enter", command=add_callback)
        enter_b.grid(row=0, column=1, padx=5, pady=5)

        cancel_b = tk.Button(account_frame, text="Cancel", command=cancel_callback)
        cancel_b.grid(row=0, column=2, padx=5, pady=5)

        # Resize the columns to fit the buttons nicely
        account_frame.grid_columnconfigure(0, weight=1)
        account_frame.grid_columnconfigure(1, weight=1)
        account_frame.grid_columnconfigure(2, weight=1)







    # def _summary(self):
    #     accounts = self._bank.all_accounts()
    #     for account in accounts:
    #         print(account)

    # def _select_account(self):
    #     print("Enter account number")
    #     account_number = input(">")

    #     # retrieve account from account list
    #     selected_account = self._bank.fetch_account(account_number)
        
    #     # check if account does not exist
    #     if not selected_account:
    #         return
        
    #     # format account info (type, number, balance) to be printed in menu
    #     selected_account_formated = self._bank.format_account(selected_account)

    #     # update current account variables
    #     self._current_account = selected_account
    #     self._current_account_formated = selected_account_formated

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

        logging.debug(f"Created transaction: {self._current_account._number}, {amount}")



        # update current account string with new balance
        self._current_account_formated = self._bank.format_account(self._current_account)

    # def _list_transactions(self):
    #     try:
    #         self._bank.list_transactions(self._current_account)
    #     except AttributeError:
    #         print("This command requires that you first select an account.")

    def _interest_and_fees(self):
        try:
            self._bank.interest_and_fees(self._current_account)
        except AttributeError:
            print("This command requires that you first select an account.")
        except TransactionSequenceError as s:
            print(f"Cannot apply interest and fees again in the month of {s.latest_date}.")

        logging.debug("Triggered interest and fees")
        # update current account string with new balance
        self._current_account_formated = self._bank.format_account(self._current_account)

    # def _save(self):
    #     # store current account to be re-set after saving the file
    #     current_account = self._current_account
    #     current_format = self._current_account_formated

    #     # reset current account variables to reflect no account selected when file is loaded
    #     self._current_account = ""
    #     self._current_account_formated = "None"
    #     with open("bank_save.pickle", "wb") as f:
    #         pickle.dump(self._bank, f)
    #         logging.debug("Saved to bank.pickle")

    #     # restore current account
    #     self._current_account = current_account
    #     self._current_account_formated = current_format

    # def _load(self):
    #     with open("bank_save.pickle", "rb") as f:   
    #         self._bank = pickle.load(f)
    #         logging.debug("Loaded from bank.pickle")
    
    # def _quit(self):
    #     sys.exit(0)

if __name__ == "__main__":
    try:
        BankGUI()

    except Exception as e:
        # handles  non-system exceptions
        print(f"Sorry! Something unexpected happened. Check the logs or contact the developer for assistance.")
        
        # Log the exception type and message
        exception_type = type(e).__name__
        exception_message = repr(e).replace('\n', '\\n')
        logging.error(f"{exception_type}: {exception_message}")
        sys.exit(0)


