from git import exc
from grit.utils import  gritInsideRepoMethod, ProgressToString
from grit.utils import positionalArgument, flagArgument

@gritInsideRepoMethod("Used to start PR and push them (provide quick link for PR starting on github)",
            [flagArgument("start","-s", help="Create a branch with the given name "),
             flagArgument("push","-p",help="Push the current branch in the given remote."),
             positionalArgument("input",help="In start mode: the branch name. In push mode: the remote name.")])
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

        originName_repo = '.'.join(repo.git.remote('get-url','origin').split(':')[1].split('.')[:-1])

        print('Start a PR --> https://github.com/' + originName_repo + '/compare/' + compBranch + '...' + argv.input + ':' + repo.active_branch.name)

        return

    return
