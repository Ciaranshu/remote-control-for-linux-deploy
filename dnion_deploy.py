#!/usr/bin/env python
#_*_ coding: utf-8 _*_
import socket, sys, traceback, time,re
from thread import *

port = 40217
End = "Done"
total_reply=[]
reip = re.compile(r'(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d])')


def selectMode():

    while True:
        cmd = raw_input("Supported modes:\n 1. Connect [ip address]\n 2. Execute [script file path] \n (exit command for close this session):\n")
        if 'connect' in cmd:
            host = str(reip.findall(cmd)[0])
            cmdmode(connect(host, port))
        if 'execute' in cmd:
            deployScript = open(cmd[8:], 'r')
            host = str(reip.findall(deployScript.readline())[0])
            s = connect(host, port)
            flag = 0
            for line in deployScript:
                if re.match(reip, str(line)) is not None:
                    flag = 0
                    s.close()
                    print ("connection closed!\n\n")
                    try:
                        host = str(reip.findall(line)[0])
                        s = connect(host, port)
                    except:
                        print ("\033[1;31;40m Error connect" + host + "\033[0m")
                        flag = 1
                        continue

                else:
                    if flag == 0:
                        scriptMode(s, str(line))

        elif 'exit' in cmd:
            break
        else:
            print "unsupported modes, please input again.\n"

#脚本参数提供需要执行的command
#command = sys.argv[2]

#try:
#    remote_ip =  socket.gethostbyname( host )
#except socket.gaierror:
#    print ('Hostname could not be resolved. Exiting')
#    sys.exit()
#print ('Ip address of ' + host + ' is ' + remote_ip)



def connect(host,port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error, msg:
        print ('Failed to create socket, Error code: ' + str(msg[0]) + ',Error  message :' + msg[1])
        sys.exit()

    print ('Socket created successfully')

    s.connect((host,port))
    print ("Connecting to %s:%d now." % (host, port))

    return s


def cmdmode(s):
    # wait for command from cmd  and send it
    while True:
        command = raw_input("Please input command(exit command for close this session):\n")
        if command == "exit":
            print ("Bye bye!")
            break
        if not command:
            print ("command is empty,please input again:")
            continue
        s.send(command)
        s.setblocking(1)  # 防止recv一直在等待数据阻塞主线程

        # 等待时间看能否改变
        time.sleep(1)
        print ("\033[1;32;40m reply from server: \033[0m")
        print (
        "\033[1;32;40m------------------------------------------------------------------------------------------- \033[0m")
        while 1:
            time.sleep(1)
            try:
                reply = s.recv(4096)
            except Exception, e:
                print (
                "\033[1;32;40m------------------------------------------------------------------------------------------ \033[0m")
                print ("\033[1;31;40m recv except error\033[0m")
                break
            if "Done" in reply:
                print (
                    "\033[1;32;40m------------------------------------------------------------------------------------------- \033[0m")
                break
            print ("\033[1;32;40m" + reply + "\033[0m")

    s.close()
    print ("connection closed!\n\n")


def scriptMode(s,command):
    # wait for command from cmd  and send it

    if not command:
        print ("command is empty,please input again:")

    s.send(command)
    s.setblocking(1)  # 防止recv一直在等待数据阻塞主线程

    # 等待时间看能否改变
    time.sleep(1)
    print ("\033[1;32;40m reply from server: \033[0m")
    print (
    "\033[1;32;40m------------------------------------------------------------------------------------------- \033[0m")
    while 1:
        time.sleep(1)
        try:
            reply = s.recv(4096)
        except Exception, e:
            print (
            "\033[1;32;40m------------------------------------------------------------------------------------------ \033[0m")
            print ("\033[1;31;40m recv except error\033[0m")
            break
        if "Done" in reply:
            print (
                "\033[1;32;40m------------------------------------------------------------------------------------------- \033[0m")
            break
        print ("\033[1;32;40m" + reply + "\033[0m")



selectMode()

