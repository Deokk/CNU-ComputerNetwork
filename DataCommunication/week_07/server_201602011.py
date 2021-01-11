import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('', 7070))

while True:
    data, addr = server_socket.recvfrom(2000)
    print(addr, data.decode())

    message = input(">>> ")
    server_socket.sendto(message.encode(), addr)
