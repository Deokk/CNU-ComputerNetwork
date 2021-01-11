import socket

TCP_IP = '10.0.2.15'
TCP_PORT = 5001

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((TCP_IP, TCP_PORT))

# 서버로부터 준비되었다는 메시지 수신하고 출력
message = sock.recv(1024)
print(message.decode())

while True:
    
    # 클라이언트가 준비되었다는 메시지를 송신
    sock.send('ready'.encode())
    # 서버로부터 숫자 입력 안내 메시지 수신 및 출력
    message = sock.recv(1024)
    print(message.decode())
    # 숫자 입력
    cli_num = input('Number : ')
    # 입력한 숫자를 송신
    sock.send(cli_num.encode())
    # 서버로부터 난수 수신 및 풀력
    ser_num = sock.recv(1024)
    print("You chose the number " + ser_num.decode() + ". Please wait.")

    # 서버로부터 연산 입력 안내 메시지 수신 및 출력
    message = sock.recv(1024)
    print(message.decode())
    # 연산 입력
    instruction = input('multiply or add : ')
    # 입력한 연산 송신
    sock.send(instruction.encode())
    print("Okay... please wait.")

    # 결과 수신 및 출력
    result = sock.recv(1024)
    print(result.decode())

sock.close()

