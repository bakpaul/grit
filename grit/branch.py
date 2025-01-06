from grit.utils import gritInsideRepoMethod
from grit.utils import positionalArgument, flagArgument, optionArgument

from git import exc

@gritInsideRepoMethod("Used to manage branch. Currently the only option is --list <remote> [nb_of_branch]",
            [flagArgument("list","-l", help="Remote from which list "),
             optionArgument("number","-n",nargs='+' ,help="Optional: number of branch to list. If specified, the branch will be sorted in order of last modified."),
             positionalArgument("input",help="The remote name")])
def branch(pwd,repo,argv):
    dir = pwd.split('/')

    if(argv.list):
        try:
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
        except ValueError as e:
            if(f"Remote named '{argv.input}' didn't exist" in str(e)):
                origin_url_fork = 'https://www.github.com/' + dir[-2] + '/' +dir[-1] + '/fork'
                print(f"This remote doesn't exists. You can add it using 'grit remote --add {argv.input}'. You can also fork this repository here --> {origin_url_fork}")
            else:
                print(f"Unknown error : {str(e)}.")

            return
        return

    return
