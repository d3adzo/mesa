import scapy

class Packet:
    def __init__(self, destination):
        self.destination = destination
        self.craftBase(destination)

    def craftBase(destination):
        pass #craft base packet (lower layers)
    
   
class CommandPacket(Packet):
    def __init__(self, destination, command):
        super().__init__(destination)
        self.command = command
    


class NTPPacket(Packet):
    def __init__(self, destination, TimeInfo):
        super().__init__(destination)
        self.TimeInfo = TimeInfo



    