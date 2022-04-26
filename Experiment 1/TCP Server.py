import socket

server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host = socket.gethostname()
print('Server runs on ', host, 'at ', socket.gethostbyname(host))
server_socket.bind(('127.0.0.1',12345))
server_socket.listen(5)

while True:
    print("Server is waiting for a connection")
    client_socket,addr=server_socket.accept()
    print("The client has connected from",addr)
    while True:
        data=client_socket.recv(1024)
        if not data or data.decode('utf-8')=='END':
            break
        print("A message has been received from the client \nClient: %s"% data.decode("utf-8"))
        try:
            client_socket.send(bytes('Hello Client','utf-8'))
        except:
            print("Exited by user")
    client_socket.close()
server_socket.close()