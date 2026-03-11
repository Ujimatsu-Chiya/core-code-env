import sys

READ_PATH = 'user.in'
WRITE_PATH = 'user.out'

class StdinWrapper:
    def __init__(self):
        self.stdin = open(READ_PATH,'r')

    def read_line(self):
        line = self.stdin.readline().rstrip('\n')
        if line == '':
            return None
        else:
            return line


class StdoutWrapper:
    def __init__(self):
        self.stdout = open(WRITE_PATH,'w')

    def write_line(self, s:str):
        self.stdout.write(s + '\n')
