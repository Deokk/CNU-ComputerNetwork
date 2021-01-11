# 필요한 모듈 import
import socket
import random

# multiply와 add에 따른 숫자를 계산하는 함수
def instruction(num, inst):
    i = random.randint(-1, 4)
    if inst == 'multiply':
        return num * i
    elif inst == 'add':
        return num + i

TCP_IP = '10.0.2.15'
TCP_PORT = 5001

# 3개의 client를 허용한다.
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((TCP_IP, TCP_PORT))
sock.listen(3)

# client의 정보를 출력
conn1, addr1 = sock.accept()
print('Connection address 1 : ' + str(addr1))

conn2, addr2 = sock.accept()
print('Connection address 2 : ' + str(addr2))

conn3, addr3 = sock.accept()
print('Connection address 3 : ' + str(addr3))

# 3개의 클라이언트가 접속하면 준비가 되었다는 메시지를 클라이언트에 전송
message = "Okay... All players have gathered. Start the game.\n"

conn1.send(message.encode())
conn2.send(message.encode())
conn3.send(message.encode())

while True:

    # 1~100의 난수를 10개 만들에 리스트에 저장
    number = [random.randint(1, 100) for i in range(10)]

    # 클라이언트로부터 숫자를 입력받기 위한 안내 메시지 생성
    message = "Please select 1 number from 1 to 10."
    
    # 클라이언트로부터 준비되었다는 것을 recv를 통해 확인
    conn1.recv(1024)
    # 이전에 생성한 메시지 전송
    conn1.send(message.encode())
    # 클라이언트로부터 숫자를 수신
    num1 = conn1.recv(1024)
    # 만들어준 난수를 리스트에서 가져와 클라이언트로 전송
    num1 = number[int(num1.decode()) - 1]
    conn1.send(str(num1).encode())

    # 클라이언트로부터 준비되었다는 것을 recv를 통해 확인
    conn2.recv(1024)
    # 이전에 생성한 메시지 전송
    conn2.send(message.encode())
    # 클라이언트로부터 숫자를 수신
    num2 = conn2.recv(1024)
    # 만들어준 난수를 리스트에서 가져와 클라이언트로 전송
    num2 = number[int(num2.decode()) - 1]
    conn2.send(str(num2).encode())

    # 클라이언트로부터 준비되었다는 것을 recv를 통해 확인
    conn3.recv(1024)
    # 이전에 생성한 메시지 전송
    conn3.send(message.encode())
    # 클라이언트로부터 숫자를 수신
    num3 = conn3.recv(1024)
    # 만들어준 난수를 리스트에서 가져와 클라이언트로 전송
    num3 = number[int(num3.decode()) - 1]
    conn3.send(str(num3).encode())

    # 클라이언트로부터 연산을 입력받기 위한 안내 메시지 생성
    message = "Do you want multiply or add...?"

    # 안내메시지를 송신하고 연산을 클라이언트로부터 수신
    conn1.send(message.encode())
    instruction1 = conn1.recv(1024).decode()
    # instruction 함수를 이용해 연산값 저장
    result1 = instruction(num1, instruction1)

    # 안내메시지를 송신하고 연산을 클라이언트로부터 수신
    conn2.send(message.encode())
    instruction2 = conn2.recv(1024).decode()
    # instruction 함수를 이용해 연산값 저장
    result2 = instruction(num2, instruction2)

    # 안내메시지를 송신하고 연산을 클라이언트로부터 수신
    conn3.send(message.encode())
    instruction3 = conn3.recv(1024).decode()
    # instruction 함수를 이용해 연산값 저장
    result3 = instruction(num3, instruction3)

    # 조건을 설정하고 알맞는 메시지를 송신
    if result1 > result2:
        if result1 > result3:
            conn1.send('Congratulations. Wou won!'.encode())
            conn2.send('Unfortunately, you have been defeated.'.encode())
            conn3.send('Unfortunately, you have been defeated.'.encode())
        else:
            conn3.send('Congratulations. Wou won!'.encode())
            conn1.send('Unfortunately, you have been defeated.'.encode())
            conn2.send('Unfortunately, you have been defeated.'.encode())
    else:
        if result2 > result3:
            conn2.send('Congratulations. Wou won!'.encode())
            conn1.send('Unfortunately, you have been defeated.'.encode())
            conn3.send('Unfortunately, you have been defeated.'.encode())
        else:
            conn3.send('Congratulations. Wou won!'.encode())
            conn1.send('Unfortunately, you have been defeated.'.encode())
            conn2.send('Unfortunately, you have been defeated.'.encode())

conn1.close()
conn2.close()
conn3.close()

