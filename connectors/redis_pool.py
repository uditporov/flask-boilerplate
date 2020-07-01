import redis


REDIS_URL = 'localhost'
REDIS_PORT = 6379
REDIS_DEFAULT_DB = 0

_redis = None


class RedisConnectionPool(object):
    """
    Class to get redis object
    Its a singleton class 
    """
    
    def connect(self, host=REDIS_URL, port=6379, db_number=REDIS_DEFAULT_DB):
        
        global _redis
        
        if _redis is None:
            self.host = host
            self.port = port
            self.db_number = db_number
            self.pool = redis.ConnectionPool(host=self.host, port=self.port, db=self.db_number)
            self.db = redis.StrictRedis(connection_pool=self.pool)
            self.redis = redis.Redis(connection_pool=self.pool)

            _redis = self

        return _redis
