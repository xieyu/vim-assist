import Controller
from Candidates import LineCandidate
from Candidates import FileCandidate
import VimUtils
import os

''''
This factory is famous for create normal components to make your life more comfortable....:D

@important:
	you must import SharedFactory in this way:
	from Factory import SharedFactory
	see MatchController and promptWindow 's doc for reason

@Attention: function in SharedFactory, will retun a shared object,
'''


class SharedFactory:
	import VimUi
	promptWindow = VimUi.PromptWindow("SharedFactory.promptWindow")
	matchController = Controller.MatchController("SharedFactory.matchController")
	@staticmethod
	def getMatchController(title, finder, acceptor):
		'''Note, the returned matcher is shared, the the one you get before will be clean and be reused'''
		SharedFactory.matchController.reNew(title, finder, acceptor,
				SharedFactory.promptWindow)
		return SharedFactory.matchController


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


