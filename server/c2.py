from server import convert
from transport import packets

#send given cmd to API for conversion
def convertCMD(cmd):
    return convert.encode(cmd)

#receive output and decode, return to TS/(DB)?
def receiveOutput(output):
    return convert.decode(output)

#send command via NTP message, craft mal packet
def sendCMD(tsOBJ, cmd, destGroup, endpoint):
    if destGroup == "agent":
        pass #send single command
    else:
        data = tsOBJ.getDBObj().pullSpecific(destGroup, endpoint)
        for ip in data:
            print(f"Sending \"{cmd}\" to {ip[0]} ({endpoint})")
        #send command to selected endpoint agent
    encoded = convertCMD(cmd)
    cPacket = packets.CommandPacket()
        