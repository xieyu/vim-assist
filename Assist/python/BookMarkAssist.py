import os
import vim

from SearchIterm import TagIterm
from Common import CommonUtil
from Common import SettingManager

class BookMarkAssist:
    storeFileName = "BookMarks"
    bookMarks = None
    @staticmethod
    def getBookMarkIterms():
        bookMarks = BookMarkAssist.load()
        bookMarks.reverse()
        return bookMarks

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
        if BookMarkAssist.bookMarks is None:
            BookMarkAssist.bookMarks = BookMarkAssist.load()

        for i, b in enumerate(BookMarkAssist.bookMarks):
            if b.equal(tagIterm):
                del BookMarkAssist.bookMarks[i]
                break
        BookMarkAssist.bookMarks.append(tagIterm)
        BookMarkAssist.save(BookMarkAssist.bookMarks)

    @staticmethod
    def reload():
        BookMarkAssist.bookMarks= BookMarkAssist.load()

    @staticmethod
    def edit():
        storeFilePath = os.path.join(SettingManager.getStoreDir(), BookMarkAssist.storeFileName)
        vim.command("sp %s"% storeFilePath)
        vim.command("autocmd BufWritePost <buffer> py BookMarkAssist.reload()")

    @staticmethod
    def load():
        storeFilePath = os.path.join(SettingManager.getStoreDir(), BookMarkAssist.storeFileName)
        result = []
        f = open(storeFilePath, 'r')
        for line in f.readlines():
            iterm = TagIterm.CreateInstancefromString(line.strip())
            if iterm:
                result.append(iterm)
        return result

    @staticmethod
    def save(filesList):
        storeFilePath = os.path.join(SettingManager.getStoreDir(), BookMarkAssist.storeFileName)
        f = open(storeFilePath, 'w')
        for b in BookMarkAssist.bookMarks:
            f.write("%s\n" % b.toString())
        f.close();
        pass


