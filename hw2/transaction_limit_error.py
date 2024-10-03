


class TransactionLimitError(Exception):
    def __init__(self, limit):
        super().__init__()
        self.limit = limit