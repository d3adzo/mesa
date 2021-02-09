import datetime
from scapy.all import IP, UDP, NTP

class Packet:
    def __init__(self, destination):
        self.destination = destination
        self.base = yes #craft the base packet
    
class NTPPacket(Packet):
    def __init__(self, destination):
        super().__init__(destination)
        self.destination = destination
   
class CommandPacket(Packet):
    def __init__(self, destination, command):
        super().__init__(destination)
        self.command = command
    
    def sComPacket(self, destination):
        pass
    