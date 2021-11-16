#!/usr/bin/env python3
import readline

class TabCompleter:
    def __init__(self,name='Completer'):
        self.name = name
        self.choices = []
        
        #readline.parse_and_bind("tab: complete")
        #readline.set_completer(self.complete)        

    def complete(self,text, state):
        for cmd in self.choices:
            if cmd.startswith(text):
                if not state:
                    return cmd
                else:
                    state -= 1
    def clear(self):
        self.choices.clear()
    


class TabManager:
    def __init__(self):
        self.completers = []
        self.default_completer = None
        readline.parse_and_bind("tab: complete")
        readline.set_completer(self.complete)
        
    def add_completer(self,completer):
        self.completers.append(completer)
        if len(self.completers) == 1: self.default_completer = completer
    def set_default_completer(self,completer):
        self.default_completer = completer
        if completer not in self.completers:
            self.completers.append(completer)
    def get_completer(self,name):
        lastword = name.split(' ')[-1]
        for c in self.completers:
            if c.name == lastword:
                return c
        return None
    def complete(self,text,state):
        buffer = readline.get_line_buffer()
        if ' ' in buffer:
            cname = buffer.split(' ')[0]
            comp = self.get_completer(cname)
        else:
            comp = self.get_completer(text)
            
        if comp:
            return comp.complete(text,state)
        else:
            if self.default_completer:
                return self.default_completer.complete(text,state)
    
"""
tc = TabCompleter()
tc.choices = ['import','importModule','importPlugin','importPluginData','use','interact','almafa']

while True:
    cmd = input('> ')
"""


"""
# TESTING

tm = TabManager()
tc = TabCompleter('')
tc.choices = ['import','importModule','importPlugin','importPluginData','use','interact','almafa']

tc1 = TabCompleter('use')
tc1.choices = ['module1','module2','module3','module4']

tc2 = TabCompleter('interact')
tc2.choices = ['AAAA','BBBB','CCCC']

tc3 = TabCompleter('almafa')
tc3.choices = ['almafa','kortefa','szilvafa']

tm.add_completer(tc)
tm.add_completer(tc1)
tm.add_completer(tc2)
tm.add_completer(tc3)

#readline.parse_and_bind("tab: complete")
#readline.set_completer(tm.complete)

while True:
    cmd = input('> ')
"""
