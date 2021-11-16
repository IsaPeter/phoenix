#!/usr/bin/env python3

# This is the basic version
class Event1(object):
    def __init__(self):
        self.__handlers = []

    def __iadd__(self, handler):
        self.__handlers.append(handler)
        return self

    def __isub__(self, handler):
        self.__handlers.remove(handler)
        return self

    def raise_event(self, *args, **keywargs):
        for handler in self.__handlers:
            handler(*args, **keywargs)

    def clearObjectHandlers(self, inObject):
        for theHandler in self.__handlers:
            if theHandler.im_self == inObject:
                self -= theHandler
                
                
# Event class for subscriptions
class Event():
    def __init__(self,*args,**kwargs):
        self.subscribers = []
    def __iadd__(self, handler):
        self.subscribers.append(handler)
        return self    
    def __isub__(self, handler):
        self.subscribers.remove(handler)
        return self    
    def subscribe(self,event):
        self.subscribers.append(event)
    def unsubscribe(self,event):
        self.subscribers.remove(event)
    def clear(self):
        self.subscribers.clear()
    def raise_event(self,*args,**kwargs):        
        for e in self.subscribers:
            e(*args,**kwargs)
    def has_subscribers(self):
        if len(self.subscribers) > 0:
            return True
        else:
            return False
            
"""          
def client_connected(conn,addr):
    print(f"[+] Client Connected with address {str(addr[0])}")
            
            
        
import socket            
class testclass:
    def __init__(self):
        self.onClientConnected = Event()
        self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.connections = []
    def listen(self):
        counter = 5
        self.server.bind(('127.0.0.1', 9001))
        print(f"[+] Listening on 127.0.0.1:9001")
        self.server.listen(counter)
        cnt = 0
        while cnt < counter:
            conn, addr = self.server.accept()
            self.connections.append(conn)
            self.onClientConnected.raise_event(conn,addr)
            cnt += 1
            
            
tc = testclass()
tc.onClientConnected += client_connected
tc.listen()
"""        
