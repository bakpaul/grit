import sys
from grit.pr import pr
from grit.remote import remote
from grit.clone import clone
from grit.branch import branch
from grit.pluginize import pluginize
import os


def main():
    if(len(sys.argv) == 1):
        printHelp()
        return

    if(sys.argv[1] == '-h'):
        printHelp()
        return

    if(sys.argv[1] == 'pr'):
        pr(sys.argv[2:])
        return
    elif(sys.argv[1] == 'clone'):
        clone(sys.argv[2:])
        return
    elif(sys.argv[1] == 'remote'):
        remote(sys.argv[2:])
        return
    elif(sys.argv[1] == 'branch'):
        branch(sys.argv[2:])
        return
    elif(sys.argv[1] == 'pluginize'):
        pluginize(sys.argv[2:])
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
    print("  - pluginize")


if __name__ == '__main__':
    exit(main())

