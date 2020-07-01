from flask import request
from flask_restplus import Resource

from . import api


class HelloWorld(Resource):

    def get(self):
        return "Hello World."
