from socket import *
import sys
import time

timeout=1

clientSocket = socket(AF_INET, SOCK_DGRAM)
while True:
    message = input("Type a message: ")
    clientSocket.settimeout(timeout)
    try:
        Ti = time.time()
        clientSocket.sendto(message.encode("utf-8"), ('127.0.0.1',12345))
        modifiedMessage, serverAddress = clientSocket.recvfrom(1024)
        time.sleep(0.5)
        Tj = time.time()
        print("Received echo: " , modifiedMessage.decode(), " in RTT: ", str(Tj-Ti))
    except:
        print('Time out! Message is lost.')
    if message == 'quit' or message == 'shutdown':
        print('Client quits!')
        break
clientSocket.close()
sys.exit(0)

