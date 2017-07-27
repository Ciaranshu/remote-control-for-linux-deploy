#_*_ coding: utf-8 _*_
import socket, sys, traceback, time
from thread import *

End = "Done"
total_reply=[]

#create socket
try:
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
except socket.error, msg:
    print ('Failed to create socket, Error code: ' + str(msg[0]) + ',Error  message :' + msg[1] )
    sys.exit()

print ('Socket created successfully')

#test: connect to server
host = sys.argv[1]
port = 40217
hosts = ["127.0.0.1",]
#脚本参数提供需要执行的command
#command = sys.argv[2]

#try:
#    remote_ip =  socket.gethostbyname( host )
#except socket.gaierror:
#    print ('Hostname could not be resolved. Exiting')
#    sys.exit()
#print ('Ip address of ' + host + ' is ' + remote_ip)

def execute(host,port):
    try:
        s.connect((host,port))
    except Exception,e:
        msg = traceback.format_exc()
        print ("connect error: " + msg)
    print ('Socket Connected to ' + host)

    #wait for command from cmd  and send it
    while True:
        command = raw_input("Please input command(exit command for close this session):\n")
        if command == "exit":
            print ("Bye bye!")
            break

        if not command:
            print ("command is empty,please input again:")
            continue
        s.send(command)
        s.setblocking(1)                    #防止recv一直在等待数据阻塞主线程

        #等待时间看能否改变
        time.sleep(1)
        print ("\033[1;32;40m reply from server: \033[0m")
        print ("\033[1;32;40m------------------------------------------------------------------------------------------- \033[0m")
        while 1:
            time.sleep(1)
            try:
                reply = s.recv(4096)
            except Exception,e:
                print ("\033[1;32;40m------------------------------------------------------------------------------------------ \033[0m")
                print ("\033[1;31;40m recv except error\033[0m")
                break
            if "Done" in reply:

                print (
                "\033[1;32;40m------------------------------------------------------------------------------------------- \033[0m")
                break
            print ("\033[1;32;40m" + reply + "\033[0m")


print ("Connecting to %s:%d now."% (host,port))
execute(host,port)


s.close()
print ("connection closed!")
