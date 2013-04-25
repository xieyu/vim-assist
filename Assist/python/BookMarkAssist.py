import os
import vim

from SearchIterm import TagIterm
from Common import CommonUtil
from SettingManager import SettingManager

class BookMarkAssist:
    storeKey = "bookmarks.json"
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
            bookmark = TagIterm(filePath, lineNumber, codeSnip)
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
        SettingManager.editSavedValue(BookMarkAssist.storeKey, "BookMarkAssist.reload()")

    @staticmethod
    def load():
        bookmarks = SettingManager.load(BookMarkAssist.storeKey)
        return [TagIterm.createFromJson(b) for b in bookmarks]

    @staticmethod
    def save(bookmarks):
        SettingManager.save(BookMarkAssist.storeKey, [b.toJson() for b in bookmarks])
