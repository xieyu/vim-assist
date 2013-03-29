import subprocess
import re
import os

from SearchIterm import SearchIterm
from SearchBackend import ItermsFilter
from Common import CommonUtil

class CodeSearchAssist:
    searchDir = None
    storeFileName = "codeSearchHistory"
    searchHistory = None
    #public interface:
    @staticmethod
    def search(symbol):
        symbol = symbol.strip()
        if symbol:
            CodeSearchAssist.addToSearchHistory(CodeSearchHistoryIterm(CodeSearchAssist.searchDir, symbol))
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
                iterm = TagIterm(name = "", path = AgAssist.getFilePath(filePath), lineNumber = str(int(row)+1), codeSnip = codeSnip.strip())
                result.append(iterm)
        return result

    @staticmethod
    def setSearchDir(dir):
        if dir:
            dir = os.path.abspath(dir)
        CodeSearchAssist.searchDir = dir

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

    @staticmethod
    def addToSearchHistory(iterm):
        if CodeSearchAssist.searchHistory is None:
            CodeSearchAssist.searchHistory = CodeSearchAssist.load()

        for i, b in enumerate(CodeSearchAssist.searchHistory):
            if b.equal(iterm):
                del CodeSearchAssist.searchHistory[i]
                break
        CodeSearchAssist.searchHistory.append(iterm)
        CodeSearchAssist.save()

    @staticmethod
    def load():
        storeFilePath = os.path.join(SettingManager.getStoreDir(), CodeSearchAssist.storeFileName)
        result = []
        try:
            f = open(storeFilePath, 'r')
            for line in f.readlines():
                iterm = CodeSearchHistoryIterm.CreateInstancefromString(line.strip())
                if iterm:
                    result.append(iterm)
        except:
            pass
        return result

    @staticmethod
    def save():
        storeFilePath = os.path.join(SettingManager.getStoreDir(), CodeSearchAssist.storeFileName)
        f = open(storeFilePath, 'w')
        for b in CodeSearchAssist.searchHistory:
            f.write("%s\n" % b.toString())
        f.close();
        pass

    @staticmethod
    def getSearchHistory():
        if CodeSearchAssist.searchHistory is None:
            CodeSearchAssist.searchHistory = CodeSearchAssist.load()
        return CodeSearchAssist.searchHistory

class CodeSearchHistoryIterm(SearchIterm):
    def __init__(self, searchDir, symbolName):
        self.searchDir = searchDir
        self.symbolName = symbolName

    def displayText(self):
        if self.searchDir:
            return "%-30s\t%s" %(self.symbolName, self.searchDir)
        else:
            return "%-30s" % (self.symbolName)

    def onAction(self, action):
        old_dir = CodeSearchAssist.searchDir
        if self.searchDir:
            CodeSearchAssist.setSearchDir(self.searchDir)
        vim.eval("CodeSearch('%s')" % self.symbolName)
        CodeSearchAssist.setSearchDir(old_dir)

    def getRankKey(self):
        return symbolName

    @staticmethod
    def CreateInstancefromString(s):
        ret = None
        try:
            pattern = re.compile("(\S*)\s*(.*$)")
            line = s.strip()
            if line:
                (symbolName, searchDir) = pattern.search(line).groups()
                ret = CodeSearchHistoryIterm(searchDir, symbolName)
        except:
            pass
        return ret

    def toString(self):
        return self.displayText()

    def equal(self, iterm):
        return self.searchDir == iterm.searchDir and self.symbolName == iterm.symbolName

class CodeSearchHistoryBackend(ItermsFilter):
    def itermPassCheck(self, word, iterm):
        return word in iterm.symbolName

