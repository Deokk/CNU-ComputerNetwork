import sys
import os
import socket

# 인자값을 확인하고 반환해주는 함수
def check_arg():
    # 배열의 크기가 2일 때 입력받은 port 를 반환합니다.
    if len(sys.argv) == 2:
        return sys.argv[1]
    # 배열의 크기가 2가 아니라면 sys.exit() 을 사용합니다.
    else:
        print("sys exit")
        sys.exit()

# 파일을 송신하는 함수입니다.
def sender_send(f_name, addr):
    # receive 명령어를 잘 받았다는 메시지를 보냅니다.
    server_socket.sendto("valid list command".encode(), addr)
    # 파일이 존재한다면 송신을 수행합니다.
    if os.path.isfile(f_name):
        # 파일이 존재함을 알리는 메시지를 만들고 송신합니다.
        is_exist_msg = f_name + " file exists!"
        print(is_exist_msg)
        server_socket.sendto(is_exist_msg.encode(), addr)
        # 파일 크기를 계산하고 출력합니다.
        file_size = os.stat(f_name).st_size
        num = int(file_size / 4096) + 1
        file_size_msg = "file_size : " + str(num)
        print(file_size_msg)
        # 계산한 파일 크기를 receiver 에게 송신합니다.
        server_socket.sendto(file_size_msg.encode(), addr)
        server_socket.sendto(str(num).encode(), addr)
        # 파일을 open 함수를 통해 읽습니다.
        read_file = open(f_name, 'rb')
        check = num
        # 반복문을 통해 계산한 파일 크기만큼 송신해줍니다.
        while check != 0:
            chunk_file = read_file.read(4096)
            server_socket.sendto(chunk_file, addr)
            packet_msg = "packet number " + str(num - check + 1)
            print(packet_msg)
            check -= 1
        read_file.close()
        print("send complete")
    # 파일이 존재하지 않는다면 메시지를 만들어 출력합니다.
    else:
        is_empty_message = f_name + " can't find!"
        print(is_empty_message)

if __name__ == '__main__':
    # port 번호를 받아옵니다.
    port = check_arg()

    # socket & bind 를 통한 소켓 생성 및 자료 수신 준비
    print("It was successfully entered. Let's move on!")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print("Server socket created.")
    server_socket.bind(('', int(port)))
    print("Successful binding. waiting for client now.")

    # 무한 루프를 통해 자료 송신을 반복합니다.
    while True:
        # receiver 로부터 받은 명령어와 파일명을 받아 저정합니다.
        msg, addr = server_socket.recvfrom(2000)
        msg = msg.decode().split()
        # 명령어가 receive 라면 파일을 sender_send 를 통해 송신합니다.
        if msg[0] == 'receive':
            file_name = msg[1]
            sender_send(file_name, addr)
        # 명령어가 receive 가 아니라면 socket 을 종료하고
        # sys.exit() 함수를 사용합니다.
        else:
            print("Command is not correct.")
            print("socket close")
            socket.close()
            print("sys exit")
            sys.exit()