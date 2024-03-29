import sys
import socket
from datetime import datetime


def main():
    run = True
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
        lines.append("0")  # if its 0 - from ips.txt, don't consider ttl
        ips_list.append(lines)

    ips_dict = {x[0]: x[1:] for x in ips_list}  # convert the list of lists to dictionary

    while run:
        flag = 0
        data, addr = client_socket.recvfrom(1024)
        data = data.decode()

        if data in ips_dict:
            desired_ip = ips_dict[data][0]
            desired_ttl = ips_dict[data][1]
            ip_and_ttl_reply = desired_ip + "," + desired_ttl
            # if the ttl not finished then we can sent the entry to the client, o.w we need to ask parent
            if is_this_entry_relevant(desired_ttl, ips_dict[data][2], ips_dict[data][3]):
                client_socket.sendto(ip_and_ttl_reply.encode(), addr)
                update_file(ips_file, ips_dict)
            else:
                flag = 1
        else:
            flag = 1

        if flag == 1:  # need to communicate with parent server tp get the entry
            parent_socket.sendto(data.encode(), (ip_parent, int(parent_port)))
            parent_data, parent_add = parent_socket.recvfrom(1024)  # receive answer from parent
            parent_data = parent_data.decode()
            # add to dictionary
            first_add, second_add = parent_data.split(',')  #ip and ttl accordingly.
            third_add = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            fourth_add = "1"  # because this entry come from parent
            ips_dict[data] = first_add, second_add, third_add, fourth_add
            reply = ips_dict[data][0] + "," + ips_dict[data][1]
            client_socket.sendto(reply.encode(), addr)
            update_file(ips_file, ips_dict)
    client_socket.close()
    parent_socket.close()


def is_this_entry_relevant(ttl, remaining_time, is_from_parent):
    if is_from_parent == "0":
        # that means this entry is from txt
        return True
    # else - we check the ttl
    remaining_time = datetime.strptime(remaining_time, '%Y-%m-%d %H:%M:%S.%f')  # convert str to datetime.
    result = (datetime.now() - remaining_time).total_seconds()
    return result < float(ttl)


def update_file(file_name, dic):
    with open(file_name, 'w') as file:
        file.truncate()  # delete all file content.
        for name in dic:
            ip_address = dic[name][0]
            ttl = dic[name][1]
            remaining = dic[name][2]
            parent_flag = dic[name][3]
            if not is_this_entry_relevant(ttl, remaining, parent_flag):
                continue
            str_write = name + "," + ip_address + "," + ttl + "\n"
            file.write(str_write)    
        for name in list(dic.keys()):
            ip_address = dic[name][0]
            ttl = dic[name][1]
            remaining = dic[name][2]
            parent_flag = dic[name][3]
            if not is_this_entry_relevant(ttl, remaining, parent_flag):
                del dic[name]


if __name__ == "__main__":
    main()
