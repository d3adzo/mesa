import datetime
import socket
import struct
import time
import threading
import select
import sys
import queue as Queue

"""
THIS CODE WAS TAKEN FROM https://github.com/sumit-1/ntpserver AND MODIFIED BY ME
"""

def system_to_ntp_time(timestamp):
    return timestamp + NTP.NTP_DELTA

def _to_int(timestamp):
    return int(timestamp)

def _to_frac(timestamp, n=32):
    return int(abs(timestamp - _to_int(timestamp)) * 2**n)

def _to_time(integ, frac, n=32):
    return integ + float(frac)/2**n	


class NTP:
    """Helper class defining constants."""

    _SYSTEM_EPOCH = datetime.date(*time.gmtime(0)[0:3])
    """system epoch"""
    _NTP_EPOCH = datetime.date(1900, 1, 1)
    """NTP epoch"""
    NTP_DELTA = (_SYSTEM_EPOCH - _NTP_EPOCH).days * 24 * 3600
    """delta between system and NTP time"""

    REF_ID_TABLE = {
            'DNC': "DNC routing protocol",
            'NIST': "NIST public modem",
            'TSP': "TSP time protocol",
            'DTS': "Digital Time Service",
            'ATOM': "Atomic clock (calibrated)",
            'VLF': "VLF radio (OMEGA, etc)",
            'callsign': "Generic radio",
            'LORC': "LORAN-C radionavidation",
            'GOES': "GOES UHF environment satellite",
            'GPS': "GPS UHF satellite positioning",
    }
    """reference identifier table"""

    STRATUM_TABLE = {
        0: "unspecified",
        1: "primary reference",
    }
    """stratum table"""

    MODE_TABLE = {
        0: "unspecified",
        1: "symmetric active",
        2: "symmetric passive",
        3: "client",
        4: "server",
        5: "broadcast",
        6: "reserved for NTP control messages",
        7: "reserved for private use",
    }
    """mode table"""

    LEAP_TABLE = {
        0: "no warning",
        1: "last minute has 61 seconds",
        2: "last minute has 59 seconds",
        3: "alarm condition (clock not synchronized)",
    }
    """leap indicator table"""


class NTPPacket:
    
    _PACKET_FORMAT = "!B B B b 11I"
    """packet format to pack/unpack"""

    def __init__(self, version=2, mode=3, tx_timestamp=0):

        self.leap = 0
        """leap second indicator"""
        self.version = version
        """version"""
        self.mode = mode
        """mode"""
        self.stratum = 0
        """stratum"""
        self.poll = 0
        """poll interval"""
        self.precision = 0
        """precision"""
        self.root_delay = 0
        """root delay"""
        self.root_dispersion = 0
        """root dispersion"""
        self.ref_id = 0
        """reference clock identifier"""
        self.ref_timestamp = 0
        """reference timestamp"""
        self.orig_timestamp = 0
        self.orig_timestamp_high = 0
        self.orig_timestamp_low = 0
        """originate timestamp"""
        self.recv_timestamp = 0
        """receive timestamp"""
        self.tx_timestamp = tx_timestamp
        self.tx_timestamp_high = 0
        self.tx_timestamp_low = 0
        """tansmit timestamp"""
        
    def to_data(self):
        try:
            packed = struct.pack(NTPPacket._PACKET_FORMAT,
                (self.leap << 6 | self.version << 3 | self.mode),
                self.stratum,
                self.poll,
                self.precision,
                _to_int(self.root_delay) << 16 | _to_frac(self.root_delay, 16),
                _to_int(self.root_dispersion) << 16 |
                _to_frac(self.root_dispersion, 16),
                self.ref_id,
                _to_int(self.ref_timestamp),
                _to_frac(self.ref_timestamp),
                #Change by lichen, avoid loss of precision
                self.orig_timestamp_high,
                self.orig_timestamp_low,
                _to_int(self.recv_timestamp),
                _to_frac(self.recv_timestamp),
                _to_int(self.tx_timestamp),
                _to_frac(self.tx_timestamp))
        except struct.error:
            return None

        return packed

    def from_data(self, data):
        try:
            unpacked = struct.unpack(NTPPacket._PACKET_FORMAT,
                    data[0:struct.calcsize(NTPPacket._PACKET_FORMAT)])
            return "working"
        except struct.error:
            return None


        self.leap = unpacked[0] >> 6 & 0x3
        self.version = unpacked[0] >> 3 & 0x7
        self.mode = unpacked[0] & 0x7
        self.stratum = unpacked[1]
        self.poll = unpacked[2]
        self.precision = unpacked[3]
        self.root_delay = float(unpacked[4])/2**16
        self.root_dispersion = float(unpacked[5])/2**16
        self.ref_id = unpacked[6]
        self.ref_timestamp = _to_time(unpacked[7], unpacked[8])
        self.orig_timestamp = _to_time(unpacked[9], unpacked[10])
        self.orig_timestamp_high = unpacked[9]
        self.orig_timestamp_low = unpacked[10]
        self.recv_timestamp = _to_time(unpacked[11], unpacked[12])
        self.tx_timestamp = _to_time(unpacked[13], unpacked[14])
        self.tx_timestamp_high = unpacked[13]
        self.tx_timestamp_low = unpacked[14]

    def GetTxTimeStamp(self):
        return (self.tx_timestamp_high,self.tx_timestamp_low)

    def SetOriginTimeStamp(self,high,low):
        self.orig_timestamp_high = high
        self.orig_timestamp_low = low


def resync(socket, data, addr):
 
    taskQueue = Queue.Queue()

    recvTimestamp = system_to_ntp_time(time.time())
    taskQueue.put((data,addr,recvTimestamp))
    
    data,addr,recvTimestamp = taskQueue.get(timeout=1)
    recvPacket = NTPPacket()
    retvalue = recvPacket.from_data(data)
    if retvalue == None:
        return

    timeStamp_high,timeStamp_low = recvPacket.GetTxTimeStamp()
    sendPacket = NTPPacket(version=3,mode=4)
    sendPacket.stratum = 2
    sendPacket.poll = 10

    sendPacket.ref_timestamp = recvTimestamp-5
    sendPacket.SetOriginTimeStamp(timeStamp_high,timeStamp_low)
    print(sendPacket.orig_timestamp, sendPacket.orig_timestamp_high, sendPacket.orig_timestamp_low)
    sendPacket.recv_timestamp = recvTimestamp
    sendPacket.tx_timestamp = system_to_ntp_time(time.time())

    retvalue = sendPacket.to_data()
    if retvalue == None:
        return
    
    socket.sendto(retvalue,addr)