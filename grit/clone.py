from git import Repo
from git import exc

import os
import sys
from grit.utils import *

@gritMethod("Clone repository which owner has the same name as the current folder",
            [argument("repository_name")])
def clone(argv):

    pwd = os.getcwd()
    dir = pwd.split('/')


    repo_url = 'git@github.com:'+dir[-1] + '/' + argv.repository_name + '.git'
    repo_dir = pwd+'/'+argv.repository_name

    print('Cloning ' + repo_url + ' into folder ' + repo_dir + '...')

    progressObj=Progress()
    repo = Repo.clone_from(repo_url, repo_dir,progress=progressObj)
    progressObj.printLastLine()

    return
