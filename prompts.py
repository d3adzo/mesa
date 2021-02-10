from teamserver import teamserver
from server import c2

from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter
from termcolor import colored

from os import system
import ipaddress

TS = teamserver.Teamserver() #setup and pulls from db

def mesaPrompt(): #TS is teamserver object
    f = open("textfiles/logo.txt", "r")
    reading = f.read()
    print(colored(reading, "red"))
    print('\nEnter "help" for list of commands.\n')

    baseCMDs = ['agents', 'db', 'interact', 'clear', 'help', 'exit', 'shutdown']
    MesaCompleter = WordCompleter(baseCMDs,
                                  ignore_case=True)
    while True:
        user_input = (prompt("MESA ~ ",
                             history=FileHistory('textfiles/history.txt'),
                             auto_suggest=AutoSuggestFromHistory(),
                             completer=MesaCompleter
                             )).lower()

        if user_input == "agents":
            TS.displayBoard()
        elif user_input == "db":
            dbPrompt()
        elif user_input.split(' ')[0] == "interact": # interact single c2/some (db) group identifier (select * from c2s where ex. os = linux)
            try:
                arr = user_input.split(' ')
                if arr[1] == "agent" or arr[1] == "a":
                    interactPrompt("agent", arr[2])

                elif arr[1] == "os" or arr[1] == "o":
                    interactPrompt("os", arr[2])

                elif arr[1] == "service" or arr[1] == "s":
                    interactPrompt("service", arr[2])

                else:
                    print(colored("Incorrect arguments given.\n SYNTAX: interact <A[GENT]/G[ROUP]> <id>", 'yellow'))
            except:
                print(colored("Incorrect arguments given.\n SYNTAX: interact <A[GENT]/G[ROUP]> <id>", 'yellow'))
        
        elif user_input == "clear":
            system('clear')

        elif user_input == "help":
            print('Base Command List')
            print(colored(" agents ~ display the board of agent entries.\n "
                            "db ~ enter the database subprompt. add/delete/edit entries here.\n "
                            "interact <A[GENT]/O[S]/S[ERVICE]> <id> ~ enter the interact subprompt. Ping/kill agents, or enter the CMD subprompt here.\n "
                            "clear ~ clear the prompt.\n "
                            "help ~ display this list of commands.\n "
                            "exit ~ quit the program, state will be saved.\n "
                            "shutdown ~ quit the program, all agents are killed, database is cleaned.",
                            'yellow'))

        elif user_input == "exit":
            print("\nTime, Dr. Freeman?\nIs it really that time again?\n")
            exit()

        elif user_input == "shutdown":
            exit() #for now
            pass  # full cleanup process and exit 
            #TODO clean db
            
        else:
            print(colored('Base command not recognized. Enter \"help\" for command list.', 'red'))


def dbPrompt():
    dbCMDs = ['add', 'delete', 'list', 'removeall', 'help', 'back']
    dbCompleter = WordCompleter(dbCMDs,
                                ignore_case=True)
    while True:
        user_input = (prompt("MESA {DB} ~ ",
                             history=FileHistory('textfiles/history.txt'),
                             auto_suggest=AutoSuggestFromHistory(),
                             completer=dbCompleter
                             )).lower()

        if user_input.split(' ')[0] == "add":
            #try:
                sep = user_input.split(' ')
                try:
                    ip = ipaddress.ip_address(sep[1])
                except:
                    print("Invalid IP, try again")
                    continue
                
                TS.getDBObj().addAgent(str(ip), sep[2], sep[3]) #add agent to db

            #except:
                #print(colored("Incorrect arguments given.\n "
                 #   "SYNTAX: add <ip> <OS> <service>", 'yellow'))

        elif user_input.split(' ')[0] == "delete":
            try:
                sep = user_input.split(' ')
                try:
                    ip = ipaddress.ip_address(sep[1])
                except:
                    print("Invalid IP, try again")
                    continue

                TS.getDBObj().deleteAgent(ip) #delete agent from db

            except:
                print(colored("Incorrect arguments given.\n SYNTAX: delete <ip>", 'yellow'))

        elif user_input == "list":
            TS.getDBObj().dbPull()
            TS.displayBoard()

        elif user_input == "removeall":
            confirmation = (input("Confirm (y/n)? ")).lower()
            if confirmation == "y":
                TS.getDBObj().removeAllAgents()

            elif confirmation == "n":
                pass #back to prompt

        elif user_input == "help":
            print('DB Subcommand List')
            print(colored(" add <ip> <os> <service> ~ add agent to the database.\n "
                          "delete <ip> ~ delete agent from the database.\n "
                          "list ~ list all agent entries.\n " 
                          "removeall ~ empty the database.\n " #TODO make it so not during active, agents must be killed.
                          #"pull ~ manually update C2 board.\n " #TODO pull updated list for board update, run list after
                          "help ~ display this list of commands.\n "
                          "back ~ return to the main prompt.",
                          'yellow'))

        elif user_input == "back":
            return

        else:
            print(colored('DB subcommand not recognized. Enter \"help\" for list of DB subcommands.', 'red'))


def interactPrompt(interactType, id):
    interactCMDs = ['ping', 'kill', 'cmd', 'help', 'back']
    interactCompleter = WordCompleter(interactCMDs,
                                ignore_case=True)
    while True:
        user_input = (prompt("MESA {"+interactType+"/"+id+"} ~ ",
                             history=FileHistory('textfiles/history.txt'),
                             auto_suggest=AutoSuggestFromHistory(),
                             completer=interactCompleter
                             )).lower()
        #submenu, add/del/listAgents/agentCmdOutput/removeall/pull(from existing, maybe does this auto.)/back
        if user_input == "ping":
            pass  #ping agent
            #S: convert (reference id ping)
            #TR: craft NTPPacket
            #S/NTPS: send packet to selected client
            #C: raw socket, see ref id ping
            #C: either send resync req or something with refid pong
            #S/NTPS: receive resync req/pong 
            #S/NTPS: send actual time update packet?
        elif user_input == "kill": 
            pass  #send agent kill command, y/n confirmation
            confirmation = (input("Confirm (y/n)?")).lower()
            if confirmation == "y":
                pass #follow through with kill command
            elif confirmation == "n":
                pass #back to prompt
        elif user_input == "cmd":
            cmdPrompt(interactType, id)
        elif user_input == "help":
            print('Interact Subcommand List')
            print(colored(" ping ~ ping agent.\n "
                          "kill ~ send kill command to agent. confirmed with y/n.\n "
                          "cmd ~ enter the cmd subprompt.\n "
                          "help ~ display this list of commands.\n "
                          "back ~ return to the main prompt.",
                          'yellow'))
        elif user_input == "back":
            return 
        else:
            print(colored('Interact subcommand not recognized. Enter \"help\" for list of Interact subcommands.', 'red'))


def cmdPrompt(interactType, id):
    cmds = ['help','back']
    cmdCompleter = WordCompleter(cmds,
                                ignore_case=True)
    while True:
        user_input = (prompt("MESA {"+interactType+"/"+id+"/CMD} ~ ",
                             history=FileHistory('textfiles/history.txt'),
                             auto_suggest=AutoSuggestFromHistory(),
                             completer=cmdCompleter
                             )).lower()

        if user_input == "help":
            print('Subcommand List')
            print(colored(" <CMD> ~ send CMD to agent.\n "
                          "help ~ display this list of commands.\n "
                          "back ~ return to the interact prompt.",
                          'yellow'))
        elif user_input == "back":
            return
        else:
            c2.sendCMD(user_input, interactType, id)
            pass #TODO what about running exes/commands that hang?s
            #S: encode command
            #TR: create commandpacket with encoded command
            #S: send commandpacket to selected client
            #C: raw socket looking for identifier (ref id comd?), parse command
            #C: run command
            #C: get output and encode in NTP response
            #S: decode output
            #S: send output to TS
            #TS: print output in prompt

    #create c2 objs and connect them to
    #establish what c2s will exist, connect to teamserver obj
    #set up teamserver obj w c2 info

    #setup DB?
    #setup beacon graphing


    #TODO add shell?

#TODO add enter key 