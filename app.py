import newrelic.agent
import os

ENV = os.environ.get('FLASK_ENV', 'development')
newrelic.agent.initialize('newrelic.ini', ENV)

from flask import Flask
from flask_restplus import Api

# main flask application instance

app = Flask(__name__)
env = app.config['ENV']
app.config.from_object('config.{}'.format(env))

settings = app.config
api = Api(app)

# registers all the blueprint and routes of each version of api
from apis.v1 import routes
from apis.healthcheck import routes

app = newrelic.agent.wsgi_application()(app)
if __name__ == '__main__':
    app.run(debug=settings['DEBUG'])
