"""
This module is responsible for adding resources of the APIs to the blueprint.
"""

from . import api, resources


api.add_resource(resources.HelloWorld, '/hello', endpoint='hello_world')

