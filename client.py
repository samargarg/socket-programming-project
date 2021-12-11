import socket
import threading

HEADER = 64
PORT = 7000
FORMAT= 'utf-8'
DISCONNECT = '!disconnect'
# SERVER = '103.232.241.185'
SERVER = '169.254.234.39'

ADDR=(SERVER,PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def send(msg):
    message =msg.encode(FORMAT)
    msg_length =len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
def receive():
    while True:
        msg_length = client.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = client.recv(msg_length).decode(FORMAT)
            if msg==DISCONNECT:
                return
            print(msg)


nickname = input(client.recv(1024).decode(FORMAT))
client.send(nickname.encode(FORMAT))

# send('Hello World!')
msg=''
thread = threading.Thread(target=receive, args=() )
thread.start()

while True:
    msg=input(' ')
    send(msg)
    if msg==DISCONNECT:
        break
    # receive()
# client.close()
# thread._Thread_stop()