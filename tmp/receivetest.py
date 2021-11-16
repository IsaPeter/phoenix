"""Timeout tester"""
import socket,time

client = socket.socket()
client.connect(('127.0.0.1',9001))

def receive_all(client):
    client.setblocking(0)
    recv_len = 1
    response = b''
    s = None
    ndc = 0
    receive = True
    while receive:
        try:
            if ndc > 3: receive = False 
            
            data = client.recv(8096)
            if data:
                response += data
                recv_len = len(data)
                
            else:
                if ndc <= 3:
                    ndc += 1
                    time.sleep(0.1)
                else:
                    receive = False
        except:
            ndc += 1
    return response.decode(encoding='latin-1')

                
            
def receive_timeout(client):
    #make socket non blocking
    #client.setblocking(0)
    
    #total data partwise in an array
    total_data=b"";
    data='';       
    timeout = 2
    no_data_cnt = 0
    
    #beginning time
    begin=time.time()        
    
    while True:
        #if you got some data, then break after timeout
        if total_data and time.time()-begin > timeout:
            break
        if no_data_cnt > 2:
            break
        #if you got no data at all, wait a little longer, twice the timeout
        #elif time.time()-begin > timeout*2:
        #    break            
    
        #recv something
        try:
            data = client.recv(8096)
            if data:
                total_data += data
                no_data_cnt = 0
                #change the beginning time for measurement
                begin = time.time()
            else:
                #sleep for sometime to indicate a gap
                #time.sleep(0.1)
                no_data_cnt = no_data_cnt +1
                print("NO Data CNT: "+str(no_data_cnt))
                pass
        except:
            pass
        

    #join all parts to make final string
    return ''.join(total_data.decode())


while True:
    cmd = input('> ')
    client.send((cmd+'\n').encode())
    result = receive_all(client)
    print(result)
