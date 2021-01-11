import socket

ip_addr = input("ip address : ")
port = input("port : ")

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


while True:
    message = input(">>> ")
    client_socket.sendto(message.encode(), (ip_addr, int(port)))

    data, addr = client_socket.recvfrom(2000)
    print(addr, data.decode())