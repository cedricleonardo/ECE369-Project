import socket

while True:
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        host = socket.gethostname()
        print('Server runs on ', host, 'at ', socket.gethostbyname(host))
        sock.bind(('127.0.0.1', 12345))
        print("The server is now receiving any message.")

        while 1:
            data, addr = sock.recvfrom(1024)
            modifiedMessage = data.decode()
            sock.sendto(modifiedMessage.encode(), addr)

    except KeyboardInterrupt:
        print("Keyboard interrupt")
        exit(1)