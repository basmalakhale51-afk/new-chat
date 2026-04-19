import os
import socket
import threading


clients = []

def broadcast(msg, sender):
    for client in clients:
        if client != sender:
            try:
                client.send(msg)
            except:
                clients.remove(client)

def handle_client(client):
    while True:
        try:
            msg = client.recv(1024)
            broadcast(msg, client)
        except:
            clients.remove(client)
            client.close()
            break

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
PORT = int(os.environ.get("PORT", 8080))
server.bind(("0.0.0.0", PORT))
server.listen()

print("Server is running...")

while True:
    client, addr = server.accept()
    print("Client connected:", addr)
    clients.append(client)

    thread = threading.Thread(target=handle_client, args=(client,))
    thread.start()
