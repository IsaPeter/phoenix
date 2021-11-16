#!/usr/bin/env python3


class ModuleOptions:
    def __init__(self):
        self.options = []
        self.case_insensitive = True
    def register_option(self,option):
        self.options.append(option)
    def add(self,name="",value="",required=False,description=""):
        o = Option(name,value,required,description)
        self.options.append(o)
    def option_is_exists(self,name):
        for o in self.options:
            if self.case_insensitive:
                if o.name.lower() == name.lower():
                    return True
            else:
                if o.name == name:
                    return True
        return False
    def get(self,name):
        for o in self.options:
            if self.case_insensitive:
                if name.lower() == o.name.lower():
                    return o
            else:
                if name == o.name:
                    return o
        return None
    def get_value(self,name):
        o = self.get(name)
        if o:
            return o.value
        else:
            return None
    def set_value(self,name,value):
        o = self.get(name)
        if o:
            o.value = value
        else:
            print(f"[x] Option with name {name}, does not exists!")   
    def get_array(self):
        result = []
        for o in self.options:
            a = [o.name,o.value,o.required,o.description]
            result.append(a)
        return result
    
    
    
    
class Option:
    def __init__(self,name="",value="",required=False,description=""):
        self.name = name
        self.value = value
        self.required = required
        self.description = description
    def has_value(self):
        if self.value != "":
            return True
        else:
            return False
    
    
"""
Testing Section
"""
"""
options = ModuleOptions()
options.add('LHOST','0.0.0.0',True,'This is LHOST')
options.add('LPORT','9001',True,"This is LPORT")

options.set_value('lport','8888')
print(tabulate(options.get_array()))
"""