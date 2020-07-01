import boto3

from exceptions import AWSConnectionFailed


class AWSConnection(object):
    """
    To handle aws authentication
    creates an instance of boto3.Session which when not provided
    with access keys and secret keys will pick up such details from
    the metadata of the instance.
    """

    session = boto3.Session()

    def __init__(self):
        """
        get credentials whenever class is initiated
        """
        self.get_credentials()

    def get_credentials(self):
        """
        fetch credentials, the credentials will have expiry limit
        which is to be set in policy in AWS. The information will be available
        in the metadata of the instance.
        updates self with the following variables
            aws_access_key: access key
            aws_secret_key: secret key
            aws_session_token: session token
        Exception:
            will catch AttributeError if no IAM role information found in
            the environment and throw AWSConnectionFailed error
        """
        self.credentials = self.session.get_credentials()
        try:
            self.aws_access_key=self.access_key
            self.aws_secret_key=self.secret_key
            self.aws_session_token=self.session_token
        except AttributeError:
            raise AWSConnectionFailed(error_code='AWS_CONNECTION_FAILED')

    @property
    def access_key(self):
        """
        getter for access key
        if key is access from other source for exampler os environment
        based on condition then logic is to be added here.
        """
        return self.credentials.access_key

    @property
    def secret_key(self):
        """
        getter for secret key
        if key is access from other source for exampler os environment
        based on condition then logic is to be added here.
        """
        return self.credentials.secret_key

    @property
    def session_token(self):
        """
        getter for session key
        if key is access from other source for exampler os environment
        based on condition then logic is to be added here.
        """
        return self.credentials.token
