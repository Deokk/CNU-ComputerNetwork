import sys
import socket
import time

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
        # ord 함수를 이용해 아스키코드로 변환하고 hex 함수를 이용해 16진수로 변환한 뒤에
        # 두 데이터가 str 타입이므로 연결하여 저장합니다. (4바이트)
        sliced_data = (hex(ord(data_array[i][0]))) + (hex(ord(data_array[i][1])))[2:]
        checksum += int(sliced_data, 0)
        checksum %= 0xFFFF
    # checksum 의 비트 반전을 하는 연산으로 XOR 연산을 이용해 반전시킵니다.
    checksum ^= 0xFFFF
    # 16진수로 변환한 후에 앞의 '0x'를 잘라준 후 반환합니다.
    return (hex(checksum)[2:]).rjust(4, '0')

def separate_header(data):
    # Frame 을 data 에서 잘라줍니다.
    frame = data[:1]
    # header 를 data 에서 잘라줍니다.
    header = data[1:37]
    # checksum 을 data 에서 잘라줍니다.
    send_checksum = data[37:41]
    # txt 파일의 정보를 data 에서 잘라줍니다.
    result_data = data[41:]
    # 위 3개의 변수를 반환합니다.
    return frame, header, result_data, send_checksum

# ack 와 frame 의 비교를 통해 오류가 발생하는지 확인합니다.
# 다를 때 에러가 발생하도록 코드를 작성했습니다.
def is_error(frame, ack):
    return frame != ack

# ack 가 0이면 1로, 1이면 0으로 바꿔주는 함수입니다.
def reverse_ack(ack):
    if ack == '0':
        return '1'
    elif ack == '1':
        return '0'

if __name__ == '__main__':
    # ip 주소와 port 번호를 받아옵니다.
    ip_addr, port = check_arg()
    print("It was successfully entered. Let's move on!")
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
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
            print('')
            num, addr = client_socket.recvfrom(2000)
            # packet number 를 출력할 때 1부터 출력하기 위해
            # 변수를 알맞게 변경합니다.
            num = int(num.decode()) + 1
            check = num
            # 파일명을 통해 open 함수 쓰기모드를 이용합니다.
            write_file = open(command_list[1], 'wb')
            # 초기 ack 를 0으로 설정합니다.
            ack = '0'
            # 오류가 발생할 경우 이전 패킷을 다시 보내기 위해
            # 패킷을 저장하는 변수입니다.
            full_data = ''
            # 반복문을 통해 파일의 크기만큼 파일을 수신합니다.
            while check != 1:
                # sender 로부터 packet 을 받아옵니다.
                chunk_file, addr = client_socket.recvfrom(1024)
                # 받아온 packet 을 정의한 separate_header 함수를 통해
                # frame, header 와 txt 파일 정보와 checksum 을 분리합니다.
                frame, header, result_data, send_checksum = separate_header(chunk_file.decode())
                # 전달받은 frame 정보를 출력합니다.
                print('Received frame number :', frame)
                # ack 로 sender 가 전달받지 못했음을 확인했을 때
                # 예외처리를 해주는 조건문입니다.
                if is_error(frame, ack):
                    print('\n=======================================================')
                    print('received prev frame number :', frame)
                    print('Maybe sender not received my send packet')
                    print('resend previous ack number')
                    print('=======================================================\n')
                    # 이전 패킷을 다시 보내주고 continue 합니다.
                    client_socket.sendto(full_data.encode('utf-8'), addr)
                    print('send ack number : ', ack)
                    print('')
                    continue

                # ack 를 반전시켜줍니다.
                ack = reverse_ack(ack)
                # header 와 txt 파일 정보를 통해 새 checksum 을 계산하기 위한
                # data 를 만들어줍니다. ('0000'은 checksum 의 자리입니다.)
                # temp_data : checksum 을 계산하기 위해 frame 을 저장합니다.
                temp_data = frame + header + '0000' + result_data
                # sender 의 checksum 을 명시적으로 볼 수 있도록 출력합니다.
                print('        Received checksum :', send_checksum)
                # 정의한 calc_checksum 함수를 이용해 새로운 checksum 을 계산합니다.
                receive_checksum = calc_checksum(temp_data)
                # receiver 의 checksum 을 명시적으로 볼 수 있도록 출력합니다.
                print('        New calculated checksum :', receive_checksum)

                # checksum 이 일치하지 않는다면 socket 을 닫고
                # 출력문을 출력한 후 sys.exit() 을 사용합니다.
                if send_checksum != receive_checksum:
                    socket.close()
                    print('checksum error!')
                    sys.exit()

                # full_data : 반전시킨 ack 를 이용해 정보를 만들어줍니다.
                full_data = ack + header + receive_checksum + result_data
                # txt 파일의 정보를 써줍니다.
                data = chunk_file[41:]
                write_file.write(data)
                # 몇번째 packet 인자를 출력해줍니다.
                packet_msg = "        Received packet number : " + str(num - check + 1)
                print(packet_msg)

                ##################### 예외처리 1번을 위한 코드 #####################
                # 처음 한 번에 한해서 9.0초(7.0 + 2)동안 sleep 합니다.
                # if check == num:
                #     time.sleep(9.0)
                #     check -= 1
                #     continue

                ##################### 예외처리 2번을 위한 코드 #####################
                # 처음 한 번에 한해서 자기자신에게 보내줘 송신 중 유실되도록 설정합니다.
                # if check == num:
                #     addr = ('localhost', int(port))

                # ack 와 함께 full_data 를 sender 에 송신합니다.
                client_socket.sendto(full_data.encode('utf-8'), addr)
                # 송신한 ack 를 명시적으로 출력합니다.
                print('send ack number : ', ack)
                print('')
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
