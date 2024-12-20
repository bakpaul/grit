from git import Repo
from git import exc
import os
from grit.utils import Progress


def branch(argv,pwd):

    if(len(argv) < 3):
        printHelp()
        return

    dir = pwd.split('/')


    repo = Repo.init(pwd)

    repo_url = 'git@github.com:' + argv[2] + '/' +dir[-1] + '.git'


    if(argv[1] == 'list'):
        remote_refs = repo.remote(argv[2]).refs
        if(len(argv) == 3):
            for refs in remote_refs:
                print(refs.name.split('/')[1])
        else:          
            tempDict = {}
            for refs in remote_refs:
                tempDict[refs.commit.committed_datetime.isoformat()] = refs.name.split('/')[1]
            sortedBranches=sorted(tempDict.items(),reverse = True)
            for i in range(min(int(argv[3]),len(sortedBranches))):
                print(sortedBranches[i][1])
        return
        
    else:
        printHelp()
        return

    return

def printHelp():
    print('ERROR: branch option requires two arguments {list} [remotename] (number) which is the github user name. ')
    print('--> if your current repository is repo, the branch will be the one from git@github.com:remotename/repo.git. If number is specified, the branches are sorted byt most recently modified and only te number specified are displayed.')
    return
