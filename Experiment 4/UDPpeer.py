import socket
import sys, threading, time


class UDPPeer:
    hostname = ''
    addr = ''
    peersList = []
    ServerPort = 6969
    ClientPort = 42069
    serverRunning = True
    clientRunning = True

    def quit(self):
        print("Quit")
        self.serverRunning = False
        self.clientRunning = False

    def clientSide(self):
        print("Starting Client Thread")

        try:
            clientS = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            clientS.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            clientS.settimeout(3)
            while self.clientRunning:
                self.waitingForInput = True
                typedInput = input("Input message to send: ")
                self.waitingForInput = False
                if typedInput == 'Quit':
                    message = ' Peer Quit ' + self.addr
                else:
                    message = typedInput
                for peer in self.peersList:
                    try:
                        clientS.sendto(message.encode(), (peer, self.ServerPort))
                        responseMessage, peerAddress = clientS.recvfrom(2048)
                    except KeyboardInterrupt:
                        print("Keyboard Interrupt!")
                        exit(1)
                    except TimeoutError as ex:
                        self.peersList.remove(peer)
                        print("Removed ", peer, " from peersList")
        except KeyboardInterrupt:
            print("Keyboard Interrupt!")
            exit()
        time.sleep(1)

    def serverSide(self):
        print("Starting Server Thread")
        try:
            serverS = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            serverS.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            serverS.bind(('', self.ServerPort))
            print("Server is ready to receive.")
            while self.serverRunning:
                message, clientAddress = serverS.recvfrom(2048)
                print("Message Received from: ", clientAddress)
                print(message.decode())
                if (clientAddress[0] not in self.peersList):
                    self.peersList.append(clientAddress[0])
                    time.sleep(1)
                elif (clientAddress in self.peersList) and (message.decode()[0:18] == ' Peer Quit '):
                    self.peersList.remove(clientAddress[0])
                    print("Removed ", clientAddress[0], " from peersList")
        except KeyboardInterrupt:
            print("Keyboard Interrupt!")
            exit()

    def __init__(self):
        self.hostname = socket.gethostname()
        self.addr = socket.gethostbyname(self.hostname)
        print("Server runs on ", self.hostname, " at ",self.addr)
        self.serverRunning = True
        try:
            BroadcastS = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            BroadcastS.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            BroadcastS.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            broadcastMessage = ' Peer Active ' + self.addr
            BroadcastS.sendto(broadcastMessage.encode(), ('<broadcast>', 6969))
            BroadcastS.close
        except KeyboardInterrupt:
            print("Keyboard Interrupt")
            exit()
        try:
            serverThread = threading.Thread(target=self.serverSide, args=())
            clientThread = threading.Thread(target=self.clientSide, args=())
            serverThread.start()
            clientThread.start()
        except KeyboardInterrupt:
            print("Keyboard Interrupt")
            exit()

UDPPeer()