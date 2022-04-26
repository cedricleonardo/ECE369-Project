from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

clients = {}
addresses = {}
HOST = ''
PORT = 6969
BUFSIZ = 1024
ADDR = (HOST, PORT)
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

# Sets up incoming clients
# Infinite loop that waits forever for incoming connections
# When connected the connection is logged, stored, and thread is handled
def accept_incoming_connections():
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("Welcome to my Chat Room! Type your name in the box below and press Enter.", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()

# Saves the name of the client that was inputted by the user and sends a message to the client discussing how to quit the chatroom
# If the message contains !DISCONNECT the client will disconnect
# If no !DISCONNECT, clients message is broadcasted to other clients
def handle_client(client):

    name = client.recv(BUFSIZ).decode("utf8")
    welcome = 'Welcome %s! If you ever want to quit, type !DISCONNECT to exit.' % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s has joined the chat!" % name
    broadcast(bytes(msg, "utf8"))
    clients[client] = name

    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("!DISCONNECT", "utf8"):
            broadcast(msg, name + ": ")
        else:
            client.send(bytes("!DISCONNECT", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s has left the chat." % name, "utf8"))
            break

# Broadcasts messages to all connected clients
def broadcast(msg, prefix=""):
    for sock in clients:
        sock.send(bytes(prefix, "utf8") + msg)

# Thread is accepted and joined, waits for completion so server is not closed
if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()