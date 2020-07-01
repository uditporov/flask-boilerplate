import json
import requests
from commons.response import Response
from logging import getLogger

logger = getLogger(__name__)


REQUEST_METHODS = {
    'POST': lambda url, params, data, headers: requests.post(url, data=json.dumps(data), headers=headers),
    'GET': lambda url, params, data, headers: requests.get(url, params, headers=headers),
    'PUT': lambda url, params, data, headers: requests.put(url, data=json.dumps(data), headers=headers),
    'HEAD': lambda url, params, data, headers: requests.head(url, headers=headers),
    'OPTIONS': lambda url, params, data, headers: requests.options(url, headers=headers),
    'PATCH': lambda url, params, data, headers: requests.options(url, data=json.dumps(data), headers=headers),
    'DELETE': lambda url, params, data, headers: requests.options(url, headers=headers)
}


class API(object):
    """
    Generic API class which can be inherited to create an api integration
    by merely defining the 'URI' and 'ENDPOINTS'

    eg -

    URI = 'http://www.google.com/'
    AUTH_TOKEN = "TEST_TOKEN"
    ENDPOINTS = {
        'FETCH_PRODUCT_DETAILS': {
            'endpoint': 'api/v1/product/{}/',
            'method': 'GET'
        }
    }

    """
    uri = None
    auth_token = None
    endpoints = {}

    def __init__(self):
        pass

    def request(self, endpoint, headers={}, url_slugs={}, query_params={}, payload={}):
        """
        Sends out the api request

        :param endpoint: url
        :param headers: dict consisting of headers
        :param url_slugs: list of slug values in the URL
        :param query_params: key value pair of query params
        :param payload: data
        :return:
        """
        request_method = REQUEST_METHODS[self._get_method(endpoint)]
        url = self._get_url(endpoint, url_slugs)
        response = Response()
        try:
            if self._get_method(endpoint) in ['POST', 'PUT', 'PATCH']:
                headers.update({'Content-Type': 'application/json'})

            if self.auth_token:
                headers.update({'AUTHORIZATION': self.auth_token})

            # requesting api
            api_resp = request_method(url, query_params, payload, headers=headers)
            api_resp.raise_for_status()
            api_resp = json.loads(api_resp.text)

            response.data = api_resp.get('data', response.data)
            response.errors = api_resp.get('errors', response.errors)
            response.message = api_resp.get('message', response.message)
            response.success = api_resp.get('success', response.success)

        except requests.exceptions.HTTPError as err:
            logger.error(err)
            response.message = "Some HTTP error occurred while accessing an API."
        except requests.exceptions.Timeout as err:
            # Maybe set up for a retry, or continue in a retry loop
            logger.error(err)
            response.message = "Request has been timed out."
        except requests.exceptions.TooManyRedirects as err:
            # Tell the user their URL was bad and try a different one
            logger.error(err)
            response.message = "Bad url being hit try a different one."
        except requests.exceptions.RequestException as err:
            # catastrophic error. bail.
            logger.error(err)
            response.message = "Catastrophic error occurred while accessing an API."

        return response

    def _get_url(self, endpoint, url_slugs={}):
        """
        This method simply return URL by appending endpoint to the URI and adds url slugs into it.
        :param endpoint: STRING defining the key of endpoints dictionary
        :param url_slugs: list of values to be appended to the url as the slug
        :return:
        """
        return self.uri + self.endpoints[endpoint]['endpoint'].format(**url_slugs)

    def _get_method(self, endpoint):
        """
        This method simply looks into the endpoints dictionary and will return the request method
        :param endpoint: STRING key of endpoints dictionary
        :return: STRING request method POST/GET/PUT
        """
        return self.endpoints[endpoint]['method']
