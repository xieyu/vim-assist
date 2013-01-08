import os
import vim
from Assist.VimUi import ControllerFactory

class FileCandidate:
    def __init__(self, name, path):
        self.name = name
        self.path = path

    def getPath(self):
        return self.path

    def getName(self):
        return self.name

    def getKey(self):
        return os.path.normpath(self.path)

    def getDisplayName(self):
        return "%-40s\t%s"%(self.name, self.path)

class TagCandidate(FileCandidate):
    def __init__(self, name, path, lineNumber, codeSnip):
        FileCandidate.__init__(self, name, path)
        self.lineNumber = lineNumber
        self.codeSnip = codeSnip

    def getLineNumber(self):
        return int(self.lineNumber)

    def getKey(self):
        return self.path+self.lineNumber

    def getDisplayName(self):
        return "%-30s\t%-10s\t%-50s"%(os.path.basename(self.path), self.lineNumber, self.codeSnip)

class CommandCandidate:
    def __init__(self, cmd, needArgs, isVimCommnd):
        self.cmdName = cmd
        self.needArgs = needArgs
        self.isVimCommnd = isVimCommnd

    def getDisplayName(self):
        return self.cmdName

class CandidateManager:
    hotSearchCb = None
    @staticmethod
    def display(result, emptyMessage="find nothing :)"):
        CandidateManager.lastWinnr = vim.eval("winnr()")
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
    def hotSearch(callbacker):
        CandidateManager.lastWinnr = vim.eval("winnr()")
        CandidateManager.hotSearchCallbacker = callbacker
        matcher = ControllerFactory.getPromptMatchController(title ="command", candidateManager = CandidateManager)
        matcher.run()

    @staticmethod
    def search(pattern):
        if CandidateManager.hotSearchCallbacker:
            return CandidateManager.hotSearchCallbacker.search(pattern)
        return []
        

    #call back function for vimui controller
    @staticmethod
    def getKeysMap():
        return {"<cr>":"close","<2-LeftMouse>":"keep","<c-o>":"keep", "<c-p>": "preview"}

    @staticmethod
    def accept(candidate, way="edit"):
        curwin = vim.eval("winnr()")
        if isinstance(candidate, FileCandidate):
            wId = vim.eval("VimUtils#firstUsableWindow()")
            vim.command("%s wincmd w"%wId) #try next window
            vim.command("silent e %s"%candidate.getPath())

        if isinstance(candidate, TagCandidate):
            lineNumber = candidate.getLineNumber()
            vim.command("%d"%lineNumber)
            vim.command("normal z.")

        if way != "autoPreview" and isinstance(candidate, CommandCandidate):
            vim.command("%s wincmd w"%CandidateManager.lastWinnr)
            if candidate.isVimCommnd:
                if not candidate.needArgs:
                    vim.command(candidate.cmdName)
                else:
                    args = vim.eval('input("%s ")'%candidate.cmdName)
                    vim.command("%s %s"%(candidate.cmdName, args.strip()))

        if way =="preview" or way == "autoPreview":
            vim.command("%s wincmd w"%curwin)
