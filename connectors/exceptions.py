class AWSConnectionFailed(Exception):
    """
    raised in case IAM role information is not found in instance
    """
    def __init__(self, error_code):
        """
        """
        self.error_code = error_code
        self.message = str(AWS_ERROR_CODES[error_code])

    def __str__(self):
        return self.message

