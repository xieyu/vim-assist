import subprocess
import re
import os
import shelve

from Assist.Candidate import FileCandidate
from Assist.Candidate import TagCandidate
from Assist.Candidate import CandidateManager
from Assist.CommonUtil import SettingManager

class GtagsAssist:
    workdir=None
    #public interface:
    @staticmethod
    def searchSymbolRef(symbol):
        symbol = symbol.strip()
        output = GtagsAssist.globalCmd("-axr %s" % symbol)
        GtagsHistory.add("refer", symbol)
        CandidateManager.display(GtagsAssist.createTagCandidate(output))

    @staticmethod
    def searchSymbolDefine(symbol):
        symbol= symbol.strip()
        output = GtagsAssist.globalCmd("-ax %s" % symbol)
        GtagsHistory.add("define", symbol)
        CandidateManager.display(GtagsAssist.createTagCandidate(output))

    @staticmethod
    def searchFile(symbol):
        GtagsHistory.add("file", symbol)
        name = name.strip()
        output = GtagsAssist.globalCmd("-Pai %s" % name)
        CandidateManager.display(GtagsAssist.createFileCandidate(output))

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
                iterm = TagCandidate(name = symbol, path = filePath, lineNumber = lineNumber, codeSnip = codeSnip)
                result.append(iterm)
        return result

    @staticmethod
    def createFileCandidate(output):
        result = []
        for filePath in output.split("\n"):
            filePath = filePath.strip()
            if filePath:
                fileName = os.path.basename(filePath)
                iterm = FileCandidate(name = fileName, path = filePath)
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


#gtags history assist
class GtagHistoryCandidate:
    def __init__(self, searchType, symbol, workdir):
        self.searchType = searchType
        self.symbol = symbol
        self.workdir = workdir

    def displayText(self):
        return "%-20s%-50s%s"%(self.searchType, self.symbol, self.workdir)

    def accept(self, way):
        GtagsHistory.replay(self)

    def equal(self, a):
        return self.searchType == a.searchType and self.symbol == a.symbol and self.workdir == a.workdir


class GtagsHistory:
    historySet = None
    dbKey = "GtagsHistory"
    @staticmethod
    def searchHot():
        GtagsHistory.historySet = SettingManager.get(GtagsHistory.dbKey)
        CandidateManager.searchHot(GtagsHistory.SearchHotCallbacker)

    @staticmethod
    def replay(h):
        print "replay the history %s , %s, %s" %(h.searchType, h.workdir, h.symbol)
        oldWorkdir = GtagsAssist.workdir
        GtagsAssist.workdir = h.workdir
        if h.searchType == "define":
            GtagsAssist.searchSymbolDefine(h.symbol)
        elif h.searchType == "refer":
            GtagsAssist.searchSymbolRef(h.symbol)
        elif h.searchType == "file":
            GtagsAssist.searchFile(h.symbol)
        GtagsAssist.workdir = oldWorkdir

    class SearchHotCallbacker:
        @staticmethod
        def search(pattern):
            return [iterm for iterm in GtagsHistory.historySet if CommonUtil.strokeMatch(pattern, iterm.symbol)]

    @staticmethod
    def add(searchType, symbol):
        workdir = GtagsAssist.workdir or os.getcwd()
        t = GtagHistoryCandidate(searchType, symbol, workdir)
        historySet = SettingManager.get(GtagsHistory.dbKey)
        for item in historySet:
            if item.equal(t):
                return
        historySet.append(t)
        SettingManager.save(GtagsHistory.dbKey, historySet)

    @staticmethod
    def clear():
        SettingManager.save(GtagsHistory.dbKey, [])

    @staticmethod
    def edit():
        GtagsHistory.tmpfile = SettingManager.tmpfile("gtagsHistory")
        GtagsHistory.dump(GtagsHistory.tmpfile)
        vim.command("sp %s"% GtagsHistory.tmpfile)
        vim.command("autocmd BufWritePost <buffer> py GtagsHistory.reload()")

    @staticmethod
    def reload():
        f = open(GtagsHistory.tmpfile, 'r')
        result = []
        pattern = re.compile("(\S*)\s*(\S*)\s*(\S*)\s*")
        for line in f.readlines():
            line = line.strip()
            if line:
                searchType, symbol, workdir = pattern.search(line).groups()
                result.append(GtagHistoryCandidate(searchType, symbol, workdir))
        SettingManager.save(GtagsHistory.dbKey, result)

    @staticmethod
    def dump(filePath):
        f = open(filePath, 'w')
        historySet = SettingManager.get(GtagsHistory.dbKey)
        for iterm in historySet:
            f.write("%-30s\t %-60s\t %s\n" % (iterm.searchType, iterm.symbol, iterm.workdir))
        f.close();
        pass


