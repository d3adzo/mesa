# mesa
In-progress C2 utlizing NTP as transport protocol.

This doubles as both a valid, working NTP time server and a command and control server.

TODO:
- [x] Server functions as a legitimate NTP Server
- [x] Commands/References are sent via custom NTP packets
- [x] Server handles multiple concurrent connections
- [x] Agent works on Windows, Linux, and macOS
- [x] Easy agent grouping (OS and Service)
- [ ] Single Byte XOR Encryption and Decryption (implemented but broken currently)
- [ ] Command Output (single and multiple)

The creator is not liable for the misuse of any of the following code. 

## Installation
### Server
Python3 must be utilized. Python2 will not work. 

Certain external packages are also used. See **Packages Installed** for list.

Use `pip3 install -r pythonserver/textfiles/requirements.txt` to install.

#### Server Database
Connection to a local MySQL server is required. Agent data is stored and pulled here.
I used a local MySQL 5.7 server. 

### Agent
Golang must be installed. The Makefile uses `go build` .

Certain external packages are also used. See **Packages Installed** for list.

Use `go get <link>` to install.

## Usage
### Server
Run `sudo python3 start.py` 

You will be asked for MySQL credentials, this is for creating a database and saving state.

Once the SQL connection has been made, the listener will start. You will reach the prompts, which is where you will interact with the program.

Enter `help` or use the TAB key for a list of commands at of the prompt levels.

#### Mesa Prompt
This is your main prompt. Display the agent table, enter the DB subprompt, interact with an agent / group of agents, or exit/shutdown. 

Commands: 
 - `agents` ~ display the board of agent entries.
 - `db` ~ enter the database subprompt.
 - `interact <a[gent]/o[s]/s[ervice]> <id>` ~ enter the interact subprompt. 
 - `help` ~ display this list of commands.
 - `exit` ~ quit the program, state will be saved.
 - `shutdown` ~ quit the program, all agents are killed, database is cleaned.
---
#### DB Prompt
This is the DB subprompt. This is where certain DB actions will take place, like adding groupings, removing agents, or describing the agents table.

Commands: 
 - `agents` ~ display the board of agent entries.
 - `group <ip> <os/service> <name>` ~ add a service identifier to an agent. Can specify a IP range. Ex. \"group 10.1.1-15.3 service SMB\"
 - `removeall` ~ remove all agents from the database.
 - `help` ~ display this list of commands.
 - `meta` ~ describe the agent tables metadata.
 - `back` ~ return to the main prompt.
---
#### Interact Prompt
This is the interaction subprompt. Send PING or KILL references to agents, or enter the CMD subprompt.

Commands:
 - `ping` ~ ping agent.
 - `kill` ~ send kill command to agent. confirmed with y/n.
 - `cmd` ~ enter the cmd subprompt.
 - `help` ~ display this list of commands.
 - `back` ~ return to the main prompt.
---
#### CMD Prompt

This is the command subprompt. Send commands to agents here.

Commands: 
 - `<input>` ~ send command `<input>` to agents.
 - `help` ~ display this list of commands.
 - `back` ~ return to the interact prompt.
---
### Client
Run `make`  

This will cross-compile agents. 
- Windows -> `windows-agent.exe`
- Linux -> `linux-agent` (currently broken, must be compiled separately on a linux machine)
- macOS -> `macos-agent`

Once an agent is run, they will setup on the machine and sync with the server. An entry will be added to the server's database, and the agent can now be controlled.

Agents are hardcoded with C2's server IP when compiled, but sending a `PING` Reference (Interact Subprompt) will update the target machine's config.

## Packages Used
### Python3
- scapy
- prompt_toolkit
- termcolor
- tabulate
- mysql.connector

Use `pip3 install -r pythonserver/textfiles/requirements.txt` to install.

### Golang
- github.com/google/gopacket
- github.com/google/gopacket/layers
- github.com/google/gopacket/pcap

Use `go get <link>` to install.

## References

Big thank you to @emmaunel for all the help, check out his C2 project DiscordGO (inspiration!)
- https://github.com/emmaunel/DiscordGo

NTP Server modified: 
- https://github.com/sumit-1/ntpserver/blob/master/ntpserver.py

Helpful for using Scapy for NTP: 
- https://gist.github.com/Dbof/178cf3c4b9eee423b293c51380cd311b

