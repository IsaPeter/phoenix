#!/usr/bin/env python3
import readline

class TabCompleter:
    def __init__(self):
        self.choices = []
        readline.parse_and_bind("tab: complete")
        readline.set_completer(self.complete)        

    def complete(self,text, state):
        for cmd in self.choices:
            if cmd.startswith(text):
                if not state:
                    return cmd
                else:
                    state -= 1
    def clear(self):
        self.choices.clear()
    


"""
# TESTING

tc = TabCompleter()
tc.choices = ['import','importModule','importPlugin','importPluginData']
"""    

