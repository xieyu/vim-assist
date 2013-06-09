import SearchBackend
#import it to avoid not found VimUi error, don't know how to fix it now.
import VimUi
from Candidate import TagCandidate

class BufferSearch:
    @staticmethod
    def instance():
        if not hasattr(BufferSearch, "_instance"):
            BufferSearch._instance = BufferSearch()
        return BufferSearch._instance

    def search(self, symbol):
        symbol = symbol.strip() or vim.eval('expand("<cword>")')
        candidates = self._createTagCandidate(symbol, vim.current.buffer)
        SearchBackend.showSearchResult(candidates)

    def searchAll(self, symbol):
        buffers =[buffer for buffer in vim.buffers if buffer.name and os.path.exists(buffer.name)]
        candidates = []
        for buffer in buffers:
            candidates.extend(self._createTagCandidate(symbol, buffer))
        SearchBackend.showSearchResult(candidates)

    def match(self, line, symbol):
        return symbol in line

    def _createTagCandidate(self, symbol, buffer):
        candidates = []
        if buffer and os.path.exists(buffer.name):
            with open(buffer.name) as f:
                for index, line in enumerate(f.readlines()):
                    if line.strip() and self.match(line, symbol):
                        candidate = TagCandidate(path = buffer.name, lineNumber = str(index + 1), codeSnip = line.strip())
                        candidates.append(candidate)
        return candidates
