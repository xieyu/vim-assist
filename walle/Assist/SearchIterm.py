import os
import vim
#intereface for searchIterm
class SearchIterm:
    def displayText(self):
        return ""

    def onAction(self, action):
        return True

class FileIterm(SearchIterm):
    def __init__(self, name, path):
        self.name = name
        self.path = path

    def displayText(self):
        return "%-40s\t%s"%(self.name, self.path)

    def onAction(self, action):
        curwin = vim.eval("winnr()")
        wid = vim.eval("VimUtils#firstUsableWindow()")
        vim.command("%s wincmd w" % wid) #try next window
        vim.command("silent e %s" % self.path)
        #jump back to result window if preview
        if action =="preview":
            vim.command("%s wincmd w" % curwin)
            return False
        return True


class TagItem(FileIterm):
    def __init__(self, name, path, lineNumber, codeSnip):
        FileCandidate.__init__(self, name, path)
        self.lineNumber = lineNumber
        self.codeSnip = codeSnip

    def displayText(self):
        return "%-30s\t%-10s\t%-50s"%(os.path.basename(self.path), self.lineNumber, self.codeSnip)

    def onAction(self, action):
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
        return True
