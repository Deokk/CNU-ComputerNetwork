from multiprocessing import Process
import socket
import os

def send_recv(client, address):
    data = client.recv(1024)
    print("client {}] {}".format(os.getpid(), data.decode()))
    response = "HTTP/1.1 200 OK\r\n"
    client.send(response.encode('utf-8'))
    client.close()

def main(port):
    proc = None
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind(('', port))
    serversocket.listen(5)
    clients = list()
    try:
        while True:
            # accept()
            client, address = serversocket.accept()
            # print(“accept client from”, address)
            print("accept client from", address)
            # clients list에 client 넣기
            # clients.append(client)
            # 멀티 프로세스 실행
            proc = Process(target=send_recv, args=(client, address))
            proc.start()
            # 1 ~ 4를 반복

    except Exception:
        proc.join()

if __name__ == "__main__":
    port = 8888
    main(port)

