#!/usr/bin/env python3

class ModuleInfo:
    def __init__(self):
        self.name = ""
        self.module_name = ""
        self.command = ""
        self.description = ""
        self.version = ""
        self.authors = []
        self.references = []
        self.platforms = []
        self.arch = []
        self.module_type = ""
        self.classes = []
        
    def get_array(self):
        result = []
        if self.name != "": result.append(['Name',self.name])
        if self.command != "": result.append(['Command',self.command])
        if self.description != "": result.append(['Description',self.description])
        if self.version != "": result.append(['Version',self.version])
        if self.module_type != "": result.append(['Module Type',self.module_type])
        if len(self.authors)>0: result.append(['Authors',', '.join(a for a in self.authors)])
        if len(self.references)>0: result.append(['References',', '.join(a for a in self.references)])
        if len(self.platforms)>0: result.append(['Platforms',', '.join(a for a in self.platforms)])
        if len(self.arch)>0: result.append(['Arch',', '.join(a for a in self.arch)])
        if len(self.classes)>0: result.append(['Classes',', '.join(a for a in self.classes)])
        return result
    
    
"""
from tabulate import tabulate
info = ModuleInfo()
info.name = "Module Name"
info.alias = "Module_alias"
info.version = '1.0'
info.authors.append('Peter Isa')
info.authors.append('Ráduly Viki')
info.platforms.extend(['Linux','Windows'])
info.arch.extend(['x86','x64'])
info.module_type = "Phoenix"

print(tabulate(info.get_array()))
"""