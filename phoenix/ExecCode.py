"""
Executes OS command in the context of the given session
"""


class ExecCode:
    def __init__(self,session_client):
        self.client = session_client
        self.blocking = False
    def execute(self,command):
        if not command.endswith('\n'):
            command += '\n'
        self.client.send(command)
        result = self.client.receive_all()
        return result
    def setblocking(self,blocking):
        try:
            num = int(blocking)
            if num == 1:
                self.blocking = True
            else:
                self.blocking = False
        except:
            print("The blocking must be 0 or 1")