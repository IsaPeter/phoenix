#!/usr/bin/env python3

from phoenix.BaseModule import BaseModule, module_type
from phoenix.Shared import shared
from phoenix.Event import Event
from phoenix.ArgumentParser import ArgumentParser
from phoenix.ExecCode import ExecCode

class NativeModule(BaseModule):
    def __init__(self):
        super().__init__() # Initialize the BaseModule
        # Set up the options
        self.options.add('SESSION','',True,'The session to communicate')

        self.info.name = "Query SUID executables"
        self.info.module_name = "native/post/querysuid"
        self.info.command = "querysuid"
        self.info.description = "Query the SUID bit set executables from the target OS."
        self.info.authors.append('Peter Isa')
        self.info.classes.extend(['post','Native'])
        self.module_type = module_type.Native
        
        self.client = None
        
    def run_with_args(self,input_cmd):
        parser = ArgumentParser(name="querysuid")
        parser.add_argument('-s','--session',name="session",help="Set the session value.")
        args = parser.parse_arguments(input_cmd)
        
        if 'session' in args: self.options.set_value('session',args['session'])
        
        #print()
        # Run the application if the help menu not shown
        if parser.show_help == False:
            self.run()

    def run(self):
        if self.check_requirements():
            try:
                payload = "find / -type f -perm -u=s 2>/dev/null"
                if self.client:
                    command = ExecCode(self.client)
                    command.waitForFinish = True # Ezt még implementálni kell
                    response = command.execute(payload) # payload futtatása
                    print(response)
                else:
                    session_value = self.options.get_value('session')
                    if session_value != '':
                        pass
            except:
                pass
