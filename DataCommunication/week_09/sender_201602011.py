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
        # print((hex(ord(data_array[i][0]))), (hex(ord(data_array[i][1]))))               # (a)과정을 거치기 전 data 출력문
        # ord 함수를 이용해 아스키코드로 변환하고 hex 함수를 이용해 16진수로 변환한 뒤에
        # 두 데이터가 str 타입이므로 연결하여 저장합니다. (4바이트)
        sliced_data = (hex(ord(data_array[i][0]))) + (hex(ord(data_array[i][1])))[2:]
        # print('(a) result :', sliced_data)                                              # (a)과정을 거친 후 data 출력문
        # 기존 checksum 에 (a)과정을 거친 데이터를 int 형으로 변환한 후에 더해줍니다.
        checksum += int(sliced_data, 0)
        # print('(b) result :', hex(checksum))                                            # (b)과정을 거친 후 data 출력문
        # (c)의 과정을 % 연산을 이용해 도출이 가능합니다.
        checksum %= 0xFFFF
        # print('(c) result :', hex(checksum))                                            # (c)과정을 거친 후 data 출력문
    # print('before (e) : ', bin(checksum))                                               # (e)과정을 거치기 전 data 출력문
    # checksum 의 비트 반전을 하는 연산으로 XOR 연산을 이용해 반전시킵니다.
    checksum ^= 0xFFFF
    # print('after (e) : ', bin(checksum))                                                # (e)과정을 거친 후 data 출력문
    # 16진수로 변환한 후에 앞의 '0x'를 잘라준 후 반환합니다.
    return (hex(checksum)[2:]).rjust(4, '0')

# header 를 만들어주는 함수입니다.
def make_header(Data, size):
    Src_Address = 'ac1e0116'            # 172.30.1.22
    Dst_Address = 'c0a83801'            # 192.168.56.1
    Zeros = '00'                        # 00
    Protocol = '17'                     # UDP 프로토콜
    length = str(hex((size + 8)))[2:]   # 인자로 받은 읽어온 데이터의 크기에 헤더 8을 더한 값을 저장합니다.
    UDP_Length = length.rjust(4, '0')   # rjust() 함수를 이용해서 앞을 0으로 채워 4바이트로 만들어줍니다.
    Src_Port = '1f40'                   # 8000번 포트를 사용합니다.
    Dst_Port = '1f40'                   # 8000번 포트를 사용합니다.
    Length = UDP_Length                 # UDP Length 와 동일합니다.
    init_checksum = '0000'              # 초기 checksum 을 0000으로 설정합니다.
    # data 를 str 형태로 합쳐줍니다.
    data = Src_Address + Dst_Address + Zeros + Protocol + UDP_Length + Src_Port + Dst_Port + Length + init_checksum + Data
    # 생성한 data 를 바탕으로 정의한 함수를 이용해 checksum 을 계산해줍니다.
    checksum = calc_checksum(data)
    # 계산한 checksum 을 출력합니다.
    print('checksum:', checksum)
    # 계산한 checksum 으로 빈 checksum 의 자리를 채워줍니다.
    data = Src_Address + Dst_Address + Zeros + Protocol + UDP_Length + Src_Port + Dst_Port + Length + checksum + Data
    # 생성한 data 를 반환합니다.
    return data

# 파일을 송신하는 함수입니다.
def sender_send(f_name, addr):
    # receive 명령어를 잘 받았다는 메시지를 보냅니다.
    server_socket.sendto("received receive command".encode(), addr)
    # 파일이 존재한다면 송신을 수행합니다.
    if os.path.isfile(f_name):
        # 파일이 존재함을 알리는 메시지를 만들고 송신합니다.
        is_exist_msg = f_name + " file exists!"
        print(is_exist_msg)
        server_socket.sendto(is_exist_msg.encode(), addr)
        # 파일 크기를 계산하고 출력합니다.
        file_size = os.stat(f_name).st_size
        num = int(file_size / (1024 - 40)) + 1
        file_size_msg = "file_size : " + str(file_size)
        print(file_size_msg)
        # 계산한 파일 크기를 receiver 에게 송신합니다.
        server_socket.sendto(file_size_msg.encode(), addr)
        server_socket.sendto(str(num).encode(), addr)
        # 파일을 open 함수를 통해 읽습니다.
        read_file = open(f_name, 'rb')
        check = num
        # 반복문을 통해 계산한 파일 크기만큼 송신해줍니다.
        while check != 0:
            # header 의 길이 40을 1024에서 뺀 만큼 file 을 읽어줍니다.
            chunk_file = read_file.read(1024 - 40)
            # 읽어준 chunk_file 을 utf-8 로 decode 한 다음
            # make_header 함수를 이용해 header 를 만들어줍니다.
            data = make_header(chunk_file.decode('utf-8'), len(chunk_file))
            # 만들어 준 데이터를 socket 을 이용해 송신합니다.
            # 이때 utf-8 로 인코딩하여 송신해줍니다.
            server_socket.sendto(data.encode('utf-8'), addr)
            # 몇 번째 packet 인지를 출력해줍니다.
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
        # receiver 로부터 받은 명령어와 파일명을 받아 저장합니다.
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
