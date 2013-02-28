import os
import vim

from SearchIterm import TagIterm
from Common import CommonUtil
from Common import SettingManager
from VimUi import ItermsFilter

class BookMarkAssist:
    dbKey = "BookMarkAssist"
    @staticmethod
    def getBookMarkIterms():
        return SettingManager.get(BookMarkAssist.dbKey)

    @staticmethod
    def addCurrentCursorToBookmark():
        filePath = vim.current.buffer.name
        if filePath:
            row, col = vim.current.window.cursor
            lineNumber = row
            codeSnip = vim.current.buffer[row - 1]
            fileName = os.path.basename(filePath)
            bookmark = TagIterm(fileName, filePath, lineNumber, codeSnip)
            BookMarkAssist.add(bookmark)

    @staticmethod
    def add(tagIterm):
        bookmarks = SettingManager.get(BookMarkAssist.dbKey)
        for b in bookmarks:
            if b.equal(tagIterm):
                return
        bookmarks.append(tagIterm)
        SettingManager.save(BookMarkAssist.dbKey, bookmarks)

    @staticmethod
    def clear():
        SettingManager.save(BookMarkAssist.dbKey, [])

    @staticmethod
    def edit():
        vim.command("autocmd BufWritePost <buffer> py BookMarkAssist.reload()")
        pass

    @staticmethod
    def reload():
        pass

    @staticmethod
    def dump(filePath):
        pass


class BookMarkSearchBackend(ItermsFilter):
    def itermPassCheck(self, word, iterm):
        symbols = word.split("@")
        if len(symbols) == 1:
            return CommonUtil.fileStrokeMatch(symbols[0], iterm.path)
        elif len(symbols) == 2:
            passFlag = True
            if symbols[0] is not "":
                passFlag = CommonUtil.fileStrokeMatch(symbols[0], iterm.path)
            if passFlag and symbols[1] is not "":
                passFlag = CommonUtil.strokeMatch(symbols[1], iterm.codeSnip)
            return passFlag
        return True

