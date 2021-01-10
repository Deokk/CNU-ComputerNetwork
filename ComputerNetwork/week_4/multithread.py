from threading import Thread
import socket
import os

def send_recv(client, address):
    data = client.recv(1024)
    print("client {}] {}".format(os.getpid(), data.decode()))
    response = "HTTP/1.1 200 OK\r\n"
    client.send(response.encode('utf-8'))
    client.close()


def main(port):
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind(('', port))
    th = None
    serversocket.listen(5)
    clients = list()

    try:
        while True:
            # accept()
            client, address = serversocket.accept()
            # print(“accept client from”, address)
            print("accept client from", address)
            # 멀티 쓰레드 실행
            th = Thread(target=send_recv, args=(client, address))
            th.start()
            # 1 ~ 3을 반복

    except Exception:
        th.join()

if __name__ == "__main__":
    port = 8888
    main(port)

