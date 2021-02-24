from prompts import mesaPrompt
from os import geteuid

#TODO pip3 install reqs file
#TODO on client, make command run in background (ie linux &)

#Entrypoint
def main():
    if os.geteuid() != 0:
        print('You must run as root')
        exit(1)

    mesaPrompt()


main()