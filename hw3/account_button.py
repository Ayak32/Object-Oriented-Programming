import tkinter as tk
from account_entry import AccountEntry
from account import Account

class AccountButton(tk.Frame):

    def __init__(self, list_frame, account, **kwargs):
        super().__init__(list_frame, **kwargs)
        self._account_number = account._number
        self._account_type = account._type

        # Create a StringVar to keep track of the selected account
        self._selected_var = tk.StringVar(value="")

        # Create the radio button
        self._edit_button = tk.Radiobutton(
            self,
            text=account.format_account(),
            variable=self._selected_var,
            value=self._account_number,
            command=self._select_account,
            indicatoron=0,  # Makes the button look like a regular button
            selectcolor="green"  # Change the color of the button when selected
        )
        self._edit_button.pack()
        
        # Update the display with account information
        self.update(account)

    def _select_account(self):
        # Change button color when selected
        self._edit_button.configure(bg="green")

        for widget in self.master.winfo_children():
            if isinstance(widget, AccountButton) and widget != self:
                widget._edit_button.configure(bg=self.master.cget("bg")) 

    def format_account(self):
        """Format the account details as a string with the account type, padded account number,
        and the current balance.
        
        Returns:
            str: A formatted string representing the account details.
        """
        type = self._account_type.capitalize()
        number = self._account_number
        balance = self.get_balance()  # Ensure you have a method to get balance
        # Pad the account number to 9 digits
        padded_account_number = f"{number:09}"
        # Format the balance with commas and 2 decimal places
        formatted_balance = f"${balance:,.2f}"
        return f"{type}#{padded_account_number},\tbalance: {formatted_balance}"

    def update(self, account):
        """Used to update this widget to display the current text of the associated note."""
        self._edit_button.configure(text=account.format_account())
