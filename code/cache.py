import memcahe
from code.configs import CACHE_COMFIGS


class Cache: 
    def __init__(self):
        self.__mem = True        #memcache init. here
        
    def __len__(self):
        pass
    
    def save(task, user_id):
        self.__mem[user_id] = task.json()
    