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
        username = input("Enter MySQL username: ")
        password = getpass.getpass(prompt="Enter MySQL password: ")

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
                         "os varchar(255) not null,"
                         "service varchar(255) not null,"
                         "status varchar(10) not null default \'MIA\',"
                         "pingtimestamp timestamp null)")

        #so do i check for data in and then pull? how do this?        

    def addAgent(self, ip, os, service):
        #print(f"insert into agents (agentID, os, service) values (\'{ip}\', \'{os}\', \'{service}\')")
        sqlcmd = "insert into agents (agentID, os, service) values (%s, %s, %s)"
        values = (str(ip), os, service)
        
        self.mycursor.execute(sqlcmd, values)
        self.mydb.commit()

        print(f"Agent {ip}/{os}/{service} added!\n")

    def deleteAgent(self, ip):
        self.mycursor.execute(f"delete from agents where agentID=\'{ip}\'")

        self.mydb.commit()
        print(f"Agent {ip} deleted!\n")

    def dbPull(self):
        self.mycursor.execute("select * from agents order by service asc")
        return self.mycursor.fetchall()
    
    def pullSpecific(self, grouping, value):
        self.mycursor.execute(f"select agentID from agents where {grouping}=\'{value}\'")
        return self.mycursor.fetchall()

    def removeAllAgents(self): #removes all agents
        self.mycursor.execute("delete from agents")

        self.mydb.commit()
        print("All agents removed!\n")

    def missingStatus(self, ip): #after 2 pings missed (timestamp+2min)
        self.mycursor.execute("update agents "
                        "set status = \'MIA\'"
                        "where agentID =\'{ip}\'")

        self.mydb.commit()
        print(colored(f"Agent {ip} is MIA!\n", "yellow")) 

    def deadStatus(self, ip): #after agent killed
        self.mycursor.execute("update agents "
                        "set status = \'dead\'"
                        f"where agentID = \'{ip}\'")

        self.mydb.commit()
        print(colored(f"Agent {ip} is dead!\n", "red")) 

    def aliveStatus(self, ip): #after receiving beacon
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
| os            | varchar(255) | NO   |     | NULL    |       |
| service       | varchar(255) | NO   |     | NULL    |       |
| status        | varchar(10)  | NO   |     | MIA     |       |
| pingtimestamp | timestamp    | YES  |     | NULL    |       |
+---------------+--------------+------+-----+---------+-------+
"""
        