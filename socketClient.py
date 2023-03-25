import socket

s = socket.socket()
port = 8574
s.connect(('10.0.1.1', port))

print('Connected')

def send(msg):
    s.send(str(msg).encode())