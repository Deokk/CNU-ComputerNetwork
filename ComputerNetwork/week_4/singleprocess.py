import time
import os
import socket

def send_recv(client_socket):
    data = client_socket.recv(1024)
    print("client {}] {}".format(os.getpid(), data.decode()))
    response = "HTTP/1.1 200 OK\r\n"
    client_socket.send(response.encode('utf-8'))
    client_socket.send(data)
    client_socket.close()

def main(port):
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind(('', port))
    serversocket.listen()

    while True:
        (clientsocket, address) = serversocket.accept()
        send_recv(clientsocket)

if __name__ == "__main__":
    port = 8888
    main(port)

