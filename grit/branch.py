from git import Repo
from git import exc
import os
from grit.utils import gritMethod, argument
from grit.utils import findRootOfRepo

@gritMethod("Used to manage branch. Currently the only option is --list <remote> [nb_of_branch]",
            [argument("--list","-l",action='store_true', help="Remote from which list "),
             argument("--number","-n",nargs=1 ,help="Optional: number of branch to list. If specified, the branch will be sorted in order of last modified."),
             argument("input",help="The remote name")])
def branch(argv):

    pwd = findRootOfRepo()
    if(pwd == "/"):
        print("ERROR : this directory and non of its parent contains a .git file.")
        return

    repo = Repo.init(pwd)

    if(argv.list):
        remote_refs = repo.remote(argv.input).refs
        if(argv.number is None):
            for refs in remote_refs:
                print(refs.name.split('/')[1])
        else:          
            tempDict = {}
            for refs in remote_refs:
                tempDict[refs.commit.committed_datetime.isoformat()] = refs.name.split('/')[1]
            sortedBranches=sorted(tempDict.items(),reverse = True)
            for i in range(min(int(argv.number[0]),len(sortedBranches))):
                print(sortedBranches[i][1])
        return

    return
