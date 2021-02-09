import transport
import server
import datetime

class NTPServer:

    def __init__(self):
        pass

    def getTime():
        info = TimeInfo()
        return info

    def sendTime(c2obj):
        createNTPPacket(c2obj.ipaddr, c2obj.osys)
        #send packet

    def createNTPPacket(source, destination):
        info = getTime()
        nPacket = NTPPacket(source, destination, info)

    #receive beacon via NTP response, send to teamserver for board
    def beaconReceived():
        pass
        #C: sends ntp resync req
        #S/NTPS: receive 'beacon'
        #S: send timestamp to TS/DB
        #S/NTPS: craft actual time packet and send

    def listen():
        pass #listening for beacon callouts, should be always running on a separate thread
