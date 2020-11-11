import sys
import socket

def main():
    port = sys.argv[1]
    ip_address = sys.argv[2]
    parent_port = sys.argv[3]
    ips_file = sys.argv[4]
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP server.
    ips_list = []
    file = open(ips_file)
    for lines in file:
        lines = lines.strip("\n")
        ips_list.append(lines.split(","))
    n=1







if __name__ == "__main__":
    main()