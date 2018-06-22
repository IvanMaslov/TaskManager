from pymemcache.client import Client
from pymemcache.exceptions import *
from code.configs import CACHE_CONFIGS, DB_CONFIGS
import psycopg2 as pg
import logging


logging.log(level=logging.DEBUG, file='cache_log.txt')


class Cache: 
    def __init__(self):
        try:
            self.__mem = Client(**CACHE_CONFIGS)        # memcache init. here
        except (MemcacheServerError, MemcacheUnexpectedCloseError, MemcacheClientError) as e:
            logging.critical("%s occurred while connecting Memcached")
            self.__mem = None
        self._tasks = 0

    def __len__(self):
        return self._tasks

    def conn(self):
        logging.info("A protected field accessed")
        return self.__mem
    
    def set(self, task, user_id):
        try:
            if self.__mem.set(str(user_id), task.json()):
                self._tasks += 1
        except (MemcacheIllegalInputError, MemcacheUnknownCommandError, TypeError) as e:
            logging.critical("%s occurred with setting(%s: %s)" % (str(e), str(user_id), str(task.json())))

    def get(self, user_id):
        try:
            res = self.__mem.get(str(user_id))
        except (MemcacheIllegalInputError, MemcacheUnknownCommandError, TypeError) as e:
            logging.critical("%s occurred with getting %s" % (str(e), str(user_id)))
            return None
        return res

    def pop(self, user_id):
        try:
            res = self.__mem.get(str(user_id))
            self.__mem.delete(str(user_id))
        except (MemcacheIllegalInputError, MemcacheUnknownCommandError, TypeError) as e:
            logging.critical("%s occurred with popping %s" % (str(e), str(user_id)))
            return None
        return res


class DatabaseConnection:
    # use with context managers:
    #   with database as
    def __enter__(self):
        try:
            self.__conn = pg.connect(self._configs)
        except pg.Error as e:
            logging.critical("%s occurred while connecting PostgreSQL Database" % str(e))
        return self.__conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self.__conn.commit()
        except pg.Error as e:
            logging.critical("%s occurred, can\'t save data, changes would be reverted" % str(e))
        self.__conn.close()

