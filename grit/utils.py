from git.remote import RemoteProgress

class Progress(RemoteProgress):
    def line_dropped(self, line):
        print(line)
    def update(self, *args):
        print(self._cur_line,end='\r')