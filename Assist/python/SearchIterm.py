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
    def __init__(self, name, path):
        self.name = name
        self.path = path

    def displayText(self):
        return "%-40s\t%s"%(self.name, self.path)

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

    def equal(self, iterm):
        return self.name == iterm.name and self.path == iterm.path

    def getRankKey(self):
        return self.name


class TagIterm(FileIterm):
    def __init__(self, name, path, lineNumber, codeSnip):
        super(TagIterm, self).__init__(name, path)
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
    def CreateInstancefromString(s):
        ret = None
        try:
            pattern = re.compile("(\S*)\s*(\S*)\s*(.*$)")
            line = s.strip()
            if line:
                (filePath, lineNumber, codeSnip) = pattern.search(line).groups()
                ret  = TagIterm(name = os.path.basename(filePath), path = filePath, lineNumber = lineNumber, codeSnip = codeSnip)
        except:
            pass
        return ret


    def toString(self):
        return "%s %s %s" %(self.path, self.lineNumber, self.codeSnip)

class CtagIterm(TagIterm):
    def __init__(self, name, path, lineNumber, codeSnip, symbolType):
        super(CtagIterm, self).__init__(name, path, lineNumber, codeSnip)
        self.symbolType = symbolType

    def displayText(self):
        return "%-30s\t%-20s\t%-10s\t%-50s"%(self.name, self.symbolType, self.lineNumber, self.codeSnip)
