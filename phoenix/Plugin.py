from enum import Enum
from phoenix.ModuleOptions import ModuleOptions
from phoenix.ModuleInfo import ModuleInfo
from tabulate import tabulate
from phoenix.ArgumentParser import ArgumentParser


class Plugin():
    def __init__(self):
        self.options = ModuleOptions()
        self.info = ModuleInfo()
        
        self.plugin_type = plugin_type.Native
        self.parser = ArgumentParser()
        
    def run(self):
        pass
    def run_with_args(self,command):
        print("[*] The function not implemented yet!")
    def show_info(self):
        print()
        print(tabulate(self.info.get_array()))
        print()      
    def show_options(self):
        self.parser.print_help()
    
    
    
    
class plugin_type(Enum):
    Native = 0
    Phoenix = 1