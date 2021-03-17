from transport import packets

import datetime



def getTime():
    return datetime.datetime.now() #returns current time, TODO format in NTP way


def sendTime(self, destination):
    timeinfo = self.getTime()
    nPacket = packets.NTPPacket(destination, timeinfo)

    nPacket.sendTimePacket()



#receive beacon via NTP response, send to teamserver for board
def resyncReceived(self, timestamp, ip, agentDB): 
    agentDB.aliveStatus(ip, timestamp)

    sendTime(ip)
    #S/NTPS: craft actual time packet and send
    #TODO change to alive status (DB), or if doesn't exist make entry w/ alive status

    
