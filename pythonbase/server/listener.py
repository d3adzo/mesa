"""
sole purpose is to listen consistenty for NTP traffic
if resync is recieved, send to ntpserver.py
if cmdoutput is received, send to c2.py
"""
import socket


def on_new_client(clientsocket,addr):
    while True:
        msg = clientsocket.recv(1024)
        #do some checks and if msg == someWeirdSignal: break:
        print('bruh')
    clientsocket.close()


def start():
    while True:
        sniff(filter="port 123", prn=process_packet, iface=iface, store=False)


    s.close()


