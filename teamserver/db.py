

class DB:
    #db fields: 
    # agentIp (given) 
    # OS (given) 
    # status (MIA default)
    # pingtimestamp (current timestamp default)
    # missedpings int (0 default)
    #?hostname field?
    def __init__(self):
        pass #check if db exists, if so pulls data from
        #otherwise creates database and tables

    def addAgent(ip, os):
        pass

    def deleteAgent(ip):
        pass

    def dbPull():
        pass

    def cleanDB():
        pass

    def missingStatus(ip): #after 2 pings missed (timestamp+2min)
        pass

    def deadStatus(ip): #after agent killed
        pass

    def aliveStatus(ip): #after receiving beacon
        pass #updates timestamp