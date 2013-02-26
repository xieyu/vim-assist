import os
import vim
from SearchIterm import FileIterm
from Common import CommonUtil
from Common import SettingManager

from VimUi import SearchWindow
from VimUi import SearchBackend

class HistoryAssist(SearchBackend):
    recentFiles = None
    dbKey = "HistoryAssist"
    def __init__(self):
        self.recentFiles = SettingManager.get(HistoryAssist.dbKey)
        if self.recentFiles is []:
            print "recent history is none"

    def search(self, pattern):
        result = []
        for filePath in self.recentFiles:
            if filePath and CommonUtil.fileStrokeMatch(pattern, filePath):
                fileName = os.path.basename(filePath)
                result.append(FileIterm(fileName, filePath))
        return result

    @staticmethod
    def add():
        filePath = vim.current.buffer.name
        rfiles = SettingManager.get(HistoryAssist.dbKey)
        if filePath in rfiles or not os.path.exists(filePath):
            return
        rfiles.append(filePath)
        SettingManager.save(HistoryAssist.dbKey, rfiles)

    @staticmethod
    def clear():
        SettingManager.save(HistoryAssist.dbKey, [])

    @staticmethod
    def edit():
        HistoryAssist.tmpfile = SettingManager.tmpfile("history")
        HistoryAssist.dump(HistoryAssist.tmpfile)
        vim.command("sp %s"% HistoryAssist.tmpfile)
        vim.command("autocmd BufWritePost <buffer> py HistoryAssist.reload()")

    @staticmethod
    def reload():
        f = open(HistoryAssist.tmpfile, 'r')
        result = []
        for line in f.readlines():
            result.append(line.strip())
        SettingManager.save(HistoryAssist.dbKey, result)

    @staticmethod
    def dump(filePath):
        f = open(filePath, 'w')
        rfiles = SettingManager.get(HistoryAssist.dbKey)
        for filePath in rfiles:
            f.write("%s\n" % filePath)
        f.close();
        pass


