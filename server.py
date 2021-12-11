import socket
import threading

HEADER = 64 #bytes To get length of msg about to be received
IP = socket.gethostbyname(socket.gethostname()) #SERVER IP
# IP = '152.57.92.228'  ## localhost IP='127.0.0.1'
PORT= 7000
ADDR=( IP, PORT )
FORMAT='utf-8'
DISCONNECT='!disconnect'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Created socket!!')
server.bind(ADDR)
print('Server binded')

clients=[]
nicknames=[]

#broadcast
def broadcast(message):
    message =message.encode(FORMAT)
    msg_length =len(message)
    for client in clients:
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        client.send(send_length)
        client.send(message)

#send msg individual
def send(conn,addr,msg):
    print('Sending {msg} to {addr}')
    msg=msg.encode(FORMAT)
    conn.send(msg)

#handle
def handle_client(conn,addr):
    NICK = str(nicknames[clients.index(conn)])
    print(f'{NICK} connected.')
    broadcast(NICK+' has entered the chat')
    while True: # connected = True
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg==DISCONNECT:
                broadcast(NICK +': '+msg)
                break # connected=False
            broadcast(NICK +': '+msg)
            print(f'[{addr}] {msg}')    
    conn.close()
    indexTopop = clients.index(conn)
    clients.pop(indexTopop)
    nicknames.pop(indexTopop)
    broadcast(NICK+' has left the chat')
    print(f'Disconnected: {addr}')
    
#start server and receive new connection
def start():
    server.listen()
    print(f'Listening on {IP}..')
    while True:
        client, addr = server.accept()
        print(f'Connected with {str(addr)} ..')
        client.send('Enter your nickname: '.encode(FORMAT))
        nickname=client.recv(1024).decode(FORMAT)
        
        clients.append(client)
        nicknames.append(nickname)
        
        print(f'{addr} has nickname {nickname}')
        thread = threading.Thread(target=handle_client, args=(client, addr) )
        thread.start()
        print(f'ACTIVE CONNECTIONS : {len(clients)}')


print('Server is starting..')
start()                         