#!/usr/bin/env python3
"""
ArgumentParser
"""
import re

class ArgumentParser():
    def __init__(self,name="appname"):
        self.description = ""
        self.name = name
        self.arguments = []
        self.subparsers = []
        self._set_help() # Set the help option
        self.show_help = False
        
    def set_description(self,desc):
        self.description = desc
    def print_help(self):
        self._print_usage()
        self._print_arguments()
        print()
        
    def add_argument(self,*args,name="",help="",hasvalue=True):
        a = Argument(name,help,hasvalue)
        a.set_arguments(args)
        self.arguments.append(a)
    def add_subparser(self,subparser,name):
        self.subparsers.append(subparser)
    def parse_arguments(self,instring):
        result_arr = {}
        for a in self.arguments:
            a.parse(instring)
            if a.hasresult:
                d = {a.name:a.value}
                result_arr.update(d)
                if list(d.keys())[0] == "help":
                    self.show_help = True
        if self.show_help:
            self.print_help()
        return result_arr
    
    
    def _print_usage(self):
        usage_str = f"Usage: {self.name} "
        for a in self.arguments:
            arg_str = "["
            for ag in a.arguments:
                arg_str += ag + '|'
            arg_str = arg_str.rstrip('|')+"] "
            usage_str += arg_str
        
        print(usage_str)
    
    
    def _print_arguments(self):
        print("\nOptional Arguments:\n")
        for a in self.arguments:
            ag_str = ""
            for ag in a.arguments:
                ag_str +=ag+","
            ag_str = ag_str.rstrip(',')+f'\t\t{a.help}'
            print(ag_str)
    def _set_help(self):
        a = Argument(name="help",hasvalue=False,help="Show the help menu")
        a.add_argument('--help')
        self.arguments.append(a)
            
    
    
class Argument():
    def __init__(self,name="",help="",hasvalue=True):
        super().__init__()
        self.arguments = []
        self.name = name
        self.uniquename = False
        if name != '':
            self.uniquename = True
        self.value = ""
        self.patterns = []
        self.hasvalue = hasvalue
        self.help = help
        self.hasresult = False
        
        
    def add_argument(self,arg):
        self.arguments.append(arg)
        self._get_longest_arg() 
        self._get_patterns()
    def set_arguments(self,args):
        self.arguments = args
        self._get_longest_arg()  
        self._get_patterns()
    def parse(self,instring):
        result = []
        for p in self.patterns:
            match = re.findall(p,instring,re.M|re.I)
            if match:
                self.hasresult = True
                if bool(self.hasvalue):
                    if len(match) == 1:
                        self.value = self._trim_value(match[0])
                    else:
                        self.value = []
                        for m in match:
                            self.value.append(m)
                else:
                    self.value = True
        
    def _trim_value(self,value):
        if value.startswith("\""):
            value = value.lstrip("\"")
        if value.endswith("\""):
            value = value.rstrip("\"")            
        return value
            
    def _get_patterns(self):
        self.patterns.clear()
        for a in self.arguments:
            if self.hasvalue:
                self.patterns.append(fr"{a} (\S+)")
            else:
                self.patterns.append(fr"{a}")
    def _get_longest_arg(self):        
        if self.uniquename == False:
            count = 0
            argname = ""
            for a in self.arguments:
                ar = a.replace('-','')
                if len(ar) > count:
                    count = len(ar)
                    argname = ar
            self.name = argname







"""
teststring = "application upload -f /etc/passwd"

parser = ArgumentParser(name="transfer")
parser.add_argument('upload',hasvalue=False,name="upload",help="set upload")
parser.add_argument('-f','--file',name="file",help="set file name")
parser.add_argument('-p',"--path",name="path",help="set file path")
args = parser.parse_arguments(teststring)
parser.print_help()
print(args)
"""