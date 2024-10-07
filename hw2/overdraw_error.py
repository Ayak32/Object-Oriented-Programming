

class OverdrawError(Exception):
    """Exception raised when a transaction exceeds the available account balance."""
    def __init__(self):
        super().__init__()