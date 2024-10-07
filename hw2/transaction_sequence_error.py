import calendar

class TransactionSequenceError(Exception):
    """Exception raised when a transaction violates the chronological sequence of transactions and interest applications."""

    def __init__(self, error, date):
        super().__init__()
        self.error = error
        if self.error == "interestError":
            month_number = date.month
            month_name = calendar.month_name[month_number]
            self.latest_date = month_name
        else:
            self.latest_date = date