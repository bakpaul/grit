from git import exc
from grit.utils import gritInsideRepoMethod, positionalArgument, flagArgument, ProgressToString, getRemoteNameFromURL, \
    getRepoNameFromURL, optionArgument


@gritInsideRepoMethod("Used to easily extract a folder and make it a repository while keeping history",
            [optionArgument("target",shortName="-t",nargs='1',help="Target repository. Syntax : remote/repo_name or repo_name. If no remote is specified, the same as the repository's one is used."),
             positionalArgument("folder_name",help="Name of the owner of the remote.")])
def pluginize(pwd,repo,argv):


    if(argv.target):
        targetInfo = argv.target[0].split('/')

        url = repo.git.remote('get-url','origin')
        orig_origin = getRemoteNameFromURL(url)

        if(len(targetInfo) == 1):
            targetInfo = [orig_origin, targetInfo[0]]

        targetRemote = "git@github.com:" + targetInfo[0] + "/" + targetInfo[1] + ".git"

        print("Pluginizing folder "  + argv.folder_name + " from local repository " + pwd + ".")
        print("--> The pluginized code will be pushed to " + targetRemote + ".")
        print("--> This repository need to exist, please create it with the name '" + targetInfo[1] + "' : https://github.com/new")
        print()
        print("WARNING ! This should only be done on a freshly cloned repository without any local changes and the target repository must be empty.")
        if(input("Do you wish to continue ? [YES/no] : ") == "no"):
            print("Aborting...")
            return

        try:
            repo.git.filter_repo("--subdirectory-filter", argv.folder_name)
            remote = repo.create_remote(targetInfo[0], targetRemote)
            repo.git.push("-u",targetInfo[0],  "master")
        except exc.CommandError as e:
            if("fatal: Could not read from remote repository" in e.stderr):
                print(f"The targeted remote doesn't exists. Please create it -->  : https://github.com/new")
                repo.delete_remote(remote)
            return
        return

    return
