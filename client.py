import sys
import socket


def main():
    run = True
    server_ip = sys.argv[1]
    server_port = sys.argv[2]
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while run:
        massage = input().encode()
        server_socket.sendto(massage, (server_ip, int(server_port)))  # send massage to server
        data, addr = server_socket.recvfrom(1024)  # receive answer from server
        data = data.decode()
        ip, ttl = data.split(',')
        print(ip)
    server_socket.close()


if __name__ == "__main__":
    main()