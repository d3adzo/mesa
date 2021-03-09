from prompts import mesaPrompt
from os import geteuid
from teamserver import teamserver

#TODO pip3 install reqs file
#TODO on client, make command run in background (ie linux &)

#Entrypoint
def main():
    if geteuid() != 0:
        print('You must run as root')
        exit(1)
    else:
        TS = teamserver.Teamserver() #setup NTP and pulls from db
        mesaPrompt(TS)


main()