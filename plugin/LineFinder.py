import vim
from Candidates import Candidate
from Factory import SharedFactory
from Acceptor import Acceptor
import Finder

class LineFinderDriver:
	def __init__(self):
		self.finder = Finder.ScanFinder(self.match)
		self.acceptor = LineAcceptor()
		self.candidateManager = LineCandidateManager()

	def run(self):
		candidates = self.candidateManager.getLinesInCurBuffer()
		self.finder.setCandidates(candidates)
		matcher = SharedFactory.getPromptMatchController(title ="Go-To-Line", finder = self.finder, acceptor = self.acceptor)
		matcher.run()

	def match(self, userInput, candidate):
		return userInput in candidate.getLineContent()

class LineCandidateManager:
	def __init__(self):
		pass

	@staticmethod
	def getLinesInCurBuffer():
		candidates = []
		bufferName = vim.current.buffer.name
		for lineNum,line in enumerate(vim.current.buffer):
			line = line.strip()
			if line:
				iterm = LineCandidate(name = "%d:\t %s"%(lineNum, line), filePath = bufferName, lineNum = lineNum + 1, lineContent = line)#vim line number start by 1
				candidates.append(iterm)
		return candidates
	@staticmethod
	def getLinesInBuffers():
		pass

	

class LineCandidate(Candidate):
	def __init__(self, name, key, filePath, lineNum):
		Candidate.__init__(name, key)
		self.path = filePath
		self.lineNum = lineNum

	def getLineNum(self):
		return self.lineNum

	def getPath(self):
		return self.path

	def getLineContent(self):
		return self.lineContent

class LineAcceptor(Acceptor):
	def __init__(self):
		pass

	def accept(self, lineCandidate, options = None):
		if options is None:
			return self.editFile(lineCandidate)

	def selectWindow(self):
		vim.command("wincmd w") #try next window

	def editFile(self, lineCandidate):
		self.selectWindow()
		vim.command("silent e %s"%lineCandidate.getFilePath())
		vim.command("%d"%lineCandidate.getLineNum())
		#close the query the window
		return False

