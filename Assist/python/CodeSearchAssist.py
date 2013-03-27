import subprocess
import re
import os

from SearchIterm import TagIterm
from Common import CommonUtil

class CodeSearchAssist:
    searchDir = None
    storeFileName = "codeSearchHistory"
    searchHistory = None
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

    @staticmethod
    def addToSearchHistory(iterm):
        if CodeSearchAssist.searchHistory is None:
            CodeSearchAssist.searchHistory = CodeSearchAssist.load()

        for i, b in enumerate(CodeSearchAssist.searchHistory):
            if b.equal(iterm):
                del CodeSearchAssist.searchHistoryi]
                break
        CodeSearchAssist.searchHistory.append(iterm)
        CodeSearchAssist.save()

    @staticmethod
    def load():
        storeFilePath = os.path.join(SettingManager.getStoreDir(), CodeSearchAssist.storeFileName)
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
        pass

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
        return True

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

    def toString(self):
        return self.displayText

    def equal(self, iterm):
        pass

