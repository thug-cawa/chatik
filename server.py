import socket
import threading
from network import *

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
clients = []
nicknames = []


def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            print(f'{nicknames[clients.index(client)]}')
            broadcast(message)
        except:
            index=clients.index(client)
            clients.remove(client)
            client.close()
            nickname=nicknames[index]
            nicknames.remove(nickname)
            break



def receive():
    while True:
        client, address = server.accept()
        print(f'Connected  {address}')

        client.send("Name".encode('utf-8'))
        nickname=client.recv(1024)

        nicknames.append(nickname)
        clients.append(client)
        print(f'nickname {nickname}')
        broadcast(f'Connected with nickname {nickname}'.encode('utf-8'))
        client.send("\n".encode('utf-8'))
        thread = threading.Thread(target=handle,args=(client,))
        thread.start()
print("server running")
receive()