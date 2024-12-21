from git import Repo
from git import exc
from grit.utils import findRootOfRepo


def pr(argv):

    if(len(argv) < 3):
        printHelp()
        return

    pwd = findRootOfRepo()
    if(pwd == "/"):
        print("ERROR : this directory and non of its parent contains a .git file.")
        return

    repo = Repo.init(pwd)
    dir = pwd.split('/')
    origin_url_fork = 'https://www.github.com/' + dir[-2] + '/' +dir[-1] + '/fork'

    if(argv[1] == 'start'):
        print('creating branch ' + argv[2] )
        branch = repo.create_head(argv[2])
        repo.head.reference = branch
        repo.head.reset(index=True)
        return
    elif(argv[1] == 'push'):
        print('Pushing branch to remote ' + argv[2])
        try:
            repo.git.push('--set-upstream',argv[2],repo.active_branch.name)
        except exc.CommandError as e:
            if("fatal: Could not read from remote repository" in e.stderr):
                print(f"Remote doesn't exist.\nYou can add it by calling 'grit remote add {argv[2]}'")
            return
        origin = repo.remote('origin')
        if('master' in origin.refs):
            compBranch = 'master'
        else :
            compBranch = 'main'

        print('Start a PR --> https://github.com/' + dir[-2] + '/' + dir[-1] + '/compare/' + compBranch + '...' + argv[2] + ':' + repo.active_branch.name)
    else:
        printHelp()
        return

    return

def printHelp():
    print('ERROR: pr option requires two arguments {start/push} [NAME]. ')
    print('--> start: will create a branch named NAME and checkout it (git checkout -b NAME)')
    print('--> push: will push the current branch to remote NAME (git push --set-upstream NAME currBranch)')
    return