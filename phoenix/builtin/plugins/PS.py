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
        

        self.info.name = "Process Dump"
        self.info.module_name = "native/ps"
        self.info.command = "ps"
        self.info.description = "Dumps the processes from the target machine."
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
            result = command.execute('ps -aux')
            print(result)                
        except Exception as x:
            print(x)
            print("[x] Process execution failed")
