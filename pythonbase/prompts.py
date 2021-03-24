from teamserver import teamserver
from server import c2

from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter
from termcolor import colored

from os import system
import ipaddress


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

        if user_input == "agents":
            TS.displayBoard()

        elif user_input == "db":
            dbPrompt(TS)

        elif "interact" in user_input: #TODO add check to make sure ip/os/service given exists in DB
            arr = user_input.split(' ')
        #try: #TODO uncomment this
            if arr[1] == "agent" or arr[1] == "a":
                interactPrompt("agent", arr[2], TS)

            elif arr[1] == "os" or arr[1] == "o":
                interactPrompt("os", arr[2], TS)

            elif arr[1] == "service" or arr[1] == "s":
                interactPrompt("service", arr[2], TS)

            else:
                print(colored("Incorrect arguments given.\n SYNTAX: interact <A[GENT]/O[S]/S[ERVICE]> <id>", 'yellow'))
        #except:
            #print(colored("Incorrect arguments given.\n SYNTAX: interact <A[GENT]/O[S]/S[ERVICE]> <id>", 'yellow'))
        
        elif user_input == "clear":
            system('clear')

        elif user_input == "help":
            print('Base Command List')
            print(colored(" agents ~ display the board of agent entries.\n "
                            "db ~ enter the database subprompt. add/delete/edit entries here.\n "
                            "interact <A[GENT]/O[S]/S[ERVICE]> <id> ~ enter the interact subprompt. Ping/kill agents, or enter the CMD subprompt here.\n "
                            "help ~ display this list of commands.\n "
                            "exit ~ quit the program, state will be saved.\n "
                            "shutdown ~ quit the program, all agents are killed, database is cleaned.",
                            'yellow'))

        elif user_input == "exit":
            print("\nTime, Dr. Freeman?\nIs it really that time again?\n")
            exit()

        elif user_input == "shutdown":
            TS.shutdown()
            #TODO send kill to all agents, removeall agents from agents, delete db
        elif user_input == "":
            pass #do nothing    
        else:
            print(colored(' Base command not recognized. Enter \"help\" for command list.\n', 'red'))


def dbPrompt(TS):
    #TODO verify ip/service/os exists in db
    dbCMDs = ['group', 'list', 'removeall', 'help', 'meta', 'back']
    dbCompleter = WordCompleter(dbCMDs,
                                ignore_case=True)
    while True:
        user_input = (prompt("MESA {DB} ~ ",
                             history=FileHistory('textfiles/history.txt'),
                             auto_suggest=AutoSuggestFromHistory(),
                             completer=dbCompleter
                             )).lower()

        if user_input.split(' ')[0] == "group":
            arr = user_input.split(' ')
            try:
                TS.getDBObj().addGrouping(arr[1], arr[2], arr[3]) #TODO add ip validation
            except:
                print(colored("Incorrect syntax. Should be \'group <ip> <os/service> <name>\'", 'yellow'))

        elif user_input == "list":
            TS.displayBoard()

        elif user_input == "removeall":
            confirmation = (input("Confirm (y/n)? ")).lower()
            if confirmation == "y":
                TS.getDBObj().removeAllAgents()

            elif confirmation == "n":
                pass #back to prompt

        elif user_input == "help":
            print('DB Subcommand List')
            print(colored(" group <ip> <os/service> <name> ~ add a service identifier to an agent.\n "
                          "list ~ list all agent entries.\n " 
                          "removeall ~ remove all agents from the database.\n " 
                          "meta ~ describe the agent tables metadata.\n "
                          "help ~ display this list of commands.\n "
                          "back ~ return to the main prompt.",
                          'yellow'))

        elif user_input == "meta":
            TS.getDBObj().describe()
        elif user_input == "back" or user_input == "exit":
            return
        elif user_input == "":
            pass #do nothing
        elif user_input == "clear":
            system('clear')
        else:
            print(colored('DB subcommand not recognized. Enter \"help\" for list of DB subcommands.', 'red'))


def interactPrompt(interactType, id, TS):
    interactCMDs = ['ping', 'kill', 'cmd', 'list', 'help', 'back']
    interactCompleter = WordCompleter(interactCMDs,
                                ignore_case=True)
    while True:
        user_input = (prompt("MESA {"+interactType+"/"+id+"} ~ ",
                             history=FileHistory('textfiles/history.txt'),
                             auto_suggest=AutoSuggestFromHistory(),
                             completer=interactCompleter
                             )).lower()

        if user_input == "ping":
            c2.sendRefCMD(TS, interactType, id, "PING")
            #listener/NTPS: receive resync req/ping 
            #TS/DB: update timestamp and enter into db alive status, create new entry if IP does not exist
            #NTPS: send actual time update packet

        elif user_input == "kill": 
            confirmation = (input("Confirm (y/n)? ")).lower()
            if confirmation == "y":
                c2.sendRefCMD(TS, interactType, id, "KILL")
                #TODO update status dead in DB
            else:
                continue #back to interact prompt

        elif user_input == "cmd":
            cmdPrompt(interactType, id, TS)
            

        elif user_input == "help":
            print('Interact Subcommand List')
            print(colored(" ping ~ ping agent.\n "
                          "kill ~ send kill command to agent. confirmed with y/n.\n "
                          "cmd ~ enter the cmd subprompt.\n "
                          "help ~ display this list of commands.\n "
                          "back ~ return to the main prompt.",
                          'yellow'))

        elif user_input == "list":
            if interactType == "agent":
                print(colored(" Agent ~ " + TS.getDBObj().pullSpecific("agentid", id)[0][0]))  
            else:
                for entry in TS.getDBObj().pullSpecific(interactType, id):
                    print(colored(" Agent ~ " + entry[0]))  

        elif user_input == "back" or user_input == "exit":
            return 
        elif user_input == "":
            pass #do nothing
        elif user_input == "clear":
            system('clear')
        else:
            print(colored('Interact subcommand not recognized. Enter \"help\" for list of Interact subcommands.', 'red'))


def cmdPrompt(interactType, id, TS):
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
        elif user_input == "back" or user_input == "exit":
            return
        elif user_input == "":
            pass #do nothing
        elif user_input == "clear":
            system('clear')
        else:
            #TODO sending quotes (and other chars) is being weird, fix this
            c2.sendCMD(TS, user_input, interactType, id) #TODO what about running exes/commands that hang?
            
            #C: get output and encode in NTP response
            #S: decode output
            #S: send output to TS
            #TS: print output in prompt