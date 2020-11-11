import sys
import socket
from datetime import datetime



def main():
    port = sys.argv[1]
    ip_parent_address = sys.argv[2]
    parent_port = sys.argv[3]
    ips_file = sys.argv[4]
    parent_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # connecting to parent server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # connecting to client (to me)
    client_socket.bind(('', int(port)))

    ips_list = []
    file = open(ips_file)
    for lines in file:
        lines = lines.strip("\n")
        lines = lines.split(",")
        # the time - alive remaining from the ttl.
        lines.append(datetime(1, 1, 1, 1, 1, 1))  # initial time.
        ips_list.append(lines)

    ips_dict = {x[0]: x[1:] for x in ips_list}  # convert the list of lists to dictionary

    """
    data = "mail.biu.ac.il"
    if data in ips_dict:
        desired_ip = ips_dict[data][0]
        desired_ttl = ips_dict[data][1]
        ips_dict[data][2] = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        i = is_this_entry_relevant(desired_ttl, ips_dict[data][2])
        n=1
    """

    while True:
        data, addr = client_socket.recvfrom(1024)
        data = data.decode()  # check if needed.
        # is_in_list = any(data in sublist for sublist in ips_list)
        # if true -> return its ip address. o.w- ask the parent for it
        # todo check what to do with TTL later. **************************

        if data in ips_dict:
            desired_ip = ips_dict[data][0]
            desired_ttl = ips_dict[data][1]
            ips_dict[data][2] = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            # if the ttl not finished then we can sent the entry to the client, o.w we need to ask parent
            if  is_this_entry_relevant(desired_ttl, ips_dict[data][2]):
                # check if encode is neede*****
                client_socket.sendto(desired_ip.encode,addr)


        else:
            r = 1



def is_this_entry_relevant(ttl, remaining_time):
    remaining_time = datetime.strptime(remaining_time, '%Y-%m-%d %H:%M:%S.%f')  # convert str to datetime.
    result = (datetime.now() - remaining_time).total_seconds()
    return result < float(ttl)

if __name__ == "__main__":
    main()
