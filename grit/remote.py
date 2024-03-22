from git import Repo
from git import exc
import os
from grit.utils import Progress


def remote(argv):

    if(len(argv) < 3):
        printHelp()
        return

    pwd = os.getcwd()
    dir = pwd.split('/')


    repo = Repo.init(pwd)

    repo_url = 'git@github.com:' + argv[2] + '/' +dir[-1] + '.git'

    if(argv[1] == 'add'):
        print('Adding remote ' + argv[2] + ' = ' + repo_url + ' and fetching it...')
        remote = repo.create_remote(argv[2], repo_url)
        remote.fetch(progress=Progress())
        return
    else:
        printHelp()
        return

    return

def printHelp():
    print('ERROR: remote option requires two arguments {add} [remotename] which is the github user name. ')
    print('--> if your current repository is repo, the added or removed remote will be added using git remote add remotename git@github.com:remotename/repo.git')
    return