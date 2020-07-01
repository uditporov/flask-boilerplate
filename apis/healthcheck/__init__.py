"""
This module is responsible for following things -
    ~ Registering blueprint for the different versions of APIs
    ~ Adding resources pointing to different versions of APIs

This module will be imported in the app.py (main flask module), as registering
of blueprints and resources needs to be done at the initialization of the app.

Attributes -
    ~ VERSION_REGEX - regex string defining the possible format of defining
                      version packages eg- v1, v2 etc
    ~ versions - contains the list of versions defined in the APIs module.
"""

import os
import re
import importlib

from flask_cors import CORS
from flask_restplus import Api, Namespace
from flask import Blueprint
from app import app

# version identifier
name = 'healthcheck'

# Declare the blueprint
blueprint = Blueprint(name, __name__)

# Set up cross-scripting allowed
CORS(blueprint)

# Set up the API and init the blueprint
api = Api(default="Healthcheck",
          default_label="APIs for liveness and readiness")
api.init_app(blueprint)

app.register_blueprint(blueprint, url_prefix='/')
