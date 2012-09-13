import os
import vim
import re
from shared.Controller import ControllerFactory
from shared.CandidateManager import FileCandidateManager
from shared.CandidateManager import RecentManager
from shared.CandidateManager import ReposManager
from shared.CandidateManager import GTagsManager
from shared.CandidateManager import MRUCandidateManager
from shared.CandidateManager import CandidateUntils

class Driver:
	def getReposPath(self):
		walle_home = vim.eval("g:walle_home")
		return os.path.abspath(os.path.join(walle_home, "config/reposConfig"))

	def getRecentPath(self):
		walle_home = vim.eval("g:walle_home")
		return os.path.abspath(os.path.join(walle_home, "config/recentEditFiles"))

class FileFinderDriver(Driver):
	def __init__(self):
		recentManager = RecentManager(self.getRecentPath())
		reposManager = ReposManager(self.getReposPath())
		self.candidateManager = FileCandidateManager(reposManager, recentManager)

	def refresh(self):
		self.candidateManager.refresh()

	def run(self):
		self.candidateManager.onStart()
		matcher = ControllerFactory.getPromptMatchController(title ="Go-to-file", candidateManager = self.candidateManager)
		matcher.run()

	def editReposConfig(self):
		vim.command("sp %s"%self.getReposPath())

	def editRecentConfig(self):
		vim.command("sp %s"%self.getRecentPath())



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

	def findSymbolDefine(self, pattern):
		result = self.candidateManager.findSymbolDefine(pattern)
		displayer = ControllerFactory.getDisplayController("symbol-define", self.candidateManager)
		displayer.setFileType("cpp")
		displayer.show(result)

	def findSymbolRef(self, pattern):
		result = self.candidateManager.findSymbolRef(pattern)
		displayer = ControllerFactory.getDisplayController("symbol-reference", self.candidateManager)
		displayer.setFileType("cpp")
		displayer.show(result)

	def findSymbol(self, pattern):
		result = self.candidateManager.findSymbol(pattern)
		displayer = ControllerFactory.getDisplayController("symbol", self.candidateManager)
		displayer.setFileType("cpp")
		displayer.show(result)

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
		if len(result) == 1:
			self.candidateManager.acceptCandidate(result[0],"None")
		else:
			displayer = ControllerFactory.getDisplayController("change_header_and_c", self.candidateManager)
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

	def editReposConfig(self):
		vim.command("sp %s"%self.getReposPath())

	def editRecentConfig(self):
		vim.command("sp %s"%self.getRecentPath())


file_locate_driver = FileFinderDriver()
#tag_locate_driver = TagFinderDriver()
gtagDriver = GTagDriver()
mruDriver = MRUDriver()

def DriverTest():
	gtagDriver.findSymbolRef("BeginPaint")

