from git.remote import RemoteProgress
import os
import functools
import argparse
from typing import Dict, List, Any, Tuple
from git import Repo
from enum import Enum

class ArgumentType(Enum):
    NONE       = 0
    POSITIONAL = 1
    OPTION     = 2
    FLAG       = 3

class argument:
    type : ArgumentType
    def __init__(self, fullName : str, shortName : str = None, help : str = None):
        self._fullName = fullName
        self._shortName = shortName
        self._help = help
        self.type = ArgumentType.NONE

    def getUsage(self) -> str:
        pass

    def getOptionsLine(self) -> str:
        pass

    def parse(self, inputArguments:list[str] ) -> tuple[str, int, list[int],str]:
        # Look for the strings that are for this argument and the return
        # 1. the name of the variable that should be created
        # 2. the position of the flag in the input argument (-1 if positional argument)
        # 3. The list containing the position of the values passed if any
        # 4. String info
        pass

class positionalArgument(argument):
    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)
        self.type = ArgumentType.POSITIONAL

    def getUsage(self):
        return self._fullName

    def getOptionsLine(self):
        return "  " + self._fullName + "\t" + self._help

    def parse(self, inputArguments:list[str] ) -> tuple[str, int, list[int], str]:
        if(len(inputArguments) == 0):
            return self._fullName, -1, [ ], "_ERROR_"
        else:
            return self._fullName, -1, [len(inputArguments) -1], "_FOUND_"


class flagArgument(argument):
    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)
        self.type = ArgumentType.FLAG

    def getUsage(self):
        return self._fullName

    def getOptionsLine(self):
        return "  " + self._fullName + "\t" + self._help

    def parse(self, inputArguments:list[str] ) -> tuple[str, int, list[int],str]:
        for i in range(len(inputArguments)):
            if((inputArguments[i] == self._shortName) or (inputArguments[i] == self._fullName)):
                    return self._fullName, i, [ ], "_FOUND_"
        return self._fullName, -1, [ ], "_NOTFOUND_"




class optionArgument(argument):
    def __init__(self,  *arg, nargs=1,**kwargs):
        super().__init__(*arg, **kwargs)
        self.type = ArgumentType.OPTION
        self._nargs = nargs


    def getUsage(self):
        return "[" + self._shortName + " " + str(self._nargs) + ":" +self._fullName +  "]"

    def getOptionsLine(self):
        return "  " + self._fullName + "\t" + self._help

    def parse(self, inputArguments:list[str] ) -> tuple[str, int, list[int],str]:
        if(self._nargs == "+"):
            nargs = 1
        else:
            nargs = int(self._nargs)
        for i in range(len(inputArguments)):
            if((inputArguments[i] == self._shortName) or (inputArguments[i] == self._fullName)):
                if(i + nargs >= len(inputArguments)):
                    return self._fullName, -1, [ ], "_ERROR_"
                else :
                    return self._fullName, i, [ j+i+1 for j in range(nargs) ], "_FOUND_"
        if(self._nargs=='+'):
            return self._fullName, -1, [ ], "_NOTFOUND_"
        else:
            return self._fullName, -1, [ ], "_ERROR_"

class parser:
    class parserOutput:
        def __init__(self):
            self.datas = {}
        def addItem(self,itemName,value):
            self.datas[itemName] = value
        def __getattr__(self,item):
            if(item in self.datas):
                return self.datas[item]
            else:
                return None



    def __init__(self, prog:str,description:str = None):
        self._prog = prog
        self._description = description
        self.argumentsPos = []
        self.argumentsOpt = []
        self.argumentsFla = []

    def addArgument(self, arg:argument):
        match arg.type:
            case ArgumentType.POSITIONAL:
                self.argumentsPos.append(arg)
                return
            case ArgumentType.OPTION:
                self.argumentsOpt.append(arg)
                return
            case ArgumentType.FLAG:
                self.argumentsFla.append(arg)
                return
            case _:
                raise RuntimeError('Argument is of base class, which is not possible.')
                return


    def printUsage(self):
        firstLine = "usage : " + self._prog
        for flag in self.argumentsFla :
            firstLine += " [" + flag.getUsage() + "]"
        for opt in self.argumentsOpt :
            firstLine += " [" + opt.getUsage() + "]"
        for pos in self.argumentsPos :
            firstLine += " " + pos.getUsage()
        print(firstLine)

    def parseArgs(self, input) -> parserOutput:
        out = parser.parserOutput()

        for flag in self.argumentsFla :
            itemName, idx, dataList, info = flag.parse(input)
            if(info == "_ERROR_"):
                self.printUsage()
                exit(0)
            elif(info == '_NOTFOUND_'):
                out.addItem(itemName,False)
            else:
                out.addItem(itemName,True)
                input.pop(idx)

        for option in self.argumentsOpt:
            itemName, idx, dataList, info = option.parse(input)
            if(info == "_ERROR_"):
                self.printUsage()
                exit(0)
            elif(info == "_NOTFOUND_"):
                out.addItem(itemName,None)
            else:
                out.addItem(itemName,[input[i] for i in dataList])
                for i in reversed(dataList) :
                    input.pop(i)
                input.pop(idx)

        for positional in self.argumentsPos:
            itemName, idx, dataList, info = positional.parse(input)
            if(info == "_ERROR_"):
                self.printUsage()
                exit(0)
            out.addItem(itemName,input[dataList[0]])
            for i in reversed(dataList) :
                input.pop(i)

        if(len(input) !=0):
            self.printUsage()
            exit(0)

        return out



def gritOutsideRepoMethod(description,argList : List[argument]):
    def gritMethod_inner(func):
        @functools.wraps(func)
        def wrapper(inputedArgs):
            parserObj = parser(
                prog="grit " + func.__name__,
                description=description)
            for param in argList:
                parserObj.addArgument(param)
            if(len(inputedArgs) == 0):
                parserObj.printUsage()
                exit(0)

            argumentsFromParse = parserObj.parseArgs(inputedArgs)

            func(argumentsFromParse)
        return wrapper
    return gritMethod_inner

def gritInsideRepoMethod(description,argList : List[argument]):
    def gritMethod_inner(func):
        @functools.wraps(func)
        def wrapper(inputedArgs):
            pwd = findRootOfRepo()
            if(pwd == "/"):
                print("ERROR : this directory and non of its parent contains a .git file.")
                return

            repo = Repo.init(pwd)

            parserObj = parser(
                prog="grit " + func.__name__,
                description=description)
            for param in argList:
                parserObj.addArgument(param)
            if(len(inputedArgs) == 0):
                parserObj.printUsage()
                exit(0)

            argumentsFromParse = parserObj.parseArgs(inputedArgs)

            func(pwd,repo,argumentsFromParse)
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