import os
import vim
import re
#intereface for candidate 
class Candidate(object):
    def displayText(self):
        return ""

    def onAction(self, action):
        return True

class FileCandidate(Candidate):
    def __init__(self, path):
        self.path = path

    def displayText(self):
        return "%-40s\t%s"%(os.path.basename(self.path), self.path)

    def onAction(self, action):
        if action == "yank":
            vim.command('let @@="%s"' % self.path)
            vim.command('let @+="%s"' % self.path)
            print "on line has been yanked"
            return False

        curwin = vim.eval("winnr()")
        wid = vim.eval("VimUtils#firstUsableWindow()")
        vim.command("%s wincmd w" % wid) #try next window
        vim.command("silent e %s" % self.path)
        #jump back to result window if preview or close
        if action =="preview":
            vim.command("%s wincmd w" % curwin)
            return False

        if action == "close":
            vim.command("%s wincmd w"%curwin)
        return True

    def __eq__(self, candidate):
        return self.path == candidate.path

    def getPath(self):
        return self.path


class TagCandidate(FileCandidate):
    def __init__(self, path, lineNumber, codeSnip):
        super(TagCandidate, self).__init__(path)
        self.lineNumber = lineNumber
        self.codeSnip = codeSnip

    def displayText(self):
        return "%-30s\t%-10s\t%-50s"%(os.path.basename(self.path), self.lineNumber, self.codeSnip)

    def onAction(self, action):
        if action == "yank":
            vim.command('let @@="%s:%s"' % (self.path, self.lineNumber))
            vim.command('let @+="%s"' % self.name)
            print "on line has been yanked"
            return False

        curwin = vim.eval("winnr()")
        wid = vim.eval("VimUtils#firstUsableWindow()")
        vim.command("%s wincmd w" % wid) #try next window
        vim.command("silent e %s"%self.path)
        vim.command("%d" % int(self.lineNumber))
        vim.command("normal z.")
        #jump back to result window if preview
        if action =="preview":
            vim.command("%s wincmd w"%curwin)
            return False
        if action == "close":
            vim.command("%s wincmd w"%curwin)
        return True

    def __eq__(self, other):
        if super(TagCandidate, self).equal(other):
            return self.lineNumber == other.lineNumber and self.codeSnip == other.codeSnip
        return False

    @staticmethod
    def createFromJson(js):
        return TagCandidate(path = str(js["path"]), lineNumber = str(js["lineNumber"]), codeSnip = str(js["codeSnip"]))

    def toJson(self):
        return {"path": self.path, "lineNumber": self.lineNumber, "codeSnip": self.codeSnip}

class CtagCandidate(TagCandidate):
    def __init__(self, symbol, path, lineNumber, codeSnip, symbolType):
        super(CtagCandidate, self).__init__(path, lineNumber, codeSnip)
        self.symbolType = symbolType
        self.symbol = symbol

    def displayText(self):
        return "%-30s\t%-20s\t%-10s\t%-50s"%(self.symbol, self.symbolType, self.lineNumber, self.codeSnip)

def filterCheck(word, candidate):
    if isinstance(candidate, FileCandidate):
        return fileCandidateFilterCheck(word, candidate)
    elif isinstance(candidate, TagCandidate):
        return tagCandidateFilterCheck(word, candidate)
    return True

def fileCandidateFilterCheck(word, candidate):
    return CommonUtil.fileMatch(word, Candidate.path)

def tagCandidateFilterCheck(word, candidate):
    symbols = word.split("@")
    if len(symbols) == 1:
        return CommonUtil.fileMatch(symbols[0], Candidate.path)
    elif len(symbols) == 2:
        passFlag = True
        if symbols[0] is not "":
            passFlag = CommonUtil.fileMatch(symbols[0], Candidate.path)
        if passFlag and symbols[1] is not "":
            passFlag = CommonUtil.wordMatch(symbols[1], Candidate.codeSnip)
        return passFlag
    return True
