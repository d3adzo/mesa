import transport
import server

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
    def receiveBeacon():
        pass
