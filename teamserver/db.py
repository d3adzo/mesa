import mysql.connector
import datetime
import getpass

class DB:
    #db fields: 
    # agentIp (given) 
    # OS (given) 
    # service (given)
    # status (MIA default)
    # pingtimestamp (given, current timestamp default)
    # missedpings int (0 default)
    def __init__(self):
        pass #check if db exists, if so pulls data from
        #otherwise creates database and tables
        print(colored("Make sure MySQL Server is running.", "yellow"))
        username = input("Enter MySQL username: ")
        password = getpass.getpass(prompt="Enter MySQL password: ")

        self.mydb = mysql.connector.connect(
            host="localhost",
            user=username,
            password=password,
            database = "mesaC2s" #TODO what if the DB doesn't exist? How to create w/o error out
        )

        self.mycursor = mydb.cursor()


        """
        self.mycursor.execute("create database mesaC2s if not exists;") #create msql db

        self.mycursor.execute("use mesaC2s;")

        self.mycursor.execute("create table agents if not exists("
                         "agentID varchar(16) not null primary key,"
                         "os varchar(255) not null,"
                         "service varchar(255) not null,"
                         "status varchar(10) not null default MIA,"
                         "pingtimestamp timestamp null,"
                         "missedpings int not null default 0"
                         ");")
        """

    def addAgent(self, ip, os, service):
        self.mycursor.execute("insert into agents "
                        "(agentIP, OS, service) "
                        "values " 
                        f"({ip}, {os}, {service})")

        print(f"Agent {ip}/{os} added!")

    def deleteAgent(self, ip):
        self.mycursor.execute(f"delete from agents where agentID = {ip}")

        self.mydb.commit()
        print(f"Agent {ip} deleted!")

    def dbPull(self):
        self.mycursor.execute("select * from agents order by service asc")
        #for x in mycursor:
            #print(x)
        return self.mycursor

    def cleanDB(self):
        self.mycursor.execute("delete from agents")

        self.mydb.commit()
        print("DB cleaned!")

    def missingStatus(self, ip): #after 2 pings missed (timestamp+2min)
        self.mycursor.execute("update agents "
                        "set status = \'MIA\'"
                        "where agentID = \'{ip}\'")

        self.mydb.commit()
        print(colored(f"Agent {ip} is MIA!", "yellow")) 

    def deadStatus(self, ip): #after agent killed
        self.mycursor.execute("update agents "
                        "set status = \'dead\'"
                        f"where agentID = \'{ip}\'")

        self.mydb.commit()
        print(colored(f"Agent {ip} is dead!", "red")) 

    def aliveStatus(self, ip): #after receiving beacon
        self.mycursor.execute("update agents "
                        "set status = \'alive\'"
                        f"where agentID = \'{ip}\'")

        self.mydb.commit()
        print(colored(f"Ping from agent {ip}!", "green")) 

    def checkStatus(self):
        #TODO how will i do this? will this run every minute? separate thread?
        #query db for list of all timestamps
        #compare current time to each one
        #if any mia, send to missingstatus method
        #cool
        self.mycursor.execute("select pingtimestamp from agents")



    #adding to db
    #given ip, os, service
    #timestamp null, status MIA
    #on first alive ping from client, current timestamp, alive status
    #start timer only now that timestamp is not null and has a valid value
        