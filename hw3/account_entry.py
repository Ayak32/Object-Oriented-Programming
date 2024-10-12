import tkinter as tk

class AccountEntry(tk.Frame):
    """ A 'megawidget' for entering note details """

    def __init_(self, parent, account_button, **kwargs):
        super().__init__(parent, **kwargs)

        self._account_button = account_button


        print("here")