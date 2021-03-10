package agent

import (
	"fmt"
	"net"
	"os"
	"runtime"
	"strings"
)

//Agent information
type Agent struct {
	OpSys     string
	ShellType string
	ShellFlag string
	IFace     string
	ServerIP  []byte
	MyIP      []byte
}

//DetectOS - detects which OS agent is running on
func DetectOS() (string, string, string) {
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

//GetNetAdapter - gets network interface of agent
func GetNetAdapter() string {
	var final string
	potentials := [4]string{"eth0", "en0", "ens33", "Ethernet"}

	devices, err := net.Interfaces()

	if err != nil {
		fmt.Println("error gathering nics")
	}

	final = "eth0" //default
	for _, device := range devices {
		for i := 0; i < len(potentials); i++ {
			if strings.Contains(strings.ToLower(device.Name), strings.ToLower(potentials[i])) {
				final = device.Name
				goto End
			}
		}
	}
End:
	fmt.Println(final)
	return final

}

//GetServerIP - gets IP address of NTP server
func GetServerIP() []byte {
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

//GetMyIP - gets local IP
func GetMyIP() []byte {
	addrs, err := net.InterfaceAddrs()
	if err != nil {
		os.Stderr.WriteString("Oops: " + err.Error() + "\n")
		os.Exit(1)
	}

	for _, a := range addrs {
		if ipnet, ok := a.(*net.IPNet); ok && !ipnet.IP.IsLoopback() {
			if ipnet.IP.To4() != nil {
				fmt.Println(ipnet.IP.String())
				return ipnet.IP
			}
		}
	}
	return nil
} //function code taken from github.com/emmuanuel/DiscordGo
