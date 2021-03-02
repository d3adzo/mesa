package agent

import (
	"fmt"
	"net"
	"os"
	"os/exec"
	"runtime"
)

type Agent struct {
	OpSys string
	ShellType string
	ShellFlag string
	IFace string
	ServerIP []byte
	MyIP []byte
}


func DetectOS() (string, string, string) { //detects which OS the agent is on
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
	} else if runtime.GOOS == "darwin" {
		sys = "macOS"
		shell = "/bin/sh"
		flag = "-c"
	} else {
		fmt.Println("operating system not detected")
		os.Exit(1)
	}

	return sys, shell, flag
}


func GetNetAdapter(shellType string, shellFlag string) (string) { //gets the network interface of the system
	var cmd string
	if shellFlag == "/c" {
		cmd = "ipconfig"
	} else {
		cmd = "ifconfig" //TODO change to ip a later
	}
	output,err := exec.Command(shellType, shellFlag, cmd).Output()
	if err != nil {
		fmt.Println("command couldn't run")
	}
	var final = string(output)
	fmt.Println(final)
	
	return final
}

func GetServerIP() ([]byte) {
	input := os.Args[1]
	addr := net.ParseIP(input) //syntax might be wrong

	//where to get the IP from? user input?
	if addr == nil {
		fmt.Println("Invalid server IP address")
		os.Exit(1)
	} else {
		fmt.Println("The address is ", addr.String())
		
	}
	return addr
}

func GetMyIP(iface string) ([]byte) { 
	//fmt.Println(iface)
	addr := net.ParseIP(iface)
	return addr
}


func Setup(agent Agent) { //set up NTP configurations based on opsys, adds firewall rule every 5 min?
	fmt.Println("lol")
}//return 0 if everything set up, 1 otherwise, try again?



