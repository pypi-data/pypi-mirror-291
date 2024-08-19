class JacobiError(Exception):
    """Class for Jacobi errors."""
    def __init__(self, category, message):
        self.category = category
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'\n[jacobi.exception.{self.category}\n\t{self.message}\n'
