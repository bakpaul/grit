from git import Repo
from git import exc

import os
import sys
from grit.utils import Progress


def clone(argv, pwd):

    if(len(argv) != 2):
        printHelp()
        return

    dir = pwd.split('/')


    repo_url = 'git@github.com:'+dir[-1] + '/' + argv[1] + '.git'
    repo_dir = pwd+'/'+argv[1]

    print('Cloning ' + repo_url + ' into folder ' + repo_dir + '...')

    repo = Repo.clone_from(repo_url, repo_dir,progress=Progress())
    sys.stdout.flush()

    return

def printHelp():
    print('ERROR: clone option requires only one argument which is the repository name. The remote will be automatically deducted from your current directory.')
    print('--> if your current directory is mydir, the remote will be set to git@github.com:mydir/repository.git')
    return