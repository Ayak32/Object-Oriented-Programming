from datetime import datetime


class Transaction:
    def __init__(self, date, amount):
        self.date = datetime.strptime(date, "%Y-%m-%d")
        self.amount = amount
    
    def __repr__(self):
        return f"{self.date.strftime('%Y-%m-%d')}, ${self.amount:,.2f}"

    # def add_transaction()
