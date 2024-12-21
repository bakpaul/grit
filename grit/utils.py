from git.remote import RemoteProgress
import os

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