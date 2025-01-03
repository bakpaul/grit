from git import exc
from grit.utils import  argument,gritInsideRepoMethod

@gritInsideRepoMethod("Used to start PR and push them (provide quick link for PR starting on github)",
            [argument("--start","-s",action='store_true', help="Create a branch with the given name "),
             argument("--push","-p",action='store_true' ,help="Push the current branch in the given remote."),
             argument("input",help="In start mode: the branch name. In push mode: the remote name.")])
def pr(pwd,repo,argv):

    dir = pwd.split('/')

    if(argv.start):
        print('creating branch ' + argv.input )
        branch = repo.create_head(argv.input )
        repo.head.reference = branch
        repo.head.reset(index=True)
        return
    elif(argv.push):
        print('Pushing branch to remote ' + argv.input )
        try:
            repo.git.push('--set-upstream',argv.input,repo.active_branch.name)
        except exc.CommandError as e:
            if("fatal: Could not read from remote repository" in e.stderr):
                print(f"Remote doesn't exist.\nYou can add it by calling 'grit remote add {argv.input}'")
            return
        origin = repo.remote('origin')
        if('master' in origin.refs):
            compBranch = 'master'
        else :
            compBranch = 'main'

        print('Start a PR --> https://github.com/' + dir[-2] + '/' + dir[-1] + '/compare/' + compBranch + '...' + argv.input + ':' + repo.active_branch.name)

        return

    return
