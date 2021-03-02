package packet
/*
import (
	"net"
)*/

type NTPPacket struct {
	srcIP []byte
	dstIP []byte 
	refID []byte
	data []byte
}