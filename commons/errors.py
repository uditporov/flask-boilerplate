class Error(object):
    """
    This signifies the error being raise from various validators.
    """

    def __init__(self, error_code, error_message):
        self.error_code = error_code
        self.error_message = error_message

    def to_dict(self):
        return {
            "error_code": self.error_code,
            "error_message": self.error_message
        }
