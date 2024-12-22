from git import exc
from grit.utils import gritInsideRepoMethod, argument, ProgressToString

@gritInsideRepoMethod("Used to easily dealing with remotes by only using owner name",
            [argument("--add","-a",action='store_true', help="Add remote"),
             argument("remote_name",help="Name of the owner of the remote.")])
def remote(pwd,repo,argv):

    dir = pwd.split('/')

    if(argv.add):

        repo_url = 'git@github.com:' + argv.remote_name + '/' +dir[-1] + '.git'
        origin_url_fork = 'https://www.github.com/' + dir[-2] + '/' +dir[-1] + '/fork'
    
        print('Adding remote ' + argv.remote_name + ' = ' + repo_url + ' and fetching it...')
        try:
            remote = repo.create_remote(argv.remote_name, repo_url)
            pts = ProgressToString()
            remote.fetch(progress=pts)
            pts.printString()
        except exc.CommandError as e:
            if("fatal: Could not read from remote repository" in e.stderr):
                print(f"This remote doesn't exists. You can fork this repository here --> {origin_url_fork}")
                repo.delete_remote(remote)
            elif(f"error: remote {argv.remote_name} already exists." in e.stderr):
                print(f"This remote name is already used.")
            return
        return

    return
