from git.remote import RemoteProgress
import os
import functools
import argparse
from typing import Dict, List, Any, Tuple

class argument:
    def __init__(self, fullName, shortName=None, action=None,nargs=None, default=None, help=None):
        self._fullName = fullName
        self._shortName = shortName
        self._action = action
        self._nargs = nargs
        self._default = default
        self._help = help

    def addArgument(self,parser):
        parameterList = []
        if self._shortName is not None:
            parameterList.append(self._shortName)
        parameterList.append(self._fullName)

        parameterDict = {}
        if self._action is not None:
            parameterDict["action"] = self._action
        if self._nargs is not None:
            parameterDict["nargs"] = self._nargs
        if self._default is not None:
            parameterDict["default"] = self._default
        if self._help is not None:
            parameterDict["help"] = self._help

        parser.add_argument(*parameterList,**parameterDict)



def gritMethod(description,argList : List[argument]):

    def gritMethod_inner(func):
        @functools.wraps(func)
        def wrapper(inputedArgs):
            parser = argparse.ArgumentParser(
                prog="grit " + func.__name__,
                description=description)
            for param in argList:
                param.addArgument(parser)
            if(len(inputedArgs) == 0):
                parser.print_usage()
                return

            argumentsFromParse = parser.parse_args(inputedArgs)

            func(argumentsFromParse)
        return wrapper
    return gritMethod_inner



class Progress(RemoteProgress):
    def line_dropped(self, line):
        print(line)
        self.last_line=line

    def update(self, *args):
        print(self._cur_line,end='\r')
        self.last_line=self._cur_line

    def printLastLine(self):
        print(self.last_line)


class ProgressToString(RemoteProgress):

    def __init__(self):
        super().__init__()
        self.string = ""
    def line_dropped(self, line):
        self.string = self.string + "\n" + line
    def update(self, *args):
        self.string = self.string + "\n" + self._cur_line
    def printString(self):
        print(self.string)

def findRootOfRepo():
    pwd = os.getcwd()
    while (not os.path.isdir(pwd+"/.git")) and (pwd != "/"):
        pwd = os.path.realpath(pwd + "/../")

    return pwd