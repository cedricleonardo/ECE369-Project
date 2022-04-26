import socket

client_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1',12345))

message = 'Hello Server'

try:
    while True:
        client_socket.send(message.encode('utf-8'))
        data=client_socket.recv(1024)
        print(str(data))
        more=input('Would you like to send more data to the server?')
        if more.lower()=='y':
            message=input("Enter Message: ")
        else:
            break
except KeyboardInterrupt:
    print("Exited by the User")
client_socket.close()