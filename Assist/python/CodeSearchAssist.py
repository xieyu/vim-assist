import subprocess
import re
import os

from SearchIterm import TagIterm
from Common import CommonUtil

class CodeSearchAssist:
    searchDir = None
    #public interface:
    @staticmethod
    def search(symbol):
        symbol = symbol.strip()
        prefix = "-n"
        if CodeSearchAssist.searchDir:
            prefix = "-n -f %s" %(CodeSearchAssist.searchDir)
        cmd_arg = "%s %s" % (prefix, symbol)
        output = CodeSearchAssist.cmd(cmd_arg)
        return CodeSearchAssist.createTagCandidate(output)

    #private helper functions
    @staticmethod
    def createTagCandidate(output):
        result = []
        pattern = re.compile("([^ \t:]*):(\d*):(.*$)")
        for line in output.split("\n"):
            line = line.strip()
            if line:
                (filePath, row, codeSnip) = pattern.search(line).groups()
                iterm = TagIterm(name = "", path = AgAssist.getFilePath(filePath), lineNumber = row, codeSnip = codeSnip.strip())
                result.append(iterm)
        return result

    @staticmethod
    def setSearchDir(dir):
        path = os.path.abspath(dir)
        CodeSearchAssist.searchDir = path

    @staticmethod
    def cmd(cmd_args):
        cmd = "csearch %s" % cmd_args
        process = subprocess.Popen(cmd, stdout = subprocess.PIPE, shell = True, cwd = AgAssist.workdir)
        output = process.stdout.read()
        del process
        return output

    @staticmethod
    def makeIndex(dir):
        absPath = os.path.abspath(dir)
        cmd = "cindex %s" % absPath
        subprocess.Popen(cmd, shell=True)

