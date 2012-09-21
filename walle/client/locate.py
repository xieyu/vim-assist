import os
import vim
import re
from shared.Controller import ControllerFactory
from shared.CandidateManager import RecentManager
from shared.CandidateManager import GTagsManager
from shared.CandidateManager import MRUCandidateManager
from shared.CandidateManager import CandidateUntils
from shared.CandidateManager import QuickFind
from shared.CandidateManager import VimCommandCandidateManager

class Driver:
	def getReposPath(self):
		walle_home = vim.eval("g:walle_home")
		return os.path.abspath(os.path.join(walle_home, "config/reposConfig"))

	def getRecentPath(self):
		walle_home = vim.eval("g:walle_home")
		return os.path.abspath(os.path.join(walle_home, "config/recentEditFiles"))

	def getVimCommandPath(self):
		walle_home = vim.eval("g:walle_home")
		return os.path.abspath(os.path.join(walle_home, "config/vimCommand"))

	def editReposConfig(self):
		vim.command("sp %s"%self.getReposPath())

	def editRecentConfig(self):
		vim.command("sp %s"%self.getRecentPath())

	def editVimCommandConfig(self):
		vim.command("sp%s"%self.getVimCommandPath())
		


class GTagDriver(Driver):
	def __init__(self):
		recentManager = RecentManager(self.getRecentPath())
		self.candidateManager = GTagsManager(recentManager)

	def globalCmd(self, name):
		args = name.split(" ")
		result = self.candidateManager.globalCmd(args)
		displayer = ControllerFactory.getDisplayController("global-Cmd", self.candidateManager)
		displayer.show(result)

	def findFile(self, pattern):
		result = self.candidateManager.findFile(pattern)
		displayer = ControllerFactory.getDisplayController("Goto-file", self.candidateManager)
		displayer.show(result)

	def showResut(self, result, pattern, title):
		displayer = ControllerFactory.getDisplayController("%s"%title, self.candidateManager)
		if  len(result) == 0:
			print "can not find symbol with pattern %s"%pattern
		elif(len(result)==1):
			self.candidateManager.acceptCandidate(result[0])
		else:
			displayer.setFileType("cpp")
			displayer.show(result)

	def findSymbolDefine(self, pattern):
		result = self.candidateManager.findSymbolDefine(pattern)
		self.showResut(result, pattern, "symbol-define")

	def findSymbolRef(self, pattern):
		result = self.candidateManager.findSymbolRef(pattern)
		self.showResut(result, pattern, "symbol-reference")


	def findSymbol(self, pattern):
		result = self.candidateManager.findSymbol(pattern)
		self.showResut(result, pattern, "symbol")

	def changeBetweenHeaderAndcFile(self):
		try:
			filename = os.path.basename(vim.current.buffer.name)
		except:
			return
		s = []
		if re.search("\.(h|hpp)$", filename):
			s.append(re.sub("\.(h|hpp)$", ".cpp", filename))
			s.append(re.sub("\.(h|hpp)$", ".c", filename))
			s.append(re.sub("\.(h|hpp)$", ".cc", filename))
			s.append(re.sub("\.(h|hpp)$", ".m", filename))
		elif re.search("\.(c|cpp|cc|m)$", filename):
			s.append(re.sub("\.(c|cpp|cc)$", ".h", filename))
			s.append(re.sub("\.(c|cpp|cc)$", ".hpp", filename))

		result = []
		for pattern in s:
			result.extend(self.candidateManager.findFile(pattern))
		result = CandidateUntils.unique(result)

		if len(result) == 0:
			print "can not find file in list: %s"%s
		elif len(result) == 1:
			self.candidateManager.acceptCandidate(result[0])
		else:
			displayer = ControllerFactory.getDisplayController("change_header_and_c", self.candidateManager)
			displayer.show(result)

class QuickFindDriver:
	def __init__(self):
		self.candidateManager = QuickFind()

	def findInCurrentBuffer(self, pattern):
		result = self.candidateManager.findInCurrentBuffer(pattern)
		displayer = ControllerFactory.getDisplayController("find-in-current-buffer", self.candidateManager)
		displayer.show(result)
		displayer.highLightWord(pattern)

	def findInAllBuffers(self, pattern):
		result = self.candidateManager.findInAllBuffers(pattern)
		displayer = ControllerFactory.getDisplayController("find-in-all-buffer", self.candidateManager)
		displayer.show(result)


class MRUDriver(Driver):
	def __init__(self):
		recentManager = RecentManager(self.getRecentPath())
		self.candidateManager = MRUCandidateManager(recentManager)


	def run(self):
		self.candidateManager.onStart()
		matcher = ControllerFactory.getPromptMatchController(title ="Go-to-file", candidateManager = self.candidateManager)
		matcher.run()

	def addCurrentToRecent(self):
		self.candidateManager.addPathtoRecent(vim.current.buffer.name)

	def addPathtoRecent(self, path):
		self.candidateManager.addPathtoRecent(path)


class VimCommandDriver(Driver):
	def __init__(self):
		#recentManager = RecentManager()
		self.candidateManager = VimCommandCandidateManager(self.getVimCommandPath())

	def run(self):
		self.candidateManager.onStart()
		matcher = ControllerFactory.getPromptMatchController(title ="command", candidateManager = self.candidateManager)
		matcher.run()







gtagDriver = GTagDriver()
mruDriver = MRUDriver()
quickFindDriver = QuickFindDriver()
vimCommandDriver = VimCommandDriver()


def DriverTest():
	gtagDriver.findSymbolRef("BeginPaint")


