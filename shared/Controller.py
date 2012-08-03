import vim
import VimUtils
class InputMatchController:
	def __init__(self, selfName):
		'''
		self.selfName is a hack for use memberFunction for vim keyMap, 
		it will call the instance's memeber fuction in following way
		:py selfName.memberFunction(), 
		So make sure that python can access the it in global scope
		'''
		self.selfName = selfName
		self.keysMap = { 
				"close":{"<esc>":"None", "<c-c>":"None", "<c-g>":"None"},
				}
		self.searchResult = None
		self.errorMsg = "find nothing :("
		self.prompt = ">>"
		self.closeCallback = None

	def renew(self, title, finder, acceptor, window):
		self.window = window
		self.window.renew(title)
		self.finder = finder
		self.acceptor = acceptor
		self.keysMap["acceptSelect"] = self.acceptor.getKeysMap()
		self.window.setOptions(("buftype=nofile", "nomodifiable", "nobuflisted", "noinsertmode", "nowrap","nonumber","textwidth=0"))
		pass

	def setPrompt(self, prompt):
		self.prompt = prompt

	def setErrorMsg(self, errorMsg):
		self.errorMsg = errorMsg

	def run(self):
		#FIXME:use right command at here
		userInput = vim.eval('''input("%s")'''%self.prompt)
		self.searchResult = self.finder.query(userInput)
		if self.searchResult:
			self.makeKeyMap()
			self.window.show()
			self.window.setContent(map(lambda item: item.getName(), self.searchResult))
		else:
			VimUtils.echo(self.errorMsg)
			self.window.close()

	def makeKeyMap(self):
		for functionName in self.keysMap.keys():
			for key, param in self.keysMap[functionName].items():
				self.registerMemberFunction(key, functionName, param)

	def registerMemberFunction(self, key, function, param=None):
		functionName = "%s.%s"%(self.selfName, function)
		self.window.registerKeyMap(key, functionName, param)

	def acceptSelect(self, acceptWay):
		candidate = self.getCurSelectedCandiate()
		if candidate:
			shouldKeep = self.acceptor.accept(candidate, acceptWay)
			if not shouldKeep:
				self.window.close()

	def getCurSelectedCandiate(self):
		curSelect = VimUtils.getCurLineNum() - 1
		try:
			return self.searchResult[curSelect]
		except:
			return None

	def getCandidateNumber(self):
		try:
			return len(self.searchResult)
		except:
			return 0

	def getCandidateNumOnOnePage(self):
		#currently we think that one line , one candidate
		return self.window.getHeight()

	def close(self, param):
		#param is "None", ignore it anyway
		if self.closeCallback:
			self.closeCallback()
		self.window.close()

	def setCloseCallback(self, closeCallback):
		self.closeCallback = closeCallback


class PromptMatchController(InputMatchController):
	def __init__(self, selfName):
		InputMatchController.__init__(self, selfName)
		self.keysMap["moveSelect"] = {
					"<C-k>": "pre","<C-p>":"pre", "<Up>":"pre",
					"<C-j>": "next", "<C-n>": "next","<Down>": "next",
					"<C-d>":"nextPage", "<PageDown>": "nextPage",
					"<C-u>": "prePage", "<PageUp>": "prePage"
					}

	def renew(self, title, finder, acceptor, window):
		self.window = window
		self.window.renew(title, self.userInputListener)
		self.finder = finder
		self.acceptor = acceptor
		self.keysMap["acceptSelect"] = self.acceptor.getKeysMap()
		self.window.setOptions(("buftype=nofile", "nomodifiable", "nobuflisted", "noinsertmode", "nowrap","nonumber","textwidth=0"))
		self.curSelect = 0

	def run(self):
		self.makeKeyMap()
		self.userInputListener("")
		self.window.show()

	#private
	def userInputListener(self, userInput):
		self.searchResult = self.finder.query(userInput)
		self.window.setContent(map(lambda item: item.getName(), self.searchResult))

	def moveSelect(self, stepDescripte):
		stepsMap = {"next":1, "pre": -1, "nextPage":self.getCandidateNumOnOnePage(), "prePage": -1*self.getCandidateNumOnOnePage()}
		try:
			step = stepsMap[stepDescripte]
		except:
			return
		self.curSelect = max(min(self.curSelect + step, self.getCandidateNumber() -1), 0)
		#note: vim lineNum start with 1, not zero.
		self.window.setCursor(self.curSelect + 1, 0)
		self.window.redraw()

	#private helpers
	def getCurSelectedCandiate(self):
		try:
			return self.searchResult[self.curSelect]
		except:
			return None

