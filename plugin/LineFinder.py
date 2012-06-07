import vim
from Candidates import LineCandidate
from Factory import SharedFactory
import CompareUtils
import Finder
import Acceptor

class CurrentBufferLineFinder:
	def __init__(self):
		self.finder = Finder.ScanFinder(CompareUtils.containIgnoreCaseCompare, CompareUtils.containIgnoreCaseCompare)
		self.acceptor = Acceptor.LineAcceptor()
		self.candidateManager = LineCandidateManager()

	def find(self):
		candidates = self.candidateManager.get_current_buffer_sybmol_candidates()
		self.finder.setCandidates(candidates)
		matcher = SharedFactory.getMatchController(title ="Go-to-file", finder = self.finder, acceptor = self.acceptor)
		matcher.setPreview(True)
		matcher.show()

class LineCandidateManager:
	def __init__(self):
		pass
	def get_current_buffer_sybmol_candidates(self):
		candidates = []
		bufferName = vim.current.buffer.name
		for lineNum,line in enumerate(vim.current.buffer):
			line = line.strip()
			if line:
				iterm = LineCandidate(name = "%d:\t %s"%(lineNum, line), key = line, filePath = bufferName, lineNum = lineNum + 1)#vim line number start by 1
				candidates.append(iterm)
		return candidates

