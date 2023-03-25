import socket

server = socket.socket()
port = 8574
host = socket.gethostname()

server.bind((host, port))
server.listen(2)
conn, address = server.accept()
print("Connection from: " + str(address))

while True:
    data = conn.recv(1024).decode()
    if not data:
        break
    print("from connected user: " + str(data))
    conn.send(str('got your data').encode())

conn.close()