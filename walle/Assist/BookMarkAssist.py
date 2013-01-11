import os
import vim
from Assist.Candidate import FileCandidate 
from Assist.Candidate import CandidateManager
from Assist.CommonUtil import CommonUtil
from Assist.CommonUtil import SettingManager

#TODO:FIXIT, remove the ugly code
from Assist.VimUi import ControllerFactory

class BookMarkCandidate:
    def __init__(self, symbol, filePath, lineNum, codeSnip):
        pass

    def displayText(self):
        return "%-30s\t%-60s" % (self.symbol, self.filePath)

    def equal(self, a):
        return self.filePath  == a.filePath and self.lineNum == a.lineNum and self.symbol == a.symbol

    def accept(self, way):
        curwin = vim.eval("winnr()")
        wid = vim.eval("VimUtils#firstUsableWindow()")
        vim.command("%s wincmd w" % wid) #try next window
        vim.command("silent e %s" % self.path)
        #jump back to result window if preview
        if way =="preview" or way == "autoPreview":
            vim.command("%s wincmd w" % curwin)

class BookMarkAssist:
    bookmarks = None
    dbKey = "BookMarkAssist"
    @staticmethod
    def searchHot():
        BookMarkAssist.recentFiles = SettingManager.get(BookMarkAssist.dbKey)
        if BookMarkAssist.recentFiles is []:
            print "recent history is none"
        CandidateManager.searchHot(BookMarkAssist.SearchHotCallbacker)

    class SearchHotCallbacker:
        @staticmethod
        def search(pattern):
            result = []
            for filePath in BookMarkAssist.recentFiles:
                if CommonUtil.strokeMatch(pattern, filePath):
                    fileName = os.path.basename(filePath)
                    result.append(FileCandidate(fileName, filePath))
            return result

    @staticmethod
    def add(symbol):
        filePath = vim.current.buffer.name
        bookmarks = SettingManager.get(BookMarkAssist.dbKey)
        tmpBookMark = BookMarkCandidate(symbol, filePath, lineNum, codeSnip)
        for b in bookmarks:
            if b.equal(tmpBookMark):
                return
        bookmarks.append(tmpBookMark)
        SettingManager.save(BookMarkAssist.dbKey, bookmarks)

    @staticmethod
    def clear():
        SettingManager.save(BookMarkAssist.dbKey, [])

    @staticmethod
    def edit():
        BookMarkAssist.tmpfile = SettingManager.tmpfile("bookmarks")
        BookMarkAssist.dump(BookMarkAssist.tmpfile)
        vim.command("sp %s"% BookMarkAssist.tmpfile)
        vim.command("autocmd BufWritePost <buffer> py BookMarkAssist.reload()")

    @staticmethod
    def reload():
        f = open(BookMarkAssist.tmpfile, 'r')
        result = []
        for line in f.readlines():
            result.append(line.strip())
        SettingManager.save(BookMarkAssist.dbKey, result)

    @staticmethod
    def dump(filePath):
        f = open(filePath, 'w')
        bookmarks = SettingManager.get(BookMarkAssist.dbKey)
        for filePath in rfiles:
            f.write("%s\n" % filePath)
        f.close();
        pass


