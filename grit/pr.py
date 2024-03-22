from git import Repo
from git import exc
import os


def pr(argv):

    if(len(argv) < 3):
        printHelp()
        return

    pwd = os.getcwd()

    repo = Repo.init(pwd)


    if(argv[1] == 'start'):
        print('creating branch ' + argv[2] )
        branch = repo.create_head(argv[2])
        repo.head.reference = branch
        repo.head.reset(index=True, working_tree=True)
        return
    elif(argv[1] == 'push'):
        print('Pushing branch to remote ' + argv[2])
        repo.git.push('--set-upstream',argv[2],repo.active_branch.name)
    else:
        printHelp()
        return

    return

def printHelp():
    print('ERROR: pr option requires two arguments {start/push} [NAME]. ')
    print('--> start: will create a branch named NAME and checkout it (git checkout -b NAME)')
    print('--> push: will push the current branch to remote NAME (git push --set-upstream NAME currBranch)')
    return