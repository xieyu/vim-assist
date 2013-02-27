import subprocess
import re
import os
import shelve

from SearchIterm import TagIterm
from Common import CommonUtil

class GtagsAssist:
    workdir=None
    #public interface:
    @staticmethod
    def searchSymbolRef(symbol):
        symbol = symbol.strip()
        output = GtagsAssist.globalCmd("-axr %s" % symbol)
        return GtagsAssist.createTagCandidate(output)

    @staticmethod
    def searchSymbolDefine(symbol):
        symbol= symbol.strip()
        output = GtagsAssist.globalCmd("-ax %s" % symbol)
        return GtagsAssist.createTagCandidate(output)

    @staticmethod
    def searchFile(symbol):
        name = name.strip()
        output = GtagsAssist.globalCmd("-Pai %s" % name)
        return GtagsAssist.createFileCandidate(output)

    @staticmethod
    def setWorkdir(workdir):
        workdir = os.path.expandvars(os.path.expanduser(workdir))
        if os.path.exists(workdir):
            GtagsAssist.workdir = workdir
        else:
            print "%s is note exists"


    #private helper functions
    @staticmethod
    def createTagCandidate(output):
        result = []
        pattern = re.compile("(\S*)\s*(\d*)\s*(\S*)\s*(.*$)")
        for line in output.split("\n"):
            line = line.strip()
            if line:
                (symbol, lineNumber, filePath, codeSnip) = pattern.search(line).groups()
                iterm = TagIterm(name = symbol, path = filePath, lineNumber = lineNumber, codeSnip = codeSnip)
                result.append(iterm)
        return result

    @staticmethod
    def createFileCandidate(output):
        result = []
        for filePath in output.split("\n"):
            filePath = filePath.strip()
            if filePath:
                fileName = os.path.basename(filePath)
                iterm = FileIterm(name = fileName, path = filePath)
                result.append(iterm)
        return result

    @staticmethod
    def globalCmd(cmd_args):
        cmd = "global %s" % cmd_args
        if GtagsAssist.workdir:
            process = subprocess.Popen(cmd, stdout = subprocess.PIPE, shell = True, cwd = GtagsAssist.workdir)
        else:
            process = subprocess.Popen(cmd, stdout = subprocess.PIPE, shell = True)
        output = process.stdout.read()
        del process
        return output

class GtagsSearchBackend(ItermsFilter):
    def itermPassCheck(self, word, iterm):
        return CommonUtil.fileStrokeMatch(word, iterm.path)
