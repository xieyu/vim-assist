import os
import vim
from Assist.Candidate import FileCandidate 
from Assist.Candidate import CandidateManager
from Assist.CommonUtil import CommonUtil

#TODO:FIXIT, remove the ugly code
from Assist.VimUi import ControllerFactory

class HistoryAssist:
    walle_home = vim.eval("g:walle_home")
    configFile= os.path.join(walle_home, "config/recentFiles")

    @staticmethod
    def prepare():
        try:
            HistoryAssist.recentFileCollection = [line.strip() for line in open(HistoryAssist.configFile).readlines()]
            HistoryAssist.recentFileCollection.reverse()
        except:
            HistoryAssist.recentFileCollection = []
            print "history is empty"

    @staticmethod
    def searchHot():
        HistoryAssist.prepare()
        CandidateManager.hotSearch(HistoryAssist.HotSearchCallbacker)

    @staticmethod
    def search(pattern):
        HistoryAssist.prepare()
        result = HistoryAssist.hotSearchCallbacker.search(pattern)
        CandidateManager.display(result)

    class HotSearchCallbacker:
        @staticmethod
        def search(pattern):
            result = []
            for filePath in HistoryAssist.recentFileCollection:
                if CommonUtil.fileStrokeMatch(pattern, filePath):
                    fileName = os.path.basename(filePath)
                    result.append(FileCandidate(fileName, filePath))
            return result

    @staticmethod
    def addToHistory():
        filePath = vim.current.buffer.name
        try:
            if filePath and os.path.exists(filePath):
                configFile = HistoryAssist.configFile
                try:
                    recentFiles = [line.strip() for line in open(configFile).readlines()]
                except:
                    recentFiles = []

                if filePath in recentFiles:
                    return
                recentFiles.append(filePath)

                if not os.path.exists(os.path.dirname(configFile)):
                    os.mkdir(os.path.dirname(configFile))

                if os.path.isfile(configFile):
                    os.remove(configFile)

                file =open(configFile, "w")
                for filePath in recentFiles:
                    if os.path.exists(filePath):
                        file.write(filePath)
                        file.write('\n')
                file.close()
        except:
            print "fail to add it to history"
            pass
