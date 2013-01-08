import subprocess
import re
from Assist.Candidate import FileCandidate
from Assist.Candidate import TagCandidate
from Assist.Candidate import CandidateManager
import os

class GtagsAssist:
    #public interface:
    @staticmethod
    def searchSymbolRef(symbol):
        symbol = symbol.strip()
        output = GtagsAssist.globalCmd(["-axr", symbol])
        CandidateManager.display(GtagsAssist.createTagCandidate(output))

    @staticmethod
    def searchSymbolDefine(symbol):
        symbol= symbol.strip()
        output = GtagsAssist.globalCmd(["-ax", symbol])
        CandidateManager.display(GtagsAssist.createTagCandidate(output))

    @staticmethod
    def searchFile(name):
        name = name.strip()
        output = GtagsAssist.globalCmd(["-Pai", name])
        CandidateManager.display(GtagsAssist.createFileCandidate(output))


    #private helper functions
    @staticmethod
    def createTagCandidate(output):
        result = []
        pattern = re.compile("(\S*)\s*(\d*)\s*(\S*)\s*(.*$)")
        for line in output.split("\n"):
            line = line.strip()
            if line:
                (symbol, lineNumber, filePath, codeSnip) = pattern.search(line).groups()
                iterm = TagCandidate(name = symbol, path = filePath, lineNumber = lineNumber, codeSnip = codeSnip)
                result.append(iterm)
        return result

    @staticmethod
    def createFileCandidate(output):
        result = []
        for filePath in output.split("\n"):
            filePath = filePath.strip()
            if filePath:
                fileName = os.path.basename(filePath)
                iterm = FileCandidate(name = fileName, path = filePath)
                result.append(iterm)
        return result

    @staticmethod
    def globalCmd(cmd_args):
        cmd = ["global"] + cmd_args
        output = subprocess.check_output(cmd)
        return output
