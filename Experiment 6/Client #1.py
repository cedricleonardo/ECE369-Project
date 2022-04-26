from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter

HOST = input('Enter host: ')
PORT = input('Enter port: ')
if not PORT:
    PORT = 6969
else:
    PORT = int(PORT)

BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

# Infinite loop to receive messages, .recv blocks execution until a message is received
def receive():
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            msg_list.insert(tkinter.END, msg)
        except OSError:
            break

# event is used when passed by send button on Tkinter
# my_msg is the input to the GUI, message is extracted and sent to the server
# If the message is !DISCONNECT, socket and GUI is closed
def send(event=None):
    msg = my_msg.get()
    my_msg.set("")
    client_socket.send(bytes(msg, "utf8"))
    if msg == "!DISCONNECT":
        client_socket.close()
        top.quit()

# When the GUI is closed, message is sent
def on_closing(event=None):
    my_msg.set("!DISCONNECT")
    send()

# Top level widget is set and named
top = tkinter.Tk()
top.title("Client #1")

# Frame for holding the list of messages
# String stores the values from the input
messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()
my_msg.set("Type messages here.")
scrollbar = tkinter.Scrollbar(messages_frame)

# Scrollbar for scrolling through the messages
msg_list = tkinter.Listbox(messages_frame, height=30, width=70, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()

messages_frame.pack()

# Input field to input users messages, messages are binded to the string variable
# Send button is created if the user does not want to press return to send the messages, can click button instead
# on_closing is used for clean up when GUI is closed
entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text="Send", command=send)
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)

# Thread is started to receive messages, GUI is made yellow
receive_thread = Thread(target=receive)
receive_thread.start()
top.configure(bg='yellow')
msg_list.configure(bg='yellow')
messages_frame.configure(bg='yellow')
tkinter.mainloop()