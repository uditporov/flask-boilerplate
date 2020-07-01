from flask_restplus import Resource


class Liveness(Resource):
    """
    resource to check liveness of API
    """
    def get(self):
        """
        API to retrieve status of the api
        :return:
        """
        response = {
            "status": "OK"
        }
        return response
