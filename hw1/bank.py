from savings_account import SavingsAccount 
from checking_account import CheckingAccount 


class Bank:

    def __init__(self):
        self._accounts = []
        self.count = 0


    def new_account(self, account_type):
        # increment count to allow for a unique account number
        self.count += 1
        if account_type == "Savings":
            self._accounts.append(SavingsAccount(self.count, account_type))
        else:
            self._accounts.append(CheckingAccount(self.count, account_type))



    def new_transaction(self, amount, date, account):
        account.add_transaction(amount, date)

        
        
    def fetch_account(self, account_number):
        for account in self._accounts:
            if account.number_matches(account_number):
                return account

    def fetch_account_then_format(self, account_number):
        for account in self._accounts:
            if account.number_matches(account_number):
                return account.format_account()
    
  
    def all_accounts(self):
        formated_accounts_list = []
        for account in self._accounts:
            formated_accounts_list.append(account.format_account())

        return formated_accounts_list
