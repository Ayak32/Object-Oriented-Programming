
class TransactionLimitError(Exception):
    """Exception raised when a transaction exceeds a predefined limit."""

    def __init__(self, limit):
        super().__init__()
        self.limit = limit