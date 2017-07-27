#_*_ coding: utf-8 _*_
import socket
import sys
import subprocess,traceback
import re
from thread import *
import time

HOST = ''
PORT = 40217
#create socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print ('Socket created')

#bind socket
try:
    s.bind((HOST, PORT))
except socket.error , msg:
    print ('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1] + "   " + __file__ + "  " + sys.getframe().f_lineno)
    sys.exit()
print ('Socket bind complete')

#listen socket
s.listen(10)
print ("Socket now is listening")


#white_list = "ls -l;ll;pwd;cd ~/p2p/;cd /home/xiaoyong/p2p/;sh deploy.sh;cat deploy.sh;sh restart_p2p_service.sh;ps aux|grep kw-live;cat restart_p2p_service.sh;sh test.sh"
whiteListInput = open('whitelistConfig','r')
whitelist = []

for line in  whiteListInput:
    whitelist.append(line)

white_list = "".join(whitelist)

#define thread for handleing conn
def clientthread(conn):
#    conn.send("welcome connect to server.Type something and hit enter!\n")

    while True:
        data = conn.recv(4096)
        #客户端传过来的数据为空
        if not data:
            conn.sendall("command is empty,do nothing!")
            continue
        #防止端口被利用来进行破坏活动
        patt = r'\b%s\b'% str(data).strip()
        match_result = re.findall(patt,white_list)
#        if str(data).strip() in "pwd*ls -l*cd /home/xiaoyong/p2p/*sh deploy.sh*sh restart_p2p_service.sh":
        if match_result:
            #conn.sendall(replay)
            print (conn.getpeername()[0] + " : " + str(data))
            #用subprocess.Popen()方法另起子线程执行shell程序,并将标准输出保存到stdout,标准错误输出到stderr
            handler = subprocess.Popen([str(data).strip()], shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)

            output = handler.stdout.readlines()
            errinfo = handler.stderr.readlines()

            if output is None:
                conn.sendall("command execute successfully and has no result return.")
            else:
                for one_line in output:
                    print (one_line)
                    conn.sendall(one_line)
            if errinfo is None:
                conn.sendall("command execute successfully and no error occurred.")
            else:
                for one_line in errinfo:
                    print (one_line)
                    conn.sendall(one_line)

            print ("command " + data + " is completed.")

        else:
            conn.sendall("command is not allowed to execute!")
            uselessWord = " " * (4096 - 5)
            conn.send(uselessWord + "Done")
            continue

        time.sleep(2)
        uselessWord = " "*(4096-5)
        conn.send(uselessWord+"Done")

    conn.close()


#wait to accept a connection
while 1:
    try:
        conn, addr = s.accept()
        conn.sendall("***************Support command are:***********\n* 1.ls -l;ll                                 *\n* 2.pwd;ps aux|grep kw-live                  *\n* 3.cd ~/p2p/;cd /home/xiaoyong/p2p/         *\n* 4.sh deploy.sh;sh restart_p2p_service.sh   *\n* 5.cat deploy.sh;cat restart_p2p_service.sh *\n**********************************************\n")
    except Exception,e:
        traceback.print_exc()
        continue
    print ('Connected with ' + addr[0] + ':' + str(addr[1]))

    #receive data from client and replay to client

    try:
        start_new_thread(clientthread,(conn,))
    except Exception,e:
        traceback.print_exc()
        continue

s.close()
