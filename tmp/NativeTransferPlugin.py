"""
Native Plugin for Data Transfer
"""
import phoenix.Plugin
from phoenix.ArgumentParser import ArgumentParser

class NativePlugin(Plugin):
    def __init__(self):
        super().__init__()
        self.info.name = "Native Data Transfer"
        self.info.alias = "transfer"
        self.plugin_type = plugin_type.Native
        self.info.description = "This Plugin helps to transfer data between attacker and victim."
    
    def run_with_args(self,command):
        parser = ArgumentParser(name="transfer")
        parser.add_argument('upload',hasvalue=False,name="upload",help="Upload File to the target machine.")
        parser.add_argument('download',hasvalue=False,name="download",help="Download File from the target machine.")
        parser.add_argument('-f','--file',name="file",help="Set uploaded file name.")
        parser.add_argument('-p',"--path",name="path",help="Set upload target path.")
        args = parser.parse_arguments(teststring)
