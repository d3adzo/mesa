from prompts import mesaPrompt
from teamserver import teamserver

from os import geteuid


#Entrypoint
def main():
    if geteuid() != 0:
        print('You must run as root')
        exit(1)
    else:
        TS = teamserver.Teamserver() #setup NTP and pulls from db
        mesaPrompt(TS)


main()