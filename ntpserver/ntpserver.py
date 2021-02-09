from transport import packets
from server import c2
import datetime

class NTPServer:

    def __init__(self):
        pass #"start" the server?

    def getTime():
        return datetime.datetime.now() #returns current time

    def sendTime(source, destination):
        createNTPPacket()
        #send packet

    def createNTPPacket(source, destination):
        timeinfo = getTime()
        nPacket = packets.NTPPacket(source, destination, info)

    #receive beacon via NTP response, send to teamserver for board
    def beaconReceived():
        pass
        #C: sends ntp resync req
        #S/NTPS: receive 'beacon'
        #S: send timestamp to TS/DB
        #S/NTPS: craft actual time packet and send

    def listen():
        pass #listening for beacon callouts, should be always running on a separate thread
