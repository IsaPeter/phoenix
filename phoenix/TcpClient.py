#!/usr/bin/env python3
import socket
from phoenix.Event import Event
import time
import select

class TcpClient():
    def __init__(self,conn,addr=None):
        self.client = conn
        self.local_address = conn.getsockname()
        self.remote_address = conn.getpeername()
        self.default_receive_buffer = 8096  # The dafault buffer size to receive data
        self.dead = False
        self.maxtimeout = 2               # 20 sec
        self.available = True
        self.ready_state = False
             
        self.onConnectionDead = Event()
    
    def get_socket(self):
        return self.client
    
    def send(self,data):
        if self.check_connection_alive():
            try:
                if not data.endswith('\n'): data = data+"\n"
                
                self.client.send(data.encode())
                
            except BrokenPipeError:
                self.dead = True
                self.onConnectionDead.raise_event(self)
        else:
            print("[x] The connection is seems to be dead!")
        
                
    def receive(self,length=8096):
        if self.check_connection_alive():
            try:
                data = self.client.recv(length)
                return data
            except Exception:
                self.dead = True
                self.onConnectionDead.raise_event(self)
        else:
            print("[x] The connection is seems to be dead!")
                    
    def receive_all(self,blocking=True):
        if self.check_connection_alive():
            try:
                recv_len = 1
                response = b''
                s = None
                if blocking:
                    self.client.setblocking(1)
                    
                while recv_len:
                    data = self.client.recv(self.default_receive_buffer)
                    response += data
                    recv_len = len(data)
                    if recv_len < self.default_receive_buffer:
                        if blocking: self.client.setblocking(0)
                        read_sock,write_sock,error_sock = select.select([self.client],[],[],0.05)
                        if blocking: self.client.setblocking(1)
                        if not read_sock:
                            break  
                return response.decode(encoding='latin-1')
            except Exception as x:
                print(x)
                self.dead = True
                self.onConnectionDead.raise_event(self)
        else:
            print("[x] The connection is seems to be dead!")
                        
             
    def receive_all2(self):
        self.client.setblocking(0)
        recv_len = 1
        response = b''
        s = None
        ndc = 0 # No Data Counter
        receive = True
        while receive:
            try:
                if ndc > 3: receive = False 
                
                data = self.client.recv(self.default_receive_buffer)
                if data:
                    response += data
                    recv_len = len(data)
                    
                else:
                    if ndc <= 3:
                        ndc += 1
                        time.sleep(0.01)
                    else:
                        receive = False
            except Exception as x:
                #print(x)
                ndc += 1
                time.sleep(0.05)
                
        # restore blocking
        self.client.setblocking(1)
        # return the result
        return response.decode(encoding='latin-1')         
    
        
        
    def check_connection_alive(self):
        if self.client._closed == False:
            if self.dead == False:
                return True
            else:
                return False
        else:
            self.dead = True
            return False
    def close(self):
        self.client.close()
        self.available = False
        self.dead = True
        self.onConnectionDead.raise_event(self)
