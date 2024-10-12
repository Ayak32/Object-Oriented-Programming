# import tkinter as tk
# #import tkinter.tkk as tkk
# from account_entry import AccountEntry
# from account import Account

# class AccountButton(tk.Frame):

#     def __init__(self, list_frame, account, **kwargs):
#         super().__init__(list_frame, **kwargs)
#         self._account_number = account._number
#         self._account_type = account._type

#         self._edit_button = tk.Button(
#             self, command=self._modify_account)



#         self._edit_button = tk.Button(self,command=self._select_account)

#         self._edit_button.pack()
#         self.update(account)



#     def _select_button(self, value):
#         # your code here
#         return


#     # def _modify_account(self):
#     #     AccountEntry(self.master.master, self).grid(row=1, column=1)

#     def format_account(self):
#         """Format the account details as a string with the account type, padded account number,
#         and the current balance.
        
#         Returns:
#             str: A formatted string representing the account details.
#         """
#         type = self._type.capitalize()
#         number = self._number
#         balance = self._balance
#         # Pad the account number to 9 digits
#         padded_account_number = f"{number:09}"
#         # Format the balance with commas and 2 decimal places
#         formatted_balance = f"${balance:,.2f}"
#         return f"{type}#{padded_account_number},\tbalance: {formatted_balance}"

#     def update(self, account):
#         """ Used to update this widget to display the current text of the
#         associated note """
        
#         self._edit_button.configure(text=account.format_account())






import tkinter as tk
# import tkinter.tkk as tkk
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
        balance = account.get_balance()  # Ensure you have a method to get balance
        # Pad the account number to 9 digits
        padded_account_number = f"{number:09}"
        # Format the balance with commas and 2 decimal places
        formatted_balance = f"${balance:,.2f}"
        return f"{type}#{padded_account_number},\tbalance: {formatted_balance}"

    def update(self, account):
        """Used to update this widget to display the current text of the associated note."""
        self._edit_button.configure(text=account.format_account())



































# import tkinter as tk
# #import tkinter.tkk as tkk
# from account_entry import AccountEntry
# from account import Account

# class AccountButton(tk.Frame):

#     def __init__(self, list_frame, account, **kwargs):
#         super().__init__(list_frame, **kwargs)
#         self._account_number = account._number
#         self._account_type = account._type

#         # self._edit_button = tk.Button(
#         #     self, command=self._modify_account)

#         # Create an IntVar to associate with the Radiobuttons
#         self._radio_var = tk.IntVar(value=None)

#         #self._edit_button = tkk.Radiobutton(list_frame, variable=self._radio_var,command=self._modify_account)
#         self._edit_button = tk.Radiobutton(
#             self, 
#             variable=self._radio_var,  # Associate the Radiobutton with _radio_var
#             value=self._account_number,  # Unique value for each account (use account number)
#             command=lambda: self._toggle_button(self._account_number)  # Use the toggle function when clicked
#         )
#         self._edit_button.pack()
#         self.update(account)



#     def _toggle_button(self, value):
#         if self._radio_var.get() == value:
#             self._radio_var.set(None)  # Unselect
#         else:
#             self._radio_var.set(value)
        

#     def _modify_account(self):
#         AccountEntry(self.master.master, self).grid(row=1, column=1)

#     def format_account(self):
#         """Format the account details as a string with the account type, padded account number,
#         and the current balance.
        
#         Returns:
#             str: A formatted string representing the account details.
#         """
#         type = self._type.capitalize()
#         number = self._number
#         balance = self._balance
#         # Pad the account number to 9 digits
#         padded_account_number = f"{number:09}"
#         # Format the balance with commas and 2 decimal places
#         formatted_balance = f"${balance:,.2f}"
#         return f"{type}#{padded_account_number},\tbalance: {formatted_balance}"

#     def update(self, account):
#         """ Used to update this widget to display the current text of the
#         associated note """
        
#         self._edit_button.configure(text=account.format_account())