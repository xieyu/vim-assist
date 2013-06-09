import VimUi
from Common import CommonUtil
from Candidate import FileCandidate
from Candidate import TagCandidate
from Candidate import CtagCandidate


def filterCheck(word, candidate):
    if isinstance(candidate, TagCandidate):
        return tagCandidateFilterCheck(word, candidate)
    elif isinstance(candidate, FileCandidate):
        return fileCandidateFilterCheck(word, candidate)
    return True

def fileCandidateFilterCheck(word, candidate):
    return CommonUtil.fileMatch(word, candidate.path)

def tagCandidateFilterCheck(word, candidate):
    symbols = word.split("@")
    if len(symbols) == 1:
        return CommonUtil.fileMatch(symbols[0], candidate.path)
    elif len(symbols) == 2:
        passFlag = True
        if symbols[0] is not "":
            passFlag = CommonUtil.fileMatch(symbols[0], candidate.path)
        if passFlag and symbols[1] is not "":
            passFlag = CommonUtil.wordMatch(symbols[1], candidate.codeSnip)
        return passFlag
    return True

def showSearchResult(candidates, filterCheck=filterCheck):
    backend = CandidatesFilter(candidates, filterCheck)
    displayWindow = VimUi.SearchWindow(backend)
    displayWindow.show()


class SearchBackend(object):
    def search(self, word):
        return []

    def getKeyActionMaps(self):
        return [("<cr>","close"),("<2-LeftMouse>","preview"),("<c-o>","preview"), ("<c-p>", "preview"), ("<c-y>", "yank")]

    def handle(self, action, Candidate):
        return Candidate.onAction(action)

    def getInitDisplayCandidates(self):
        return []

    def prepare(self):
        pass

class CandidatesFilter(SearchBackend):
    def __init__(self, Candidates, filterCheck, limit = 50):
        self.Candidates = Candidates
        self.limit = limit
        self.filterCheck = filterCheck

    def getInitDisplayCandidates(self):
        return self.Candidates

    def search(self, word):
        count = 0
        result = []
        for Candidate in self.Candidates:
            if self.filterCheck is None or self.filterCheck(word, Candidate):
                count = count + 1
                if count > self.limit:
                    break
                result.append(Candidate)
        return result
