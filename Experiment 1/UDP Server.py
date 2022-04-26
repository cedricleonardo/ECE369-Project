import socket

sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
host = socket.gethostname()
print('Server runs on ', host, 'at ', socket.gethostbyname(host))
sock.bind(('127.0.0.1',12345))

while True:
    data, addr = sock.recvfrom(4096)
    print("Client connected from", addr)
    print(str(data))
    message = bytes(("Hello, this is the UDP Server").encode('utf-8'))
    sock.sendto(message, addr)
