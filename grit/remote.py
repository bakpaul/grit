from git import Repo
from git import exc
import os
from grit.utils import Progress, ProgressToString


def remote(argv,pwd):

    if(len(argv) < 3):
        printHelp()
        return

    dir = pwd.split('/')


    repo = Repo.init(pwd)

    repo_url = 'git@github.com:' + argv[2] + '/' +dir[-1] + '.git'
    origin_url_fork = 'https://www.github.com/' + dir[-2] + '/' +dir[-1] + '/fork'

    if(argv[1] == 'add'):
        print('Adding remote ' + argv[2] + ' = ' + repo_url + ' and fetching it...')
        try:
            remote = repo.create_remote(argv[2], repo_url)
            pts = ProgressToString()
            remote.fetch(progress=pts)
            pts.printString()
        except exc.CommandError as e:
            if("fatal: Could not read from remote repository" in e.stderr):
                print(f"This remote doesn't exists. You can fork this repository here --> {origin_url_fork}")
                repo.delete_remote(remote)
            elif(f"error: remote {argv[2]} already exists." in e.stderr):
                print(f"This remote already exists.")
            return
        return
    else:
        printHelp()
        return

    return

def printHelp():
    print('ERROR: remote option requires two arguments {add} [remotename] which is the github user name. ')
    print('--> if your current repository is repo, the added or removed remote will be added using git remote add remotename git@github.com:remotename/repo.git')
    return