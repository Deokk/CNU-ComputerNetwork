import sys
import socket

# 인자값을 확인하고 반환해주는 함수
def check_arg():
    # 배열의 크기가 3일 때 입력받은 ip 주소와 port 를 반환합니다.
    if len(sys.argv) == 3:
        return sys.argv[1], sys.argv[2]
    # 배열의 크기가 3이 아니라면 sys.exit() 을 사용합니다.
    else:
        print("sys exit")
        sys.exit()

# data 를 인자로 받아 checksum 을 계산해줍니다.
def calc_checksum(data):
    # 2바이트씩 나누기 위한 변수 s 와 e 를 0과 2 로 초기화합니다.
    s = 0
    e = 2
    # 2바이트씩 쪼갠 정보를 저장할 빈 리스트를 만들어줍니다.
    data_array = []
    # data 의 길이를 2로 나눈 값만큼 반복합니다.
    # data 를 s와 e를 이용해 자르고 data_array 에 추가해줍니다.
    for i in range(int(len(data) / 2)):
        data_array.append(data[s:e])
        s += 2
        e += 2
    # 처음 checksum 을 0으로 초기화합니다.
    checksum = 0x0
    # data array 의 길이만큼 반복해줍니다.
    # checksum 을 반복하여 계산하기 위한 반복문입니다.
    for i in range(len(data_array)):
        print((hex(ord(data_array[i][0]))), (hex(ord(data_array[i][1]))))               # (a)과정을 거치기 전 data 출력문
        # ord 함수를 이용해 아스키코드로 변환하고 hex 함수를 이용해 16진수로 변환한 뒤에
        # 두 데이터가 str 타입이므로 연결하여 저장합니다. (4바이트)
        sliced_data = (hex(ord(data_array[i][0]))) + (hex(ord(data_array[i][1])))[2:]
        print('(a) result :', sliced_data)                                              # (a)과정을 거친 후 data 출력문
        # 기존 checksum 에 (a)과정을 거친 데이터를 int 형으로 변환한 후에 더해줍니다.
        checksum += int(sliced_data, 0)
        print('(b) result :', hex(checksum))                                            # (b)과정을 거친 후 data 출력문
        # (c)의 과정을 % 연산을 이용해 도출이 가능합니다.
        checksum %= 0xFFFF
        print('(c) result :', hex(checksum))                                            # (c)과정을 거친 후 data 출력문
    print('before (e) : ', bin(checksum))                                               # (e)과정을 거치기 전 data 출력문
    # checksum 의 비트 반전을 하는 연산으로 XOR 연산을 이용해 반전시킵니다.
    checksum ^= 0xFFFF
    print('after (e) : ', bin(checksum))                                                # (e)과정을 거친 후 data 출력문
    # 16진수로 변환한 후에 앞의 '0x'를 잘라준 후 반환합니다.
    return (hex(checksum)[2:]).rjust(4, '0')

def separate_header(data):
    # header 를 data 에서 잘라줍니다.
    header = data[:36]
    # checksum 을 data 에서 잘라줍니다.
    send_checksum = data[36:40]
    # txt 파일의 정보를 data 에서 잘라줍니다.
    result_data = data[40:]
    # 위 3개의 변수를 반환합니다.
    return header, result_data, send_checksum

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
        # 명령어가 exit 이라면 socket 을 종료하고
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
            # 파일이 존재하는지에 대한 답변을 수신하고 출력합니다.
            is_exist, addr = client_socket.recvfrom(2000)
            print(is_exist.decode())
            # 파일의 크기를 수신하고 출력합니다.
            file_size, addr = client_socket.recvfrom(2000)
            print(file_size.decode())
            num, addr = client_socket.recvfrom(2000)
            # packet number 를 출력할 때 1부터 출력하기 위해
            # 변수를 알맞게 변경합니다.
            num = int(num.decode()) + 1
            check = num
            # 파일명을 통해 open 함수 쓰기모드를 이용합니다.
            write_file = open(command_list[1], 'wb')
            # 반복문을 통해 파일의 크기만큼 파일을 수신합니다.
            while check != 1:
                # sender 로부터 packet 을 받아옵니다.
                chunk_file, addr = client_socket.recvfrom(1024)
                # 받아온 packet 을 정의한 separate_header 함수를 통해
                # header 와 txt 파일 정보와 checksum 을 분리합니다.
                header, result_data, send_checksum = separate_header(chunk_file.decode())
                # header 와 txt 파일 정보를 통해 새 checksum 을 계산하기 위한
                # data 를 만들어줍니다. ('0000'은 checksum 의 자리입니다.)
                new_data = header + '0000' + result_data
                # sender 의 checksum 을 명시적으로 볼 수 있도록 출력합니다.
                print('sender checksum:', send_checksum)
                # 정의한 calc_checksum 함수를 이용해 새로운 checksum 을 계산합니다.
                receive_checksum = calc_checksum(new_data)
                # receiver 의 checksum 을 명시적으로 볼 수 있도록 출력합니다.
                print('receiver checksum:', receive_checksum)

                # checksum 이 일치하지 않는다면 socket 을 닫고
                # 출력문을 출력한 후 sys.exit() 을 사용합니다.
                if send_checksum != receive_checksum:
                    socket.close()
                    print('checksum error!')
                    sys.exit()

                # txt 파일의 정보를 써줍니다.
                data = chunk_file[40:]
                write_file.write(data)
                # 몇번째 packet 인지를 출력해줍니다.
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
