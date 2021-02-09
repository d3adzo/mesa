from teamserver import db

class Teamserver:
    def __init__(self):
        self.agentDB = db.DB()

    def getDBObj(self):
        return self.agentDB

    #display the board of active c2s, call again to refresh
    def displayBoard(self):
        data = self.agentDB.dbPull()
        #TODO parse data into cool table
    
    def printOutput(self): #?does this go somewhere else
        pass #print command output
        #take into account single/group (one/many) command responses

    #have prompt to send commands to one specific or all C2s
    #control prompt (teamserver) for c2 entry edits (ex. remove)