from git.remote import RemoteProgress

class Progress(RemoteProgress):
    def line_dropped(self, line):
        print(line)
    def update(self, *args):
        print(self._cur_line,end='\r')

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