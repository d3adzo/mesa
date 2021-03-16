import mysql.connector
import datetime
import getpass

from termcolor import colored

class DB: #TODO REWORK all based around beacon recieved and packet sniffing
    def __init__(self):
        #check if db exists, if so pulls data from
        #otherwise creates database and tables
        print("Setting up DB...")
        print(colored("Make sure MySQL Server is running.", "yellow"))
        #username = input("Enter MySQL username: ")
        #password = getpass.getpass(prompt="Enter MySQL password: ")
        username = "root"
        password = "mesa"

        self.mydb = mysql.connector.connect(
            host="localhost",
            user=username,
            password=password
        )

        self.mycursor = self.mydb.cursor()
        
        self.mycursor.execute("create database if not exists mesaC2s") #create msql db

        self.mycursor.execute("use mesaC2s")

        self.mycursor.execute("create table if not exists agents("
                         "agentID varchar(16) not null primary key,"
                         "os varchar(255) null,"
                         "service varchar(255) null,"
                         "status varchar(10) not null default \'MIA\',"
                         "pingtimestamp timestamp null)")



    #DB MODS
    def addAgent(self, ip, os, timestamp): #INTERNAL, when receive first (setup) ping
        sqlcmd = "insert into agents (agentID, os, timestamp) values (%s, %s, %s)"
        values = (str(ip), os, str(timestamp)) #TODO make sure stamp is in correct format
        
        self.mycursor.execute(sqlcmd, values)
        self.mydb.commit()

        print(f"Agent {ip}/{os}/{service} added!\n")


    def deleteAgent(self, ip): #INTERNAL, for kill command
        self.mycursor.execute(f"delete from agents where agentID=\'{ip}\'")

        self.mydb.commit()
        print(f"Agent {ip} deleted!\n")


    def dbPull(self): #PUBLIC
        self.mycursor.execute("select * from agents order by service asc")
        return self.mycursor.fetchall()
    

    def pullSpecific(self, grouping, value): #INTERNAL, use this when sending group commands?
        self.mycursor.execute(f"select agentID from agents where {grouping}=\'{value}\'")
        return self.mycursor.fetchall()


    def addGrouping(self, ip, typ, grouping): #PUBLIC
        sqlcmd = "insert into agents (%s) values (%s) where agentID=\'%s\'"
        values = (typ, grouping, str(ip))
        self.mycursor.execute(sqlcmd, values)

        print(f"Identifier \"{grouping}\" added to {str(ip)}!\n")


    def removeAllAgents(self): #PUBLIC, removes all agents
        self.mycursor.execute("delete from agents")

        self.mydb.commit()
        print("All agents removed!\n")


    def updateTimestamp(self, tstamp, agent): #INTERNAL, updates on resync request
        sqlcmd = "insert into agents (pingtimestamp) values (%s) where agentID=\'%s\'"
        values = (tstamp, agent)

        self.mycursor.execute(sqlcmd, values)
        self.mydb.commit()

        #no print statement on resync?

    def describe(self):
        self.mycursor.execute("desc agents")
        for value in self.mycursor.fetchall():
            print(value)


    #STATUS CHECKS
    def missingStatus(self, ip): #INTERNAL, after 3 pings missed (timestamp+3min)
        self.mycursor.execute("update agents "
                        "set status = \'MIA\'"
                        f"where agentID =\'{ip}\'")

        self.mydb.commit()
        print(colored(f"Agent {ip} is MIA!\n", "yellow")) 


    def deadStatus(self, ip): #PUBLIC, after agent killed
        self.mycursor.execute("update agents "
                        "set status = \'dead\'"
                        f"where agentID = \'{ip}\'")

        self.mydb.commit()
        print(colored(f"Agent {ip} is dead!\n", "red")) 


    def aliveStatus(self, ip): #INTERNAL, after receiving beacon
        self.mycursor.execute("update agents "
                        "set status = \'alive\'"
                        f"where agentID = \'{ip}\'")

        self.mydb.commit()
        print(colored(f"Ping from agent {ip}!\n", "green")) 


    def checkStatus(self):
        #TODO how will i do this? will this run every minute? separate thread?
        #query db for list of all timestamps
        #compare current time to each one
        #if any mia, send to missingstatus method
        #cool
        self.mycursor.execute("select pingtimestamp from agents")

    #TODO add clean method. removes full db (for shutdown option)

    #adding to db
    #given ip, os, service
    #timestamp null, status MIA
    #on first alive ping from client, current timestamp, alive status
    #start timer only now that timestamp is not null and has a valid value

    """
+---------------+--------------+------+-----+---------+-------+
| Field         | Type         | Null | Key | Default | Extra |
+---------------+--------------+------+-----+---------+-------+
| agentID       | varchar(16)  | NO   | PRI | NULL    |       |
| os            | varchar(255) | YES  |     | NULL    |       |
| service       | varchar(255) | YES  |     | NULL    |       |
| status        | varchar(10)  | NO   |     | MIA     |       |
| pingtimestamp | timestamp    | YES  |     | NULL    |       |
+---------------+--------------+------+-----+---------+-------+
"""
        