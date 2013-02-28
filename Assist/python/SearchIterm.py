import os
import vim
#intereface for searchIterm
class SearchIterm(object):
    def displayText(self):
        return ""

    def onAction(self, action):
        return True

    def equal(self, iterm):
        return True

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
        return self.name is iterm.name and self.path is iterm.path


class TagIterm(FileIterm):
    def __init__(self, name, path, lineNumber, codeSnip):
        super(TagIterm, self).__init__(name, path)
        self.lineNumber = lineNumber
        self.codeSnip = codeSnip

    def displayText(self):
        return "%-30s\t%-10s\t%-50s"%(os.path.basename(self.path), self.lineNumber, self.codeSnip)

    def onAction(self, action):
        if action == "yank":
            vim.command('let @@="%s"' % self.name)
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
            return self.lineNumber is iterm.lineNumer and self.codeSnip is iterm.codeSnip
        return False
