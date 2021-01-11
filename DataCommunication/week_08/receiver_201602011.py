import sys
import socket

# 인자값을 확인하고 반환해주는 함수
def check_arg():
    # 배열의 크기가 3일 때 입력받은 ip주소와 port 를 반환합니다.
    if len(sys.argv) == 3:
        return sys.argv[1], sys.argv[2]
    # 배열의 크기가 3이 아니라면 sys.exit() 을 사용합니다.
    else:
        print("sys exit")
        sys.exit()

if __name__ == '__main__':
    # ip 주소와 port 번호를 받아옵니다.
    ip_addr, port = check_arg()
    print("It was successfully entered. Let's move on!")
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # non-blocking 으로 설정합니다.
    client_socket.setblocking(False)
    # timeout 을 15로 설정합니다.
    client_socket.settimeout(15.0)
    print("receiver socket created.")

    # 무한 루프를 통해 자료 수신을 반복합니다.
    while True:
        command = input("enter a command: \n1. receive \n2. exit\n")
        # 명령어를 나누어줍니다.
        command_list = command.split()
        # 명령어가 exit 이라면 socket을 종료하고
        # sys.exit 함수를 사용합니다.
        if command_list[0] == 'exit':
            print("socket close")
            socket.close()
            print("sys exit")
            sys.exit()
        # 명령어가 receive 라면 자료를 수신을 준비합니다.
        if command_list[0] == 'receive':
            # 명령어를 sender 에게 송신합니다.
            client_socket.sendto(command.encode(), (ip_addr, int(port)))
            # 명령어가 유효한지에 대한 답변을 수신하고 출력합니다.
            is_valid, addr = client_socket.recvfrom(2000)
            print(is_valid.decode())
            # 파일이 존재하는지에 대한 답변을 수산히고 출력합니다.
            is_exist, addr = client_socket.recvfrom(2000)
            print(is_exist.decode())
            # 파일의 크기를 수신하고 출력합니다.
            file_size, addr = client_socket.recvfrom(2000)
            print(file_size.decode())
            num, addr = client_socket.recvfrom(2000)
            # packet number를 출력할 때 1부터 출력하기 위해
            # 변수를 알맞게 변경합니다.
            num = int(num.decode()) + 1
            check = num
            # 파일명을 통해 open 함수 쓰기모드를 이용합니다.
            write_file = open(command_list[1], 'wb')
            # 반복문을 통해 파일의 크기만큼 파일을 수신합니다.
            while check != 1:
                chunk_file, addr = client_socket.recvfrom(4096)
                write_file.write(chunk_file)
                packet_msg = "packet number " + str(num - check + 1)
                print(packet_msg)
                check -= 1
            write_file.close()
            print("receive complete")
        # 명령어가 exit 도 아니고 receive 도 아니라면
        # socket 을 종료하고 sys.exit()을 사용합니다.
        else:
            print("Command is not correct.")
            print("socket close")
            socket.close()
            print("sys exit")
            sys.exit()
