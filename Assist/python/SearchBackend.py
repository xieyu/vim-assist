
class SearchBackend:
    def search(self, word):
        return []

    def getKeyActionMaps(self):
        return [("<cr>","close"),("<2-LeftMouse>","preview"),("<c-o>","preview"), ("<c-p>", "preview"), ("<c-y>", "yank")]

    def handle(self, action, iterm):
        return iterm.onAction(action)

    def getInitDisplayIterms(self):
        return []

class DisplayBackend:
    def getDisplayIterms(self):
        return []

    def getKeyActionMaps(self):
        return [("<cr>","close"),("<2-LeftMouse>","preview"),("<c-o>","preview"), ("<c-p>", "preview"), ("<c-y>", "yank")]

    def handle(self, action, iterm):
        return iterm.onAction(action)

class ItermsDisplayer(DisplayBackend):
    def __init__(self, iterms):
        self.iterms = iterms

    def getDisplayIterms(self):
        return self.iterms

class ItermsFilter(SearchBackend):
    def __init__(self, iterms):
        self.iterms = iterms

    def getInitDisplayIterms(self):
        return self.iterms

    def search(self, word):
        result = [iterm for iterm in self.iterms if self.itermPassCheck(word, iterm)]
        if len(result) < 1000:
            result = sorted(result, cmp=self.itermRank)
        return result

    def itermPassCheck(self, world, iterm):
        return True

    def itermRank(self, iterm1, iterm2):
        return len(iterm1.getRankKey()) - len(iterm2.getRankKey())


class FileSearchBackend(ItermsFilter):
    def itermPassCheck(self, word, iterm):
        return CommonUtil.fileStrokeMatch(word, iterm.path)

class TagSearchBackend(ItermsFilter):
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

