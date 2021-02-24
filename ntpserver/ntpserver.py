from transport import packets
from server import c2
import datetime

class NTPServer:

    def __init__(self):
        #thread the listen call
        self.listenResync()

    def getTime():
        return datetime.datetime.now() #returns current time


    def sendTime(self, destination):
        timeinfo = self.getTime()
        nPacket = packets.NTPPacket(destination, timeinfo)

        nPacket.sendTimePacket()


    def listenResync(self):
        #run in loop, thread when beacon recv
        pass #listening for beacon callouts, should be always running on a separate thread
        self.resyncReceived() #TODO arguments?


    #receive beacon via NTP response, send to teamserver for board
    def resyncReceived(self): 
        pass
        #S/NTPS: receive 'beacon'
        #S: send timestamp to TS/DB
        #S/NTPS: craft actual time packet and send
        #TODO change to alive status (DB), or if doesn't exist make entry w/ alive status

        
