import os
basedir = os.path.abspath(os.path.dirname(__file__))


PROJECT_NAME = 'UDIT'
DEBUG = False
TESTING = False
CSRF_ENABLED = True
SECRET_KEY = 'this-really-needs-to-be-changed'
SQLALCHEMY_DATABASE_URI = "postgresql://DBUSER:DBUSER@localhost:5400/DB_NAME"
ERROR_404_HELP = False
ENTITY_PER_PAGE = 20
DEFAULT_CHANNEL_NAME = 'UDIT'
STREAM_HOST = ''
STREAM_SERVICE = 'KAFKA'
KAFKA_AUDIT_TOPIC_NAME = 'UDIT'
SQLALCHEMY_TRACK_MODIFICATIONS = True

CACHE_DEFAULT_EXPIRY_TIME = 20

LOG_CONFIG = {
    "version": 1,
    "handlers": {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': "/app/logs" + "/%s.log" % PROJECT_NAME,
            'formatter': 'customFormatter',
            'maxBytes': 1024 * 1024 * 100,
            'backupCount': 10
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'customFormatter',
        }
    },
    "loggers": {
        '': {
            "handlers": ["file"],
            "level": "INFO",
        }
    },
    "formatters": {
        "customFormatter": {
            "format": ("@timestamp %(asctime)s || @filename %(name)s || @ loglevel %(levelname)s ||"
                        "@process %(process)d || @thread %(thread)d || "
                        "@path %(pathname)s || @line %(lineno)d || "
                        "@environment %(environment)s || @project %(project)s ||"
                        "@module %(name)s || @message %(message)s ||")
        }
    }
}
