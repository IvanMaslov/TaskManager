"""
Classes defenition here
"""

import json


class TaskManager:
    def __init__(self):
        self._task_pool = []
        pass

    def __len__(self):
        return len(self._task_pool)

    def get(self):
        pass

    def add(self, task):
        self._task_pool.append(task)

    


class Task:
    @staticmethod
    def check(day, time):
        c_t = time.time()       #parse it to (month, day, time) format
        # copy this from Buisbot proj.
        return True

    def __init__(self, day, time, name, description):
        if not self.check(day, time):
            raise Exception("Wrong time/day format!")
        self._time = time
        self._day = day
        self._name = name
        self._description = dedcription
    
    def __repr__(self):
        return self._name + "/n" + self._description

    def json(self):
        return json.dumps(self.__dict__)

    

    
   

