import sys
from grit.pr import pr
from grit.remote import remote
from grit.clone import clone
from grit.branch import branch
import os


def main():
    if(len(sys.argv) == 1):
        printHelp()
        return

    #Find root directory of the repo
    pwd = os.getcwd()
    while (not os.path.isdir(pwd+"/.git")) and (pwd != "/"):
        pwd = os.path.realpath(pwd + "/../")

    if(pwd == "/"):
        print("ERROR : this directory and non of its parent contains a .git file.")
        return


    if(sys.argv[1] == 'pr'):
        pr(sys.argv[1:],pwd)
        return
    elif(sys.argv[1] == 'clone'):
        clone(sys.argv[1:])
        return
    elif(sys.argv[1] == 'remote'):
        remote(sys.argv[1:],pwd)
        return
    elif(sys.argv[1] == 'branch'):
        branch(sys.argv[1:],pwd)
        return
    else:
        printHelp()
        return


def printHelp():
    print("grit is a pr utility. It requires an argument form the following list :")
    print("  - clone")
    print("  - pr")
    print("  - remote")
    print("  - branch")


if __name__ == '__main__':
    exit(main())

