import os
import vim
import re
#intereface for searchIterm
class SearchIterm(object):
    def displayText(self):
        return ""

    def onAction(self, action):
        return True

    def equal(self, iterm):
        return True

    def getRankKey(self, iterm):
        return ""

class FileIterm(SearchIterm):
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

    def __eq__(self, iterm):
        return self.path == iterm.path

    def getPath(self):
        return self.path


class TagIterm(FileIterm):
    def __init__(self, path, lineNumber, codeSnip):
        super(TagIterm, self).__init__(path)
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

    def equal(self, iterm):
        if super(TagIterm, self).equal(iterm):
            return self.lineNumber == iterm.lineNumber and self.codeSnip == iterm.codeSnip
        return False

    @staticmethod
    def createFromJson(js):
        return TagIterm(path = str(js["path"]), lineNumber = str(js["lineNumber"]), codeSnip = str(js["codeSnip"]))

    def toJson(self):
        return {"path": self.path, "lineNumber": self.lineNumber, "codeSnip": self.codeSnip}

class CtagIterm(TagIterm):
    def __init__(self, symbol, path, lineNumber, codeSnip, symbolType):
        super(CtagIterm, self).__init__(path, lineNumber, codeSnip)
        self.symbolType = symbolType
        self.symbol = symbol

    def displayText(self):
        return "%-30s\t%-20s\t%-10s\t%-50s"%(self.symbol, self.symbolType, self.lineNumber, self.codeSnip)

