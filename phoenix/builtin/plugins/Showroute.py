"""
Native Plugin for System Routes
"""
from phoenix.Plugin import Plugin, plugin_type
from phoenix.ArgumentParser import ArgumentParser
from phoenix.ExecCode import ExecCode
from phoenix.Plugin import Plugin

class NativePlugin(Plugin):
    def __init__(self):
        super().__init__()
        self.info.name = "Show IP Routes"
        self.info.module_name = "native/showroute"
        self.info.command = 'showroute'
        self.plugin_type = plugin_type.Native
        self.info.description = "This Plugin shows the routes on the remote host."
        
        #self.parser = ArgumentParser(name="showroute")
        #self.parser.add_argument('-s','--session',name="session",help="The target session to use")        

        self.client = None
        
    
    def run_with_args(self,command):
               
        #args = self.parser.parse_arguments(command)
        #if not self.parser.show_help:
        #    self.run(args)
        self.run('')
        
    def run(self,args):
        
        if 'session' in args:
            session_name = args['session']
            session = shared.phoenix.get_session(session_name)
            if session:
                self.client = session.get_socket()
                
        command = ExecCode(self.client)
        # Check python3 is available on the target machine
        result = command.execute('route')
        print(result)
            
    