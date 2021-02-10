from teamserver import db
from ntpserver import ntpserver

from termcolor import colored

class Teamserver:
    def __init__(self):

        #try:
        self.agentDB = db.DB()
        """
        except:
            print(colored("Problem connecting to the MySQL DB! \n"
                    "Make sure that the credentials entered are correct/MySQL Server is running. \n"
                    "Exiting...",
                    "red"))
            exit()
        """
        self.NTPServer = ntpserver.NTPServer()

    def getDBObj(self):
        return self.agentDB

    def getNTPServer(self):
        return self.NTPServer

    #display the board of active c2s, call again to refresh
    def displayBoard(self):
        data = self.agentDB.dbPull()
        #TODO parse data into cool table
    
    def printOutput(self): #?does this go somewhere else
        pass #print command output
        #take into account single/group (one/many) command responses