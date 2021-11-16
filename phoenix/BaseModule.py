#!/usr/bin/env python3
from tabulate import tabulate
from phoenix.ModuleInfo import ModuleInfo
from phoenix.ModuleOptions import ModuleOptions
from enum import Enum
from phoenix.Colors import colors
"""
Default Instance of the Phoenix Base Module
Author: Peter Isa
"""

class BaseModule:
	def __init__(self):
		self.info = ModuleInfo()
		self.options = ModuleOptions()
		self.module_interactive = False
		self.module_type = module_type.Native
		
	def run(self):
		if self.__check_requirements():
			print("[+] Executed Successfully")
			# Run the module
		pass
	def run_with_args(self,*args,**kwargs):
		print("[!] The function does not implemented yet!")
		pass
	def check(self):
		print("[*] The Check funcion is not implemented for this module!")
	def show_options(self):
		print()
		print(tabulate(self.options.get_array(), headers=['Name', 'Value','Required','Description']))
		print()
	def show_info(self):
		"""
		data = [
		    ['Name',self.info['Name']],
		    ['Alias',self.info['Alias']],
		    ['Description',self.info['Description']],
		    ['Author', ', '.join(a['Name'] for a in self.info['Author'])],
		    ['References','\n'.join([t for k in [d.values() for d in [data for data in self.info['References']]]for t in k])],
		    ['Platform',', '.join(k for k in self.info['Platform'])],
		    ['Arch',', '.join(k for k in self.info['Arch'])],
		    ['Type',', '.join(k for k in self.info['Type'])],
		    ['Class',', '.join(k for k in self.info['Class'])],
		    ['Version',self.info['Version']]
		]
		"""
		print()
		print(tabulate(self.info.get_array()))
		print()         
        
	def interactive(self):
		self.module_interactive = True
		# Create prompt string
		input_str = ""
		if self.info.module_name != "":
			input_str = f'Phoenix({colors.OKGREEN+self.info.module_name+colors.ENDC})> '
		else:
			input_str = f'Phoenix({colors.OKGREEN+self.info.name+colors.ENDC})> '
	    
		while self.module_interactive:
			cmd = input(input_str)
			self.command_interpreter(cmd.split(' '))

	def command_interpreter(self,command):
		# Exit from the module
		if command[0].lower() in ['exit','bg']: self.module_interactive = False
		elif command[0].lower() == 'set':
			if len(command) == 3:
				if self.options.option_is_exists(command[1]):
					self.options.set_value(command[1],command[2])
					print(f"[+] {command[1].upper()} ==> {command[2]}")
				else:
					print(f"[!] {command[1]} does not exists in the Options!") 
			else:
				print("[!] Not enough parameter given.")
		elif command[0].lower() == 'unset':
			if len(command) == 2:
				if self.options.option_is_exists(command[1]):
					self.options.set_value(command[1],"")
					print(f"[+] Successfulyl unset {command[1].upper()}")
				else:
					print(f"[!] {command[1]} does not exists in the Options!")
			else:
				print("[!] Not enough parameter given.")
		elif command[0].lower() in ['run','exploit']:
			self.run()
		elif command[0].lower() == 'show':
			if len(command) == 2:
				if command[1].lower() == 'options':
					self.show_options()
				if command[1].lower() == 'info':
					self.show_info()
		elif command[0].lower() == 'options':
			self.show_options()
		elif command[0].lower() == 'info':
			self.show_info()
		elif command[0].lower() == 'check':
			self.check()
	    
	def check_requirements(self):
		requirements_passed = True
		for o in self.options.options:
			if o.required == True and o.has_value() == False:
				requirements_passed = False
				print(f"[!] The {o[0]} must required to be set!")
				break
		return requirements_passed
	



class module_type(Enum):
	Native = 0
	Phoenix = 1

"""
This is a testing module
"""
"""
class phoenix_module(base_module):
    def __init__(self):
        super().__init__()
        self.info = {
                'Name' : 'PostgreSQL Remote Code Exec',
                'Alias':'postgres_remote_exec',
                'Description':'Remote Code Execution in the Postgre SQL.',
                'Author': [
                    {'Name':'Peter Isa'}
                ],
                'References':[
                    {'CVE':'CVE-2021-1546'},
                    {'URL':'http://webpage.com/CVE-2021-1546'}
                ],
                'Platform':['Linux'],
                'Arch':['x64'],
                'Type':['Phoenix','Native'],
                'Class':['Post','Exec','RCE','Authenticated'],
                'Options':[
                    ['RHOST','',True,"The remote host"],
                    ['RPORT','5432',True,"The remote port"],
                    ['LHOST','127.0.0.1',False,"The local host"],
                    ['LPORT','4444',False,"The local port"]
                ]
            }        
        
      
pm = phoenix_module()
pm.interactive()
"""