#!/usr/bin/env python3
from tabulate import tabulate
from phoenix.TabCompleter import TabCompleter, TabManager
from phoenix.ModuleLoader import ModuleLoader

class Phoenix:
    def __init__(self):
        self.modules = []
        self.jobs = [] # This feature is not implemented yet!
        self.interactive = False
        self.sessions = []
        self.__module_cache = []
        self.plugins = []
        self.load_paths = []
        
        # Initialize help menu
        self.help = [
            ['help','Show this menu'],
            ['list [type]','List all available [modules, listeners, sessions]'],
            ['use [name/number]','Use a selected module'],
            ['info [module]','Shows info for a specified module'],
            ['interact [name/number]','Interact with active session'],
            ['search [term]','Search in the modules'],
            ['exit','Exit from the application'] 
        ]
        # tabulation manager
        self.tabman = TabManager()
        
    def run(self):
        self.interactive = True
        while self.interactive:
            cmd = input('Phoenix > ')
            self.command_interpreter(cmd)
            
        # The end of Phoenix shutdown all opened sockets
        self._shutdown_sockets()
    def command_interpreter(self,command):
        cmd = command.rstrip().split(" ")
        if cmd[0].lower() == 'show':
            pass
        if cmd[0].lower() == "help": self.show_help()
        elif cmd[0].lower() == "exit": self.interactive = False
        elif cmd[0].lower() == 'search':
            pass
        elif cmd[0].lower() == 'list':
            if len(cmd) == 2:
                self.item_list(cmd[1])
        elif cmd[0].lower() == 'use':
            if len(cmd) == 2:
                self.use_module(cmd[1])
        elif cmd[0].lower() == 'interact':
            if len(cmd) == 2:
                self.interact_session(cmd[1])
        elif cmd[0].lower() == 'info':
            if len(cmd) == 2:
                if cmd[1].isnumeric():
                    if int(cmd[1]) < len(self.__module_cache):
                        obj = self.__module_cache[int(cmd[1])]
                        obj.show_info()
                obj = self.get_module(cmd[1])
                if obj != None:
                    obj.show_info()
                else:
                    obj = self.get_session(cmd[1])
                    if obj != None:
                        obj.show_info()
                    else:
                        obj = self.get_plugin(cmd[1])
                        if obj:
                            obj.show_info()
                        else:
                            print(f"[!] The object with name {cmd[1]} does not found!")
        elif cmd[0].lower() == 'sessions':
            self.item_list('sessions')
        elif cmd[0].lower() == 'test':
            self.testmethod()
        elif cmd[0].lower() == 'reload':
            self.reload_resources()
        else:
            # Check cmd[0] is a module name and module run_with_args() function
            modname = cmd[0].lower()
            module = self.get_module(modname)
            if module:
                module.run_with_args(command)
                
    def interact_session(self,sessname):
        """
        Interact with a Session with a given name or number
        """
        found = False
        if sessname.isnumeric():
            integer = int(sessname)
            if integer < len(self.sessions):
                sess = self.sessions[integer]
                if sess:    
                    self.plugin_autoload(sess) # testing purposes
                    sess.interactive()     
            else:
                print("[x] Invalid session number")
        else:
            for s in self.sessions:
                if s.name == sessname:
                    found = True
                    self.plugin_autoload(sess) # testing purposes
                    s.interactive()
                    break
            if not found:
                print(f"[x] Cannot find active session with name [{sessname}]")
                
    def item_list(self,item_type):
        item_type = item_type.lower()
        result_array = []
        counter = 0
        header = []
        if item_type == 'modules':
            self.__module_cache.clear()
            header = ['#','Name','Type','Command','Description']
            for m in self.modules:
                result_array.append([counter,m.info.module_name,m.module_type.name,m.info.command,m.info.name])
                counter += 1
            
        if item_type == 'sessions':
            header = ['#','Name','Remote Address','Client Type','Platform','Hostname','Username']
            for s in self.sessions:
                rhost = s.get_rhost()
                rport = s.get_rport()
                result_array.append([counter,s.name,(rhost+":"+rport),s.client_type.name,s.platform,s.hostname,s.username])
                counter += 1   
        if item_type == 'jobs':
            pass
        if item_type == 'plugins':
            header = ['#','Module Name','Type','Command','Description']
            for p in self.plugins:
                result_array.append([counter,str(p.info.module_name),p.plugin_type.name,p.info.command,p.info.name])
                counter += 1
            
            
        print()
        print(tabulate(result_array,headers=header))
        print()
        
    def use_module(self,module):
        if module.isnumeric():
            integer = int(module)
            if integer < len(self.modules):
                module = self.modules[integer]
                module.interactive()
        else:
            for m in self.modules:
                if m.info.name == module:
                    m.interactive()
                    break
                elif m.info.module_name == module:
                    m.interactive()
                    break
                elif m.info.command == module:
                    m.interactive()
                    break
        
    def show_help(self):
        header = ['Command','Description']
        print()
        print(tabulate(self.help,headers=header))
        print()
    def show_module_info(self,modname):
        if module.isnumeric():
            integer = int(module)
            if integer < len(self.modules):
                module = self.modules[integer]
                module.show_info()
        else:
            for m in self.modules:
                if m.name == module_name:
                    m.show_info()
                    break
    
    def get_module(self,name):
        for m in self.modules:
            if m.info.command == name:
                return m
            elif m.info.name == name:
                return m
            elif m.info.module_name == name:
                return m
        return None
    def get_session(self,name):
        for s in self.sessions:
            if s.name == name:
                return s
        return None
    def get_plugin(self,name):
        for s in self.plugins:
            if s.info.module_name == name:
                return s
            elif s.info.name == name:
                return s
            elif s.info.command == name:
                return s
        return None
    def add_session(self,sess):
        self.sessions.append(sess)
        sess.onSessionDead += self.sessionDeadEventHandler
        # run initial enum data
        sess.enuminfo()
        
    def sessionDeadEventHandler(self,session):
        s = self.get_session(session.name)
        if s:
            print(f"[*] Session {session.name} was deleted from sessions.")
            self.sessions.remove(session)
            

            
    def testmethod(self):
        from phoenix.ExecCode import ExecCode
        s = self.sessions[0]
        e = ExecCode(s.get_socket())
        result = e.execute('uname -a')
        print(result)
    def reload_resources(self):
        try:
            print("[*] Realoading resources")
            from phoenix.ModuleLoader import ModuleLoader
            loader = ModuleLoader()
            loader.paths = ['modules','phoenix/builtin']
            loader.load()
            self.modules = loader.modules
            self.plugins = loader.plugins
            print(f"[+] Successfully loaded {str(len(self.modules))} modules and {str(len(self.plugins))} plugins")
        except:
            print("[x] Error occurred while reloading resources.")
    def load_modules(self):
        loader = ModuleLoader()
        loader.paths = self.load_paths
        loader.load()        
        self.modules = loader.modules
        self.plugins = loader.plugins
        
    def init_tabmanager(self):
        # Initialize a new Tabulate Completer Object
        # Thsi is the Default one
        help_tab= TabCompleter('')
        help_tab.choices = self._get_help_tabs()
        
        modules_tab = TabCompleter('use')
        modules_tab.choices = self._get_module_names()
        
        # Add Tabcompleters to tabmanager
        self.tabman.add_completer(help_tab)
        self.tabman.add_completer(modules_tab) 
        
        session_tab = TabCompleter('interact')
        session_tab.choices = []
        
    def _shutdown_sockets(self):
        for s in self.sessions:
            try:
                s.client.close()
            except:
                pass
    def _get_help_tabs(self):
        """Got the HELP tabs for completer"""
        return [i[0].split(' ',1)[0] for i in self.help]
    def _get_module_names(self):
        return [i.info.module_name for i in self.modules]
    def plugin_autoload(self,sess):
        for p in self.plugins:
            sess.plugins.append(p)