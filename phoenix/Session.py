#!/usr/bin/env python3
"""
Session module for phoenix and Native modules
"""
from enum import Enum
import string
import random
from tabulate import tabulate
from phoenix.Event import Event
from phoenix.Colors import colors
from phoenix.Shared import shared

class Session():
    def __init__(self,client=None):
        self.client = client # The Client instance
        self.name = self.__generate_name() # generate an unique name
        self.interact_module = False # Module Interaction
        self.client_type = client_type.Native
        self.plugins = [] # the loaded plugins for this session
        self.prompt_str = ">"
        self.onSessionDead = Event()
        self.platform = ""
        self.hostname = ""
        self.username = ""
        
    def set_client(self,tcp_client):
        self.client = tcp_client
        
    def __generate_name(self,size=8, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))
    
    def get_socket(self):
        return self.client
    
    def get_client_type(self):
        return self.client.shell_type
    
    def interactive(self):
        self.interact_module = True
        # Create shell prompt name
        if self.client_type == client_type.Native:
            self.prompt_str = f"Session({colors.WARNING+self.name+colors.ENDC}) > "
        else:
            self.prompt_str = f"Phoenix({colors.WARNING+self.name+colors.ENDC}) > "
        try:
            # Interactive loop start
            while self.interact_module:
                if self.client.check_connection_alive():
                    cmd = input(self.prompt_str).rstrip()
                    self.command_interpreter(cmd)
                else:
                    self.interact_module = False
                    self.onSessionDead.raise_event(self)
        except KeyboardInterrupt:
            pass        
        
    def command_interpreter(self,cmd):
        command = cmd.split(' ')
        if command[0].lower() == 'show':
            if len(command) == 2:
                if command[1].lower() == 'info': self.show_info()
                elif command[1].lower() == 'help': self.show_help()
                elif command[1].lower() == 'plugins': self.show_plugins()
        elif command[0].lower() == 'help': self.show_help()
        elif command[0].lower() == 'info': self.show_info()
        elif command[0].lower() in ['bg','exit']:
            self.interact_module = False
        elif command[0].lower() == 'terminate':
            self.client.close()
        elif command[0].lower() == "cmd":
            command.pop(0)
            cmd = ' '.join([i for i in command])
            self.run_command(cmd+"\n")
        elif command[0].lower() == 'shell':
            self.open_os_shell()
        elif command[0].lower() == 'test':
            print(self.client.local_address)
            print(self.client.remote_address)
        elif command[0].lower() == 'loadplugin':
            if len(command) == 2:
                plugin = shared.phoenix.get_plugin(command[1])
                if plugin:
                    self.plugins.append(plugin)
                    print(f"[+] Successfully loaded plugin: {plugin.info.name}")
                else:
                    print(f"[x] Failed to load plugin!")
        elif command[0].lower() == 'rename':
            if len(command) == 2:
                self.name = command[1]
                if self.client_type == client_type.Native:
                    self.prompt_str = f"Session({colors.WARNING+self.name+colors.ENDC}) > "
                else:
                    self.prompt_str = f"Phoenix({colors.WARNING+self.name+colors.ENDC}) > "                
        else:
            found_plugin = False
            # Check plugins contains appropriate name
            if len(self.plugins) > 0:
                for p in self.plugins:
                    if p.info.name.lower() == command[0].lower(): found_plugin = True
                    if p.info.command.lower() == command[0].lower(): found_plugin = True
                    if p.info.module_name.lower() == command[0].lower(): found_plugin = True
                    if found_plugin:
                        p.client = self.client
                        p.run_with_args(cmd)
                        break
                    
                        
                
            
    def run_command(self, command):
        self.client.send(command)
        result = self.client.receive_all()
        print(result)
    def show_help(self):
        help = [
            ['bg, exit','Exit from the current interactive session'],
            ['terminate','Terminate the current session'],
            ['help','Show this menu'],
            ['info','Show information about the session'],
            ['cmd <command>','Without colon, run the command in the remote host'],
            ['show plugins','Show the appropriate plugins.'],
            ['loadplugin','Loads the selected plugin.'],
            ['rename','Rename the current Session.'],
            ["get_modules"," Got the loaded modules list in the Phoenix Client"],
            ["exec","Executes a python code on the target"],
            ["load_code","Load python code to the dict"]
        ]
        print()
        if self.client_type == client_type.Native:
            print(f"Options for Native Session ({self.name})")
        else:
            print(f"Options for Phoenix Session ({self.name})")
            
        print(tabulate(help))
        print()
        
        if len(self.plugins) > 0:
            res = []
            for p in self.plugins:
                res.append([p.info.command,p.info.name])
            print(f"Extended Options from plugins")
            print(tabulate(res))
            print()
        
    def show_info(self):
        data = [
            ['Name',self.name],
            ['Local Address',str(self.get_lhost()+":"+self.get_lport())],
            ['Remote Address',str(self.get_rhost()+":"+self.get_rport())],
            ['Client Type',str(self.client_type.name)]
        ]
        
        print()
        print(tabulate(data))
        print()

    def get_rhost(self):
        return str(self.client.remote_address[0])
    def get_rport(self):
        return str(self.client.remote_address[1])
    def get_lhost(self):
        return str(self.client.local_address[0])
    def get_lport(self):
        return str(self.client.local_address[1])    
    def show_plugins(self):
        counter = 0
        header = ['#','Module Name','Type','Command','Description']
        result_array = []
        for p in shared.phoenix.plugins:
            if p.plugin_type.name == self.client_type.name:
                result_array.append([counter,str(p.info.module_name),p.plugin_type.name,p.info.command,p.info.name])
                counter += 1            
        print()
        print(tabulate(result_array,headers=header))
        print()
    def open_os_shell(self):
        run = True
        print("[*] Opening OS Shell")
        while run:
            try:
                cmd = input()
                if not cmd.endswith('\n'):
                    cmd += "\n"
                self.client.send(cmd)
                received = self.client.receive_all2()
                print(received,end='')
            except:
                run = False
    def enuminfo(self):
        try:
            payload = "uname -a;whoami"
            self.client.send(payload)
            result = self.client.receive_all()
            if result:
                data = result.splitlines()
                uname_data = data[0].split(' ')
                self.platform = uname_data[0]
                self.hostname = uname_data[1]
                self.username = data[1]
        except:
            pass




class client_type(Enum):
    Native = 0
    Phoenix = 1
    

"""
s = session()
s.client_type = client_type.Phoenix
s.interactive()
"""