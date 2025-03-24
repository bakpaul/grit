from git import exc
from grit.utils import gritInsideRepoMethod, positionalArgument, flagArgument, ProgressToString, getRemoteNameFromURL, \
    getRepoNameFromURL, optionArgument, Progress
import os

@gritInsideRepoMethod("Used to easily extract a folder and make it a repository while keeping history",
            [optionArgument("target",shortName="-t",nargs='1',help="Target repository. Syntax : remote/repo_name."),
             flagArgument("cont",shortName="--continue",help="Flag to only use when the push phase failed because the remote didn't exist. (The script will tell you when you need it)."),
             positionalArgument("folder_name",help="Name of the owner of the remote.")])
def pluginize(pwd,repo,argv):


    if(argv.target is not None):
        targetInfo = argv.target[0].split('/')

        if(len(targetInfo) == 1):
            print(f"Syntax of target is 'remote/repo_name' e.g. 'grit pluginize myFolder -t bakpaul/myFolderPluginized' ")

        targetRemote = "git@github.com:" + targetInfo[0] + "/" + targetInfo[1] + ".git"

        if(not os.path.isdir(pwd + "/" + argv.folder_name) and not argv.cont):
            print("Folder " + argv.folder_name + " doesn't exist. Please enter a valid subfolder of " + pwd)
            print("--> forgot to use flag '--continue' ?")
            return


        if(not argv.cont):
            print("Pluginizing folder "  + argv.folder_name + " from local repository " + pwd + ".")
            print("--> The pluginized code will be pushed to " + targetRemote + ".")
            print("--> This repository need to exist, please create it with the name '" + targetInfo[1] + "' : https://github.com/new")
            print()
            print("WARNING ! This should only be done on a freshly cloned repository without any local changes and the target repository must be empty.")
            if(input("Do you wish to continue ? [YES/no] : ") == "no"):
                print("Aborting...")
                return
            else:
                print()
        else:
            print("Continuing pluginization. Still need to push to " + targetRemote + "...")
            print()


        try:
            if( not argv.cont ):
                repo.git.filter_repo("--subdirectory-filter", argv.folder_name)
            remote = repo.create_remote(targetInfo[0], targetRemote)
            repo.git.push("-u",targetInfo[0],  repo.head.reference)
        except exc.CommandError as e:
            if("failed to push some refs to" in e.stderr):
                print(f"The targeted remote doesn't exists. Please create it -->  : https://github.com/new")
                print(f"Run 'grit pluginize {argv.folder_name} -t {argv.target[0]} --continue'")
                repo.delete_remote(remote)
            elif("filter-repo" in e.stderr):
                print(f"The git command 'filter-repo' is required, please install it through 'sudo apt install git-filter-repo'.")
            else:
                print(e.stderr)
            return
        print("Done ! Your new plugin is here --> https://github.com/" + '/'.join(targetInfo))
        return

    return
