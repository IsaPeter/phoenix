"""
Native Plugin for System Information
"""
from phoenix.Plugin import Plugin, plugin_type
from phoenix.ArgumentParser import ArgumentParser
from phoenix.ExecCode import ExecCode

class NativePlugin(Plugin):
    def __init__(self):
        super().__init__()
        self.info.name = "System Information Gather"
        self.info.module_name = "native/systeminfo"
        self.info.command = 'systeminfo'
        self.plugin_type = plugin_type.Native
        self.info.description = "This Plugin collectes system related information."
        
        self.parser = ArgumentParser(name="systeminfo")
        self.client = None
        
        self.payloads = {
            'python3':'python3 -c "import platform as p;import json;s=p.system();m=p.machine();pl=p.platform();v=p.version();a=p.architecture();n=p.node();r=p.release();pv=p.python_version();d={\'system\':s,\'machine\':m,\'platform\':pl,\'version\':v,\'arch\':a,\'node\':n,\'release\':r,\'pyversion\':pv};print(json.dumps(d))"'
        }
    
    def run_with_args(self,command):
               
        self.parser.add_argument('-s','--session',name="session",help="The target session to use")        
        
        args = self.parser.parse_arguments(command)
        if not self.parser.show_help:
            self.run(args)
        
    def run(self,args):
        
        if 'session' in args:
            session_name = args['session']
            session = shared.phoenix.get_session(session_name)
            if session:
                self.client = session.get_socket()
                
        command = ExecCode(self.client)
        # Check python3 is available on the target machine
        result = command.execute('which python3')
        if 'python3' in result:
            self.python3_systeminfo(args)
            
    def python3_systeminfo(self,args):
        command = ExecCode(self.client)
        payload = self.payloads['python3']
        result = command.execute(payload)
        if 'system' in result:
            import json
            data = json.loads(result)
            print()
            print(f"System:       {data['system']}")
            print(f"Machine:      {data['machine']}")
            print(f"Platform:     {data['platform']}")
            print(f"Version:      {data['version']}")
            print(f"Architecture: {', '.join(str(i) for i in data['arch'])}")
            print(f"Hostname:     {data['node']}")
            print(f"Kernel:       {data['release']}")
            print(f"Python:       {data['pyversion']}")
            print()
        else:
            print(f"[x] No enough information to determine the System informations.")
            