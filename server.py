import sys
import socket
from datetime import datetime



def main():
    port = sys.argv[1]
    ip_parent = sys.argv[2]
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
    data = "fuc34534545fuckingfuckingfuck"
    if data in ips_dict:
        desired_ip = ips_dict[data][0]
        desired_ttl = ips_dict[data][1]
        ips_dict[data][2] = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        i = is_this_entry_relevant(desired_ttl, ips_dict[data][2])
    ips_dict[data] = "yael", "linoy"
    update_file(ips_file, ips_dict)
    n=1
    """

    while True:
        flag = 0
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
            if is_this_entry_relevant(desired_ttl, ips_dict[data][2]):
                # check if encode is neede*****
                client_socket.sendto(desired_ip.encode,addr)
            else:
                # chaeck if need to delete********
                flag = 1
        else:
            flag = 1

        if flag == 1:  # need to communicate with parent server tp get the entry
            parent_socket.sendto(data.encode(), (ip_parent, parent_port))
            parent_data, parent_add = parent_socket.recvfrom(1024)  # receive answer from parent
            parent_data = parent_data.decode()
            # add to dictionary
            first_add, second_add = parent_data.split(',')
            third_add = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            ips_dict[data] = first_add, second_add, third_add
            reply = ips_dict[data][0]
            client_socket.sendto(reply.encode, addr)



def is_this_entry_relevant(ttl, remaining_time):
    remaining_time = datetime.strptime(remaining_time, '%Y-%m-%d %H:%M:%S.%f')  # convert str to datetime.
    result = (datetime.now() - remaining_time).total_seconds()
    return result < float(ttl)

def update_file(file_name, dict):
    with open(file_name, 'w') as file:
        file.truncate()  # delete all file content.
        for name in dict:
            ip_address = dict[name][0]
            ttl = dict[name][1]
            str = name + "," + ip_address + "," + ttl + "\n"
            file.write(str)


if __name__ == "__main__":
    main()
