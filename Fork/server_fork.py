import os, time, sys
from socket import *                     
ThreadCount = 0  
myHost = '127.0.0.1'                              
myPort = 12345                         
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>" 

sockobj = socket(AF_INET, SOCK_STREAM)           
sockobj.bind((myHost, myPort))                   
print('Socket is listening..')
sockobj.listen(5)             

def now():                                       
    return time.ctime(time.time())

activeChildren = []
def reapChildren():                              
    while activeChildren:                        
     pid,stat = os.waitpid(0, os.WNOHANG)     
     if not pid: break
     activeChildren.remove(pid)

def handleClient(connection):
    connection.send(str.encode('Server is working:'))
    s_time = time.time()
    while 1:                                     
        data = connection.recv(2048)             
        response = 'Server message: ' + data.decode('utf-8','ignore')
        if not data: 
         break
    e_time = time.time()
    connection.close() 
    print('Time Taken: ',e_time-s_time,"seconds")
    os._exit(0)

def dispatcher():                                
    while 1:                                      
        connection, address = sockobj.accept()   
        print('Connected to: ' + address[0] + ':' + str(address[1]))
        reapChildren()                           
        childPid = os.fork()                     
        if childPid == 0:                        
            handleClient(connection)
        else:                                    
            activeChildren.append(childPid)      

dispatcher()