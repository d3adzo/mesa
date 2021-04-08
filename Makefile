DIRECTORY=goclient/bin
MAC=macos-agent
LINUX=linux-agent
WIN=windows-agent.exe
FLAGS=-ldflags "-s -w"


all: clean create-directory agent-mac agent-windows agent-linux

create-directory:
	mkdir ${DIRECTORY}

agent-mac:
	echo "Compiling macos binary"
	env GOOS=darwin GOARCH=amd64 go build ${FLAGS} -o ${DIRECTORY}/${MAC} goclient/cmd/main.go

agent-windows:
	echo "Compiling Windows binary"
	env GOOS=windows GOARCH=amd64 go build ${FLAGS} -o ${DIRECTORY}/${WIN} goclient/cmd/main.go

agent-linux:
	echo "Compiling Linux binary"
	env CGO_ENABLED=1 GOOS=linux GOARCH=amd64 go build ${FLAGS} -o ${DIRECTORY}/${LINUX} goclient/cmd/main.go

clean:
	rm -rf ${DIRECTORY}
