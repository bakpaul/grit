from grit.utils import gritOutsideRepoMethod
from grit.utils import positionalArgument, flagArgument, optionArgument
import os
from git import exc
from git import Repo


def dumpInformation(repository, configFile, outputFolder):

    return

@gritOutsideRepoMethod("Used to save and load current state of github repositories inside a tree. Options are <save/load> <output (-o)> <input (-i)>",
            [flagArgument("save","-s" ,help="Dump the tree inside the input directory into the dump folder."),
             flagArgument("load","-l" ,help="Build the tree from input files"),
             optionArgument("input","-i" ,nargs=1, help="In save mode: directory to be saved. In load mode: directory containing saved files."),
             optionArgument("output","-o",nargs=1, help="In save mode: directory where to save files. In load mode: directory where to recreate tree. Will be created if non existent.")
             flagArgument("treatHidden","-t" ,help="Don't ignore hidden directories")])
def tree(argv):
    pwd = os.getcwd()

    canonInput = os.path.realpath(argv.input[0])
    if(not os.path.isdir(canonInput)):
        print('Provide an existing path as input : ')
        print(' - In save mode: directory to be saved. ')
        print(' - In load mode: directory containing saved files.')
        exit(1)

    canonOutput = os.path.realpath(argv.output[0])
    if(not os.path.isdir(canonOutput)):
        os.makedirs(canonOutput)
    elif(len(os.listdir(canonOutput)) != 0):
        print('Output dir must be empty.')
        exit(1)

    if(argv.save):
        for root, dirs, files in os.walk(canonInput):
            if('.git' in dirs): #This is a git repo, save state.
                repo = Repo.init(root)

                pass

            if(not argv.treatHidden): #Filter hidden folders
                for dir in dirs:
                    if(dir[0]=='.'):
                        dirs.remove(dir)

    elif(argv.load):
        pass


    return


def treatFolder(folder, configFile, outputFolder):

    return
