import VimUtils
from SettingManager import settingManager

class MatchController:
	def __init__(self, selfName):
		'''
		self.selfName is a hack for use memberFunction for vim keyMap
		'''
		self.selfName = selfName
		self.settingScope = "MatchController"

	def reNew(self, title, finder, window):
		self.window = window
		self.window.reNew(title, self.userInputListener)
		self.finder = finder
		self.window.setOptions(("buftype=nofile", "nomodifiable", "nobuflisted", "noinsertmode", "nowrap","nonumber","textwidth=0"))
		self.makeKeyMap()
		self.curSelect = 0

	def show(self):
		self.oldWindowId = VimUtils.getCurWinId()
		self.window.show()


	#private
	def userInputListener(self, userInput):
		result = self.finder.query(userInput)
		self.window.setContent(result)

	def getCurSuiteCandiate(self):
		return self.finder.getSuiteCandidate(self.curSelect)

	def makeKeyMap(self):
		commands = [("openInOldWin","keep","openInOldWindow"),
				 	("openInOldWinThenHideSelf", "hide", "openInOldWindow"),
				 	("selectPre",None,"selectPre"),
				 	("selectNext",None,"selectNext")
				 	]
		for com ,option, functionName in commands:
			key = settingManager.getScopeKeyMap(self.settingScope, com)
			if key:
				self.registerMemberFunction(key, functionName, option)
			else:
				print "com %s can not find its key"%com


	def registerMemberFunction(self, key, function, param=None):
		functionName = "%s.%s"%(self.selfName, function)
		self.window.registerKeyMap(key, functionName, param)
	
	def selectPre(self):
		print "select pre"
		self.moveSelect(-1)

	def selectNext(self):
		print "select next"
		self.moveSelect(1)

	def moveSelect(self, step):
		sel = self.curSelect + step
		#note:suiteCandidateNum maybe zero
		if sel > self.finder.getSuiteCandidateNum() - 1:
			sel = self.finder.getSuiteCandidateNum() - 1
		if sel < 0:
			sel = 0
		self.curSelect = sel
		#note: vim lineNum start with 1, not zero.
		VimUtils.jumpToLine(self.curSelect + 1)

	def openInOldWindow(self, openOptions):
		candidate = self.getCurSuiteCandiate()
		if candidate is None:
			return

		pos = candidate.getPos()
		if openOptions != "keep":
			self.window.close()
		if self.oldWindowId:
			VimUtils.makeWinFocusOn(self.oldWindowId)
		VimUtils.openFile(candidate.getFilePath(), pos)
