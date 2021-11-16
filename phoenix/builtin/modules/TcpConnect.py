#!/usr/bin/env python3
"""
Native TCP Connect module
"""

from phoenix.BaseModule import BaseModule, module_type
from phoenix.Shared import shared
from phoenix.Event import Event
from phoenix.ArgumentParser import ArgumentParser
from phoenix.Session import Session
from phoenix.TcpClient import TcpClient
import socket


class NativeModule(BaseModule):
    def __init__(self):
        super().__init__() # Initialize the BaseModule
        # Set up the options
        self.options.add('RHOST','127.0.0.1',True,'The host to connect')
        self.options.add('RPORT','9001',True,'The port to connect')

        self.info.name = "Tcp Connector"
        self.info.module_name = "native/tcp_connect"
        self.info.command = "tcp_connect"
        self.info.description = "Connects to a listening Tcp port on the target machine."
        self.info.authors.append('Peter Isa')
        self.info.classes.extend(['Connect','Native'])
        self.module_type = module_type.Native
        
        # Set EventListeners
        self.onSessionCreated = Event()
        
    def run_with_args(self,input_cmd):
        parser = ArgumentParser(name="tcp_connect")
        parser.add_argument('--rhost',name="rhost",help="Set The RHOST value.")
        parser.add_argument('--rport',name="rport",help="Set the RPORT value.")
        args = parser.parse_arguments(input_cmd)
        
        if 'rport' in args: self.options.set_value('rport',args['rport'])
        if 'rhost' in args: self.options.set_value('rhost',args['rhost'])
        print()
        # Run the application if the help menu not shown
        if parser.show_help == False:
            self.run()

    def run(self):
        if self.check_requirements():
            try:
                rhost = self.options.get_value('rhost')
                rport = self.options.get_value('rport')
                
                client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                
                print(f"[*] Connecting to {rhost}:{str(rport)}")
                client.connect((rhost,int(rport)))
                print(f"[+] Successfully connected to {rhost}:{str(rport)}")
                
                # Create a TCP Client object
                c = TcpClient(client)
                # got the newly created session
                new_session = Session(c)
                print(f"[+] New Session created {rhost} ==> {new_session.name}")
                
                # raise session created event
                if new_session:
                    shared.phoenix.add_session(new_session)
                    
            except Exception as x:
                print(f"[x] {x}")
            