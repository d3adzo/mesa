package agent

import (
	"fmt"
	"net"
	"os"
	"os/exec"
	"runtime"
)

type Agent struct {
	opsys string
	shellType string
	shellFlag string
	iface string
	serverIP []byte
	myIP []byte
}


func detectOS() (string, string, string) { //detects which OS the agent is on
	sys := "Unknown"
	shell := "temp"
	flag := "temp"
	if runtime.GOOS == "windows" {
		sys = "Windows"
		shell = "cmd"
		flag = "/c"
	} else if runtime.GOOS == "linux" {
		sys = "Linux"
		shell = "/bin/sh"
		flag = "-c"
	}else {
		fmt.println("operating system not detected")
		os.Exit(1)
	}

	return sys, shell, flag
}


func getNetAdapter(shellType string, shellFlag string) string { //gets the network interface of the system
	var cmd string
	if shellFlag == "/c" {
		cmd = "ipconfig"
	}else {
		cmd = "ip a"
	}
	output := exec.Command(shellType, shellFlag, cmd).Output()
	
	
	return "something"
}

func getServerIP() []byte {
	input := os.Args[1]
	addr := net.ParseIP(input)

	//where to get the IP from? user input?
	if addr == nil {
		fmt.Println("Invalid server IP address")
		os.Exit(1)
	} else {
		fmt.Println("The address is ", addr.String())
		return addr
}

func getMyIP(iface string) []byte {

}


func setup(agent Agent) { //set up NTP configurations based on opsys, adds firewall rule every 5 min?

}//return 0 if everything set up, 1 otherwise, try again?





