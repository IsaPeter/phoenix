"""
Native Plugin for System Information
"""
from phoenix.Plugin import Plugin, plugin_type
from phoenix.ArgumentParser import ArgumentParser
from phoenix.ExecCode import ExecCode
from phoenix.Colors import colors

class NativePlugin(Plugin):
    def __init__(self):
        super().__init__()
        self.info.name = "Enumerate Logon Users"
        self.info.module_name = "native/enumusers"
        self.info.command = 'enumusers'
        self.plugin_type = plugin_type.Native
        self.info.description = "This Plugin enumerates a logon users from the target system."
        
        self.client = None
        
    
    def run_with_args(self,command):
        self.run('')
        
    def run(self,args):
        
        if 'session' in args:
            session_name = args['session']
            session = shared.phoenix.get_session(session_name)
            if session:
                self.client = session.get_socket()
                
        command = ExecCode(self.client)
        # Check python3 is available on the target machine
        result = command.execute('cat /etc/passwd')
        userlines = result.splitlines()
        print() # for separate purposes only
        for u in userlines:
            if not 'nologin' in u and not '/bin/false' in u:
                print(self.create_userline(u))
        # Print for separate last line
        print()
        
    def create_userline(self,userline):
        try:
            data = userline.split(':')
            uname = data[0]
            uid = data[2]
            gid = data[3]
            name = data[4]
            home = data[5]
            shell = data[6]
            return f"user(username={uname}, uid={uid}, gid={gid}, name={name}, home={home}, shell={shell})"
        except:
            return userline

