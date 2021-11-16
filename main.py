#!/usr/bin/env python3
from phoenix.ModuleLoader import ModuleLoader
from phoenix.Phoenix import Phoenix
from phoenix.Shared import shared


        
def load_logo():
    try:
        with open('./phoenix/logo','r') as l:
            logo_string = l.read()
        if logo_string:
            print(logo_string+'\n\n')
    except:
        print("[x] Failed to load application logo!")
        
        
def load_modules():
    loader = ModuleLoader()
    loader.paths = ['modules','phoenix/builtin']
    loader.load()
    
    return loader.modules,loader.plugins

def main():
    phoenix = Phoenix()
    shared.phoenix = phoenix
    load_logo()
    #modules,plugins = load_modules()
    #phoenix.modules = modules
    #phoenix.plugins = plugins
    phoenix.load_paths = ['modules','phoenix/builtin']
    phoenix.load_modules()
    phoenix.init_tabmanager()
    phoenix.run()
    
    
if __name__ == '__main__':
    main()



