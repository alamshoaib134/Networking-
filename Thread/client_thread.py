import os.path
import socket
import tqdm
import time
start_time = time.time()
ClientMultiSocket = socket.socket()
host = '127.0.0.1'
port = 2004
filename = "War_and_Peace.txt"
filesize = os.path.getsize(filename)
SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096 # send 4096 bytes each time step

print('Waiting for connection response')
try:
    ClientMultiSocket.connect((host, port))
except socket.error as e:
    print(str(e))

ClientMultiSocket.send(f"{filename}{SEPARATOR}{filesize}".encode())

res = ClientMultiSocket.recv(1024)
progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
with open(filename, "rb") as f:
    while True:
        bytes_read = f.read(BUFFER_SIZE)
        if not bytes_read:
            break
        ClientMultiSocket.sendall(bytes_read)
        progress.update(len(bytes_read))
# close the socket

endtime = time.time()
ClientMultiSocket.close()
print()
print("Elapsed Time: ",endtime-start_time)

