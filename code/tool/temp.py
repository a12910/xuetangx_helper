
import socket
import os
import threading
import time

def ping_ip(ip):  # 3、ping指定IP判断主机是否存活
    outputs = os.popen('ping -%s 1 %s' % ('c', ip)).readlines()
    for key in outputs:
        if str(key).upper().find('TTL') >= 0:
            print(ip, 'ok')

def ping_all(ip):  # 4、ping所有IP获取所有存活主机
    pre_ip = (ip.split('.')[:-1])
    for i in range(1, 256):
        add = ('.'.join(pre_ip) + '.' + str(i))
        threading._start_new_thread(ping_ip, (add,))
        time.sleep(0.1)

if __name__ == '__main__':
    ping_all(socket.gethostbyname(socket.gethostname()))