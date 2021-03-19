from prompts import mesaPrompt
from server import listener

from os import geteuid
from teamserver import teamserver
from threading import Thread

#TODO on client, make command run in background (ie linux &)?

#Entrypoint
def main():
    if geteuid() != 0:
        print('You must run as root')
        exit(1)
    else:
        TS = teamserver.Teamserver() #setup NTP and pulls from db
        mesaPrompt(TS)


main()