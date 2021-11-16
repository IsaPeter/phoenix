#!/usr/bin/env python3
"""
Phoenix Job Object
"""
from multiprocessing import Process
import time

class Job:
    def __init__(self,obj):
        self.target_object = obj # Set the target object
        self.created = time.time()
        self.main_process = None
        
    def run(self):
        self.main_process = Process(target=self.target_object.run)
        self.main_process.start()
    def run_with_rags(self,args):
        self.main_process = Process(target=self.target_object.run,args=(args,))
        self.main_process.start()
    def join(self):
        self.main_process.join()
    def kill(self):
        self.main_process.kill()
        




# Testing
"""
import os
class testclass:
    def __init__(self):
        pass
    def run(self):
        os.system("nc -lvnp 9005")
       
       
tc = testclass()
j = Job(tc)
j.run()

while True:
    cmd = input('> ')
    if cmd == 'join':
        j.join()
"""