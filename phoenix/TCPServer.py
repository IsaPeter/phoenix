#!/usr/bin/env python3
import os,sys,socket
from phoenix.TcpClient import TcpClient
from phoenix.Session import Session

class TcpServer():
    def __init__(self,address='127.0.0.1',port=9001):
        self.server_address = address
        self.server_port = port
        self.clients_count = 1  # The count of the clients to accept
        self.clients = []   # The connected Clients
        self.sessions = []  # The created sessions
        
        
    def listen(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind((self.server_address, self.server_port))
            print(f"[+] Listening on {self.server_address}:{str(self.server_port)}")
            s.listen(self.clients_count)
            cnt = 0
            while cnt < self.clients_count:
                conn, addr = s.accept()
                c = TcpClient(conn,addr)
                s = Session(c)
                print(f"[+] Client Connected with address {str(addr[0])} ==> {s.name}")
                self.clients.append(c)
                self.sessions.append(s)
                cnt += 1
                
        except Exception as x:
            print(f"[-] {x}")
    def get_client(self):
        if len(self.clients) > 0:
            return self.clients[0]
    def get_session(self):
        if len(self.sessions) >0:
            return self.sessions[0]
    def get_clients(self):
        return self.clients
    def get_sessions(self):
        return self.sessions