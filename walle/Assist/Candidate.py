import os
import vim
from Assist.VimUi import ControllerFactory

class FileCandidate:
    def __init__(self, name, path):
        self.name = name
        self.path = path

    def displayText(self):
        return "%-40s\t%s"%(self.name, self.path)

    def accept(self, way="edit"):
        curwin = vim.eval("winnr()")
        wid = vim.eval("VimUtils#firstUsableWindow()")
        vim.command("%s wincmd w" % wid) #try next window
        vim.command("silent e %s" % self.path)
        #jump back to result window if preview
        if way =="preview" or way == "autoPreview":
            vim.command("%s wincmd w" % curwin)


class TagCandidate(FileCandidate):
    def __init__(self, name, path, lineNumber, codeSnip):
        FileCandidate.__init__(self, name, path)
        self.lineNumber = lineNumber
        self.codeSnip = codeSnip

    def displayText(self):
        return "%-30s\t%-10s\t%-50s"%(os.path.basename(self.path), self.lineNumber, self.codeSnip)

    def accept(self, way):
        curwin = vim.eval("winnr()")
        wid = vim.eval("VimUtils#firstUsableWindow()")
        vim.command("%s wincmd w" % wid) #try next window
        vim.command("silent e %s"%self.path)
        vim.command("%d" % int(self.lineNumber))
        vim.command("normal z.")
        #jump back to result window if preview
        if way =="preview" or way == "autoPreview":
            vim.command("%s wincmd w"%curwin)



class CandidateManager:
    searchHotCallbacker = None
    @staticmethod
    def display(result, emptyMessage="find nothing :)"):
        if  not result or len(result) == 0:
            print emptyMessage
            return
        displayer = ControllerFactory.getDisplayController("search-result", CandidateManager)
        if(len(result)==1):
            CandidateManager.accept(result[0])
            vim.command("redraw")
        else:
            displayer.show(result)
        pass


    @staticmethod
    def searchHot(callbacker):
        CandidateManager.searchHotCallbacker = callbacker
        matcher = ControllerFactory.getPromptMatchController(title ="search-Hot", candidateManager = CandidateManager)
        matcher.run()


    #call back function for vimui controller
    @staticmethod
    def search(pattern):
        if CandidateManager.searchHotCallbacker:
            return CandidateManager.searchHotCallbacker.search(pattern)
        return []

    @staticmethod
    def getKeysMap():
        return {"<cr>":"close","<2-LeftMouse>":"keep","<c-o>":"keep", "<c-p>": "preview"}

    @staticmethod
    def shouldClose(way):
        return way is "close"

    @staticmethod
    def accept(candidate, way="edit"):
        candidate.accept(way)
