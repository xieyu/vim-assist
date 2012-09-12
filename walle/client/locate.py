import os
import vim
from shared.Controller import ControllerFactory
from shared.CandidateManager import FileCandidateManager
from shared.CandidateManager import TagCandidateManager
from shared.CandidateManager import RecentManager
from shared.CandidateManager import ReposManager
from shared.CandidateManager import GTagsManager
from shared.CandidateManager import MRUCandidateManager

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




class TagFinderDriver(Driver):
	def __init__(self):
		recentManager = RecentManager(self.getRecentPath())
		self.candidateManager = TagCandidateManager(recentManager)

	def setTagFile(self, tagFile):
		self.candidateManager.setTagFile(tagFile)

	def findTagByFullName(self, name):
		result = self.candidateManager.findTagByFullName(name)
		displayer = ControllerFactory.getDisplayController("find-tag", self.candidateManager)
		displayer.show(result)


class GTagDriver(Driver):
	def __init__(self):
		recentManager = RecentManager(self.getRecentPath())
		self.candidateManager = GTagsManager(recentManager)

	def globalCmd(self, name):
		args = name.split(" ")
		result = self.candidateManager.globalCmd(args)
		displayer = ControllerFactory.getDisplayController("find-tag", self.candidateManager)
		displayer.show(result)

	def globalFindFile(self, pattern):
		args = ["-Pi"] + [pattern]
		result = self.candidateManager.globalCmd(args)
		displayer = ControllerFactory.getDisplayController("find-tag", self.candidateManager)
		displayer.show(result)



class MRUDriver(Driver):
	def __init__(self):
		recentManager = RecentManager(self.getRecentPath())
		self.candidateManager = MRUCandidateManager(recentManager)


	def run(self):
		self.candidateManager.onStart()
		matcher = ControllerFactory.getPromptMatchController(title ="Go-to-file", candidateManager = self.candidateManager)
		matcher.run()

	def editReposConfig(self):
		vim.command("sp %s"%self.getReposPath())

	def editRecentConfig(self):
		vim.command("sp %s"%self.getRecentPath())


file_locate_driver = FileFinderDriver()
tag_locate_driver = TagFinderDriver()
gtagDriver = GTagDriver()
mruDriver = MRUDriver()
