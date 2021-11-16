#!/usr/bin/env python3

from phoenix.BaseModule import BaseModule, module_type
from phoenix.TCPServer import TcpServer
from phoenix.Shared import shared
from phoenix.Event import Event
from phoenix.ArgumentParser import ArgumentParser


class NativeModule(BaseModule):
    def __init__(self):
        super().__init__() # Initialize the BaseModule
        # Set up the options
        self.options.add('LHOST','0.0.0.0',True,'The host to listen on')
        self.options.add('LPORT','9001',True,'The port to listen on')

        self.info.name = "Teszt ModuleAA"
        self.info.module_name = "AAA"
        self.info.command = "almafa"
        self.info.description = "teszt"
        self.info.authors.append('Peter Isa')
        self.info.classes.extend(['Listener','Native'])
        self.module_type = module_type.Native
        
        # Set EventListeners
        self.onSessionCreated = Event()
        
    def run_with_args(self,input_cmd):
        parser = ArgumentParser(name="tcp_listener")
        parser.add_argument('--lhost',name="lhost",help="Set The LHOST value.")
        parser.add_argument('--lport',name="lport",help="Set the LPORT value.")
        args = parser.parse_arguments(input_cmd)
        
        if 'lport' in args: self.options.set_value('lport',args['lport'])
        if 'lhost' in args: self.options.set_value('lhost',args['lhost'])
        print()
        # Run the application if the help menu not shown
        if parser.show_help == False:
            self.run()

    def run(self):
        if self.check_requirements():
            try:
                lhost = self.options.get_value('lhost')
                lport = self.options.get_value('lport')
                server = TcpServer(lhost,int(lport))
                server.listen()
                # got the newly created session
                new_session = server.get_session() 
                # raise session created event
                if new_session:
                    if self.onSessionCreated.has_subscribers(): 
                        self.onSessionCreated.raise_event(new_session)
                    shared.phoenix.add_session(new_session)
            except:
                pass
            