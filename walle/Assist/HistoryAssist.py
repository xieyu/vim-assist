import os
import vim
from Assist.Candidate import FileCandidate 
from Assist.Candidate import CandidateManager
from Assist.CommonUtil import CommonUtil
from Assist.CommonUtil import SettingManager

#TODO:FIXIT, remove the ugly code
from Assist.VimUi import ControllerFactory

class HistoryAssist:
    recentFiles = None
    dbKey = "HistoryAssist"
    @staticmethod
    def searchHot():
        HistoryAssist.recentFiles = SettingManager.get(HistoryAssist.dbKey)
        if HistoryAssist.recentFiles is []:
            print "recent history is none"
        CandidateManager.searchHot(HistoryAssist.SearchHotCallbacker)

    class SearchHotCallbacker:
        @staticmethod
        def search(pattern):
            result = []
            for filePath in HistoryAssist.recentFiles:
                if CommonUtil.strokeMatch(pattern, filePath):
                    fileName = os.path.basename(filePath)
                    result.append(FileCandidate(fileName, filePath))
            return result

    @staticmethod
    def add():
        filePath = vim.current.buffer.name
        rfiles = SettingManager.get(HistoryAssist.dbKey)
        if filePath in rfiles:
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


