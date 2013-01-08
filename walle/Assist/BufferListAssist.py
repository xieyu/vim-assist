import os
import vim
from Assist.Candidate import FileCandidate 
from Assist.Candidate import CandidateManager
from Assist.CommonUtil import CommonUtil

#TODO:FIXIT, remove the ugly code
from Assist.VimUi import ControllerFactory

class BufferListAssist:
    walle_home = vim.eval("g:walle_home")
    configFile= os.path.join(walle_home, "config/recentFiles")

    @staticmethod
    def prepare():
        BufferListAssist.filePaths = [buf.name for buf in vim.buffers if buf.name and os.path.exists(buf.name)]

    @staticmethod
    def searchHot():
        BufferListAssist.prepare()
        CandidateManager.hotSearch(BufferListAssist.HotSearchCallbacker)

    @staticmethod
    def search(pattern):
        BufferListAssist.prepare()
        result = BufferListAssist.hotSearchCallbacker.search(pattern)
        CandidateManager.display(result)

    class HotSearchCallbacker:
        @staticmethod
        def search(pattern):
            result = []
            for filePath in BufferListAssist.filePaths:
                if CommonUtil.fileStrokeMatch(pattern, filePath):
                    fileName = os.path.basename(filePath)
                    result.append(FileCandidate(fileName, filePath))
            return result
