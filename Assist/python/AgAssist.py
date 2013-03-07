import subprocess
import re
import os

from SearchIterm import TagIterm
from Common import CommonUtil

class AgAssist:
    workdir=None
    FilePattern = None
    #public interface:
    @staticmethod
    def search(symbol):
        symbol = symbol.strip()
        cmd = "--nocolor --nogroup --column %s" % symbol
        output = AgAssist.cmd(cmd)
        return AgAssist.createTagCandidate(output)

    @staticmethod
    def clearWorkdir():
        AgAssist.workdir = None

    @staticmethod
    def setWorkdir(workdir):
        workdir = os.path.expandvars(os.path.expanduser(workdir))
        if os.path.exists(workdir):
            AgAssist.workdir = workdir
        else:
            print "%s is note exists"
        print "change dir to %s" % AgAssist.workdir

    @staticmethod
    def clearWorkdir():
        AgAssist.workdir = None

    #private helper functions
    @staticmethod
    def createTagCandidate(output):
        result = []
        pattern = re.compile("(\S*):(\d*):(\d*):(.*$)")
        for line in output.split("\n"):
            line = line.strip()
            if line:
                (filePath, row, col, codeSnip) = pattern.search(line).groups()
                iterm = TagIterm(name = "", path = AgAssist.getFilePath(filePath), lineNumber = row, codeSnip = codeSnip.strip())
                result.append(iterm)
        return result

    @staticmethod
    def getFilePath(filePath):
        if AgAssist.workdir is None:
            return filePath
        else:
            return os.path.join(AgAssist.workdir, filePath)

    @staticmethod
    def cmd(cmd_args):
        cmd = "ag %s" % cmd_args
        if AgAssist.workdir:
            process = subprocess.Popen(cmd, stdout = subprocess.PIPE, shell = True, cwd = AgAssist.workdir)
        else:
            process = subprocess.Popen(cmd, stdout = subprocess.PIPE, shell = True)
        output = process.stdout.read()
        del process
        return output
