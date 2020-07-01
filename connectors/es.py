from aws_requests_auth.aws_auth import AWSRequestsAuth
from elasticsearch import Elasticsearch, RequestsHttpConnection

from aws import AWSConnection


ES_URL = 'localhost'
ES_SERVICE = None
ES_PORT = 9200
ES_INDEX = 'INDEX'
ES_AWS_REGION='ap-southeast-1'

class ElasticSearchConnection(object):
    """
    Wrapper Class to connect to elasticsearch depending
    on the settings
    """
    @classmethod
    def connect(cls):
        """
        wrapper method around es connection
        """
        es_service = ES_SERVICE
        return AWSESConnection.connect()


class AWSESConnection(object):
    """
    Class to connect to AWS ES managed service using IAM user
    authentication
    """
    @classmethod
    def connect(cls):
        """
        elasticsearch aws connection class which handles
        authentication using AWSRequestsAuth
        """
        credentials = AWSConnection()
        awsauth = AWSRequestsAuth(
            aws_access_key=credentials.aws_access_key,
            aws_secret_access_key=credentials.aws_secret_key,
            aws_token=credentials.aws_session_token,
            aws_host=ES_URL,
            aws_region=ES_AWS_REGION,
            aws_service='es'
        )

        return Elasticsearch(
            ES_URL, port=ES_PORT, http_auth=awsauth,
            use_ssl=True, verify_certs=True,
            connection_class=RequestsHttpConnection)
