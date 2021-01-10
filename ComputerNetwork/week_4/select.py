import select
import socket
import os

def main(port):
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind(('', port))
    serversocket.listen(5)

    while True:
        input_ready, write_ready, except_ready = select.select([serversocket], [], [])
        for socket_val in input_ready:
            if socket_val == serversocket:
                client, address = serversocket.accept()
                input_ready.append(client)
                print("accept client from", address)
            else:
                data = socket_val.recv(1024)
                if data:
                    msg = "HTTP/1.1 200 OK\r\n"
                    socket_val.send(msg.encode('utf-8'))
                else:
                    socket_val.close()
                    input_ready.remove(socket_val)

if __name__ == "__main__":
    port = 8888
    main(port)


