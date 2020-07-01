import logging
from logging.config import dictConfig

from app import settings


class LOGSetup(object):
    """log setup with configuration"""
    old_factory = logging.getLogRecordFactory()
    def setup_log(self):
        dictConfig(settings['LOG_CONFIG'])
        logging.setLogRecordFactory(self.record_factory)

    def record_factory(self, *args, **kwargs):
        """
        adds some custom field in log formatter
        """
        record = self.old_factory(*args, **kwargs)
        record.environment = settings['ENV']
        record.project = settings['PROJECT_NAME']
        return record
