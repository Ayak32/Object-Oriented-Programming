import sys
import tkinter as tk
from tkinter import ttk
import logging
# import pickle
from datetime import datetime
from bank import Bank
import tkinter.messagebox as messagebox
from accounts import OverdrawError, TransactionLimitError, TransactionSequenceError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from accounts import Account
from base import Base

# class Base(DeclarativeBase):
#     pass

class Menu:
    """Display a menu and respond to choices when run."""

    def __init__(self):
        self._window = tk.Tk()
        self._window.title("MY BANK")
        self._window.report_callback_exception = self.handle_exception

        engine = create_engine("sqlite:///bank.db")
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self._session = Session()
        logging.debug(f"Saved to bank.db")

        self._bank = Bank(self._session)
        self._current_account = None
        self._current_account_var = tk.StringVar()
        # self._theme_manager = ThemeManager()
        # self._current_theme = 'light'

        # self._style = ttk.Style()
        # self._style.theme_use('clam')

        self._options_frame = tk.Frame(self._window)
        self._options_frame.grid(row=0, column=1, columnspan=2)

        self._dynamic_frame = tk.Frame(self._window)
        self._dynamic_frame.grid(row=1, column=1, columnspan=2, sticky="nsew")

        self._accounts_frame = tk.Frame(self._window)
        self._accounts_frame.grid(row=2, column=1, sticky="nsew")

        self._transactions_frame = tk.Frame(self._window)
        self._transactions_frame.grid(row=2, column=2, sticky="nsew")

        tk.Button(self._options_frame, text="open account", 
                command=self._open_account).grid(row=1, column=1)
        tk.Button(self._options_frame, text="add transaction", 
                command=self._add_transaction).grid(row=1, column=2)
        tk.Button(self._options_frame, text="interest and fees", 
                command=self._interest_and_fees).grid(row=1, column=3)
        # tk.Button(self._options_frame, text="save", 
        #         command=self._save).grid(row=1, column=4)
        # tk.Button(self._options_frame, text="load", 
        #         command=self._load).grid(row=1, column=5)
        # tk.Button(self._options_frame, text="toggle theme", 
        #           command=self._toggle_theme).grid(row=1, column=6)

        # self._apply_theme()
        self._window.mainloop()

    # def _toggle_theme(self):
    #     if self._current_theme == 'light':
    #         self._current_theme = 'dark'
    #     else:
    #         self._current_theme = 'light'
    #     self._apply_theme()

    # def _apply_theme(self):
        # if self._current_theme == 'light':
        #     theme = ThemeManager.LIGHT_THEME
        # else:
        #     theme = ThemeManager.DARK_THEME
        
        # self._style.configure('TFrame', background=theme['bg'])
        # self._style.configure('TLabel', background=theme['bg'], foreground=theme['fg'])
        # self._style.configure('TButton', background=theme['button_bg'], 
        #                      foreground=theme['button_fg'])
        # self._style.configure('TRadiobutton', background=theme['bg'], 
        #                      foreground=theme['fg'])
        
        # self._window.configure(bg=theme['bg'])
        
        # for frame in (self._options_frame, self._dynamic_frame, 
        #              self._accounts_frame):
        #     for widget in frame.winfo_children():
        #         if isinstance(widget, tk.Frame):
        #             widget.configure(style='TFrame')
        #         elif isinstance(widget, tk.Label):
        #             widget.configure(style='TLabel')
        #         elif isinstance(widget, tk.Button):
        #             widget.configure(style='TButton')
        #         elif isinstance(widget, tk.Radiobutton):
        #             widget.configure(style='TRadiobutton')
        # for frame in self._transactions_frame:
        #     for widget in frame.winfo_children():
                
        # self._style.configure('Valid.TEntry', fieldbackground=theme['valid_bg'])
        # self._style.configure('Invalid.TEntry', fieldbackground=theme['invalid_bg'])

        # self._style.configure('Positive.TLabel', 
        #                       background=theme['transaction_positive'], 
        #                       foreground=theme['button_fg'])
        # self._style.configure('Negative.TLabel', 
        #                       background=theme['transaction_negative'],
        #                       foreground=theme['button_fg'])

    def _clear_dynamic_frame(self):
        """Helper method to clear dynamic content area."""
        for widget in self._dynamic_frame.winfo_children():
            widget.destroy()

    def _open_account(self):
        self._clear_dynamic_frame()
        tk.Label(self._dynamic_frame, text="account type:").grid(row=2, column=1)

        account_type = tk.StringVar(value="checking")  # default to checking
        tk.Radiobutton(self._dynamic_frame, text="Checking", variable=account_type, value="checking").grid(row=3, column=1)
        tk.Radiobutton(self._dynamic_frame, text="Savings", variable=account_type, value="savings").grid(row=3, column=2)

        tk.Button(self._dynamic_frame, text="Enter", command=lambda: self._confirm_account(account_type.get())).grid(row=4, column=1)

        tk.Button(self._dynamic_frame, text="Cancel", command=self._clear_dynamic_frame).grid(row=4, column=2)

    def _confirm_account(self, account_type):
        self._bank.open_account(account_type)
        self._session.commit()
        logging.debug(f"Saved to bank.db")
        self._clear_dynamic_frame() 
        self._display_accounts()

    def _display_accounts(self):
        """Displays a list of accounts in the bank."""
        for widget in self._accounts_frame.winfo_children():
            widget.destroy()  
        
        accounts = self._session.query(Account).all()
        logging.debug(f"Loaded from bank.db")

        if not accounts:  
            pass
        else:
            row = 0
            for account in accounts:
                account_num = str(account.account_number)        
                tk.Radiobutton(self._accounts_frame, text=str(account), 
                                variable=self._current_account_var, value=account_num, 
                                command=lambda acc=account: self._select_account(acc) 
                                ).grid(row=row, column=1)
                row += 1

            if self._current_account:
                self._current_account_var.set(str(self._current_account.account_number))


    def _display_transactions(self):
        for widget in self._transactions_frame.winfo_children():
            widget.destroy()
        if self._current_account is not None:
            tk.Label(self._transactions_frame, 
                      text=f"Transactions for Account {self._current_account.account_number}:",
                     ).grid(row=0, column=1, sticky="w")
            if self._current_account.transactions:
                row = 1
                for t in self._current_account.transactions:
                    bg_color = "dark green" if t.amount >= 0 else "dark red"
                    # theme_style = 'Positive.TLabel' if t.amount >= 0 else 'Negative.TLabel'
                    tk.Label(self._transactions_frame, text=str(t), 
                              bg=bg_color).grid(row=row, column=1, sticky="w")
                    row += 1
            else:
                tk.Label(self._transactions_frame, text="No transactions for this account.").grid(row=1, column=1, sticky="w")
        else:
            tk.Label(self._transactions_frame, text="No account selected.").grid(row=0, column=1, sticky="w")


    def _select_account(self, acc):
        self._current_account = acc
        self._display_accounts()
        self._display_transactions()

    def _add_transaction(self):
        self._clear_dynamic_frame()

        tk.Label(self._dynamic_frame, text="Transaction Amount:").grid(row=1, column=1)
        self.amount_entry = tk.Entry(self._dynamic_frame)
        self.amount_entry.grid(row=1, column=2)
        self.amount_entry.bind("<KeyRelease>", self._validate_inputs)

        tk.Label(self._dynamic_frame, text="Transaction Date:").grid(row=2, column=1)
        self.date_entry = tk.Entry(self._dynamic_frame)
        self.date_entry.grid(row=2, column=2)
        self.date_entry.bind("<KeyRelease>", self._validate_inputs)

        self._submit = tk.Button(self._dynamic_frame, text="Submit", state="disabled", command=self._submit_transaction)
        self._submit.grid(row=3, column=1)
        tk.Button(self._dynamic_frame, text="Cancel", command=self._clear_dynamic_frame).grid(row=3, column=2)

    def _submit_transaction(self):
        if self._current_account is None:
            messagebox.showwarning("Error", "Please select an account before adding a transaction.")
            return
        amount = self.amount_entry.get()
        date = self.date_entry.get()
        date_str = datetime.strptime(date, "%Y-%m-%d")
        self._clear_dynamic_frame()
        try:
            self._current_account.add_transaction(amount, date_str)
            self._session.commit()
            logging.debug(f"Saved to bank.db")
        except AttributeError:
            messagebox.showwarning("Error", "Please select an account before adding a transaction.")
        except OverdrawError as err:
            messagebox.showwarning("Error", err.message)
        except TransactionLimitError as err:
            messagebox.showwarning("Error", err.message + err.limit)
        except TransactionSequenceError as err:
            date = err.latest_date.strftime("%Y-%m-%d")
            messagebox.showwarning("Error", f"New transactions must be from {date} onward.")

        self._display_accounts()
        self._display_transactions()

    def _validate_inputs(self, *args):
        amount = self._validate_amount()
        date = self._validate_date()

        if amount and date:
            self._submit.config(state="normal")
        else:
            self._submit.config(state="disabled")

    def _validate_date(self):
        date_str = self.date_entry.get()
        if len(date_str) == 10 and date_str[4] == '-' and date_str[7] == '-':
            try:
                # date_str = datetime.strptime(self.date_entry.get(), "%Y-%m-%d").date 
                datetime.strptime(self.date_entry.get(), "%Y-%m-%d").date 

                self.date_entry.config(bg="#006400") 
                # self.date_entry.config(style='Valid.TEntry') 
                return True
            except ValueError:
                pass
        self.date_entry.config(bg="#8B0000")
        # self.date_entry.config(style='Invalid.TEntry') 
        return False

    def _validate_amount(self):
        try:
            # value = float(self.amount_entry.get())
            float(self.amount_entry.get())
            self.amount_entry.config(bg="#006400") 
            # self.amount_entry.config(style='Valid.TEntry') 
            return True
        except ValueError:
            self.amount_entry.config(bg="#8B0000")
            # self.amount_entry.config(style='Invalid.TEntry') 
            return False

    def _interest_and_fees(self):
        try:
            self._current_account.interest_and_fees()
            self._session.commit()
            logging.debug(f"Saved to bank.db")
        except AttributeError:
            messagebox.showwarning("Error", "This command requires that you first select an account.")
        except TransactionSequenceError as err:
            month = err.latest_date.strftime("%B")
            messagebox.showwarning("Error", f"Cannot apply interest and fees again in the month of {month}.")
        self._display_accounts()
        self._display_transactions()

    # def _save(self):
    #     with open("bank_save.pickle", "wb") as f:
    #         pickle.dump(self._bank, f)

    # def _load(self):
    #     with open("bank_save.pickle", "rb") as f:   
    #         self._bank = pickle.load(f)

    def handle_exception(self, exception, value, traceback):
        messagebox.showwarning("Error", "Sorry! Something unexpected happened. Check the logs or contact the developer for assistance.")
        logging.error(f"{exception.__name__}: {repr(value)}")
        self._session.close
        sys.exit(0)

if __name__ == "__main__":
    logging.basicConfig(filename='bank.log', level=logging.DEBUG, 
                        format='%(asctime)s|%(levelname)s|%(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    # engine = sqlalchemy.create_engine("sqlite://bank.db")
    Menu()

