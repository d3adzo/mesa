import mysql.connector
import datetime
import getpass

from termcolor import colored

class DB: 
    def __init__(self):
        print("Setting up DB...")
        print(colored("Make sure MySQL Server is running.", "yellow"))
        #username = input("Enter MySQL username: ") #TODO add back
        #password = getpass.getpass(prompt="Enter MySQL password: ")
        username = "root"
        password = "mesa"

        self.mydb = mysql.connector.connect(
            host="localhost",
            user=username,
            password=password
        )
        self.mycursor = self.mydb.cursor(buffered=True)
        
        self.mycursor.execute("create database if not exists mesaC2s") #create msql db

        self.mycursor.execute("use mesaC2s")

        self.mycursor.execute("create table if not exists agents("
                         "agentID varchar(16) not null primary key,"
                         "os varchar(255) null,"
                         "service varchar(255) null,"
                         "status varchar(10) not null default \'ALIVE\',"
                         "pingtimestamp timestamp null)")



    #DB MODS
    def addAgent(self, ip, timestamp, status): #INTERNAL, when receive first (setup) ping
        sqlcmd = "insert into agents (agentID, timestamp, status) values (%s, %s, %s)"
        values = (str(ip), str(timestamp), status)
        
        self.mycursor.execute(sqlcmd, values)
        self.mydb.commit()

        print(colored(f"Agent {ip}/{os}/{service} added!\n", "yellow"))


    def deleteAgent(self, ip): #INTERNAL, for kill command
        self.mycursor.execute(f"delete from agents where agentID=\'{ip}\'")

        self.mydb.commit()
        print(colored(f" Agent {ip} deleted!\n", "yellow"))


    def dbPull(self): #PUBLIC
        self.checkStatus()

        self.mycursor.execute("select * from agents order by agentID asc")
        return self.mycursor.fetchall()
    

    def pullSpecific(self, grouping, value): #INTERNAL, use this when sending group commands?
        self.checkStatus()
        
        self.mycursor.execute(f"select agentID from agents where {grouping}=\'{value}\'")
        return self.mycursor.fetchall()


    def addGrouping(self, ip, typ, grouping): #PUBLIC
        sqlcmd = f"update agents set {typ} = \'{grouping}\' where agentID = \'{str(ip)}\'"
        self.mycursor.execute(sqlcmd)
        self.mydb.commit()

        print(colored(f"Identifier \"{grouping}\" added to Agent {str(ip)}!\n", "yellow"))


    def removeAllAgents(self): #PUBLIC, removes all agents
        self.mycursor.execute("delete from agents")

        self.mydb.commit()
        print(colored(" All agents removed!\n", "yellow"))


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
        print(colored(f" Agent {ip} is MIA!\n", "yellow")) 


    def deadStatus(self, ip): #PUBLIC, after agent killed
        self.mycursor.execute("update agents "
                        "set status = \'dead\'"
                        f"where agentID = \'{ip}\'")

        self.mydb.commit()
        print(colored(f" Agent {ip} is dead!\n", "red")) 


    def aliveStatus(self, ip, timestamp): #INTERNAL, after receiving beacon
        self.mycursor.execute(f"select agentID from agents where agentID = \'{ip}\'")
        resp = self.mycursor.fetchall()
        print(resp, "resp thingy", ip)
        if resp != None:
            if resp[0] != ip:
                self.addAgent(ip, timestamp, "ALIVE")
            else:
                self.mycursor.execute("update agents "
                        f"set status, timestamp = \'alive\',\'{timestamp}\'"
                        f"where agentID = \'{ip}\'")

                self.mydb.commit()
        
        print(colored(f" Ping from agent {ip}!\n", "green")) 


    def checkStatus(self): #internal, called on each summon of the table
        #query db for list of all timestamps
        #compare current time to each one
        #if any mia, send to missingstatus method
        tscurrent = datetime.datetime.now()
        strcurrent = "{:%Y-%m-%d %H:%M:%S}".format(tscurrent)

        t2 = datetime.datetime.strptime(strcurrent, "%Y-%m-%d %H:%M:%S")

        self.mycursor.execute("select pingtimestamp,agentID from agents")
        data = self.mycursor.fetchall()
        if data == None:
            return # skip if no agents in table

        for entry in data:
            check = entry[0] #%Y-%m-%d %H:%M:%S
            t1 = datetime.datetime.strptime(check, "%Y-%m-%d %H:%M:%S") #TODO fix error here

            difference = t2 - t1

            if difference.seconds/60 > 3.0:
                self.missingStatus(entry[1])


    def cleanDB(self): #EXTERNAL, called on 'shutdown'
        self.mycursor.execute("drop table agent")



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
        