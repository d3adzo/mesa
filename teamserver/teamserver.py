from teamserver import db

class Teamserver:
    def __init__(self):
        self.agentDB = db.DB()

    def getDBObj():
        return self.agentDB

    #display the board of active c2s, call again to refresh
    def displayBoard():
        pass
    
    def printOutput():
        pass #print command output
        #take into account single/group (one/many) command responses

    def getC2List(): #static list
        pass

    def updateC2List(): #update c2 list (pull db)
        pass

    #have prompt to send commands to one specific or all C2s
    #control prompt (teamserver) for c2 entry edits (ex. remove)

    #TODO maybe for speed purposes, don't always query db. have some sort of static list of entries
    #TODO pull only if edits to db are made (add/delete/missingping,etc.)