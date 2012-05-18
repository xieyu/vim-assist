import Controller
import Finder
import Acceptor
from Candidates import LineCandidate
from Candidates import FileCandidate
import VimUtils
import os

''''
This factory is famous for create normal components to make your life more comfortable....:D

@Attention: function in SharedFactory, will retun a shared object,
'''


class SharedFactory:
	@staticmethod
	def getMatchController(title, finder, acceptor):
		'''Note, the returned matcher is shared, the the one you get before will be clean and be reused'''
		matchController.reNew(title, finder, acceptor, promptWindow)
		return matchController


class CandidatesFactory:
	@staticmethod
	def createForCurBuffer():
		lines = VimUtils.getCurBufferContent()
		filePath = VimUtils.getCurBufferName()
		return CandidatesFactory.createLineCandidatesForFile(filePath, lines)

	@staticmethod
	def createLineCandidatesForFile(filePath, lines):
		lineNum = 0
		candidates = []
		for line in lines:
			lineNum += 1
			name = "%d:%s"%(lineNum, line.strip())
			item = LineCandidate(name = name, content = line, filePath = filePath, lineNum = lineNum)
			candidates.append(item)
		return candidates

	@staticmethod
	def createForReposPath(reposPaths):
		candidates = []
		try:
			for repos in reposPaths:
				for root, dirs, files in os.walk(repos):
					for filePath in files:
						filePath = os.path.join(root, filePath)
						item = FileCandidate(name = filePath, content = filePath, filePath = filePath)
						candidates.append(item)
			return candidates
		except:
			return []

class FinderFactory:
	def createScanFinder():
		pass


import VimUi
promptWindow = VimUi.PromptWindow("Factory.promptWindow")
matchController = Controller.MatchController("Factory.matchController")
