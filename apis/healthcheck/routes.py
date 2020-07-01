"""
This module is responsible for adding resources of the APIs to the blueprint.

apis.__init__ modules calls the add_resources function to add resources into the blueprints.

    >> api = importlib.import_module("apis.{}.routes".format(version))
    >> api.add_resource(resource, url, endpoint, view, method)
"""

from apis.healthcheck import resources, api

# Dispatches URI
api.add_resource(resources.Liveness, 'status',
                 endpoint='liveness', methods=['GET'])

