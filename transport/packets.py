import datetime
from scapy.all import IP, UDP, NTP

class Packet:
    def __init__(self, destination):
        self.destination = destination
        self.baseline = "\x1c\x01\x11\xe9" + "\x00"*7 #something is wrong here
    

class NTPPacket(Packet):
    def __init__(self, destination, timeinfo):
        super().__init__(destination)
    

    def sendTimePacket(self):
        pass
   

class CommandPacket(Packet):
    def __init__(self, destination, command):
        super().__init__(destination)
        self.command = command
    
    
    def sendCommandPacket(self):
        if len(self.command) > 32:
            cmdArr = [self.command[i:i+32] for i in range(0, len(self.command), 32)]
        else:
            cmdArr = [self.command]

        for ctr in range(0, len(cmdArr)):
            if ctr < len(cmdArr)-1:
                refId = str("COMU".encode('utf-8')).strip('b\'') #Command Unfinished
            else:
                refId = str("COMD".encode('utf-8')).strip('b\'')  #Command Finished

            ucode = str(cmdArr[ctr].encode("utf-8")).strip('b\'') #Encoded command

            ntpPayload = self.baseline + refId + ucode +"\x00"*(32-len(cmdArr[ctr]))
            packet = IP(dst=self.destination)/UDP(dport=123,sport=50000)/(ntpPayload)

            send(packet)


class IDPacket(Packet):
    def __init__(self, destination, refId):
        super().__init__(destination)
        self.refId = refId


    def sendIdPacket(self):
        payload = self.baseline + str(self.refId.encode('utf-8').strip('b\'')) + 32*"\x00"
        packet = IP(dst=self.destination)/UDP(dport=123,sport=50000)/(payload)

        send(packet)
    