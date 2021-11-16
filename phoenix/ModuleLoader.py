#!/usr/bin/env python3
import glob,importlib
from pathlib import Path

class ModuleLoader():
    def __init__(self):
        self.path = ''
        self.modules = []
        self.plugins = []
        self.paths = []
        
    def load_from_path(self,path):
        p = Path(path)
        self.path = path
        for file in p.glob('**/*.py'):
            f = str(file).replace('/','.').replace('.py','')
            m = importlib.import_module(f)        
            if 'PhoenixModule' in dir(m):
                module = m.PhoenixModule()
                self.modules.append(module)
            elif 'NativeModule' in dir(m):
                module = m.NativeModule()
                self.modules.append(module)
            elif 'NativePlugin' in dir(m):
                plugin = m.NativePlugin()
                self.plugins.append(plugin)
            elif 'PhoenixPlugin' in dir(m):
                plugin = m.PhoenixPlugin()
                self.plugins.append(plugin)                
                
        return self.modules
    
    def load(self,reload=False):
        for path in self.paths:
            p = Path(path)
            for file in p.glob('**/*.py'):
                f = str(file).replace('/','.').replace('.py','')
                if reload:
                    m = importlib.reload(f)
                else:
                    m = importlib.import_module(f)        
                if 'PhoenixModule' in dir(m):
                    module = m.PhoenixModule()
                    self.modules.append(module)
                elif 'NativeModule' in dir(m):
                    module = m.NativeModule()
                    self.modules.append(module)
                elif 'NativePlugin' in dir(m):
                    plugin = m.NativePlugin()
                    self.plugins.append(plugin)
                elif 'PhoenixPlugin' in dir(m):
                    plugin = m.PhoenixPlugin()
                    self.plugins.append(plugin)                
                    
  
    def reload(self):
        self.modules.clear()
        self.plugins.clear()
        if self.path != "":
            self.paths.append(self.path)
        else:
            self.load(reload=True)


