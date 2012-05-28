
class MatchController:
	def __init__(self, selfName):
		'''
		self.selfName is a hack for use memberFunction for vim keyMap, 
		it will call the instance's memeber fuction in following way
		:py selfName.memberFunction(), 
		So make sure that python can access the it in global scope
		'''
		self.selfName = selfName
		#function name: comamnds
		self.commandMap ={
				"moveSelect":["selectPre", "selectNext", "nextPage", "prePage"],
				"acceptSelect":["acceptSelect"],
				}
		#command: [(keys,pramasList),(keys,  paramList)...]
		self.keysMap = {
				"selectPre":[(["<C-j>","<C-p>", "<Up>"], "pre")],
				"selectNext":[(["<C-n>","<Down>"], "down")],
				"nextPage": [(["<C-d>", "<PageDown>"], "nextPage")],
				"prePage" : [(["<C-u>", "<PageUp>"], "prePage")],
				"acceptSelect": [(["<cr>","<2-LeftMouse>"], "None")]
		}

	def reNew(self, title, finder, acceptor, window):
		self.window = window
		self.window.reNew(title, self.userInputListener)
		self.finder = finder
		self.acceptor = acceptor
		self.window.setOptions(("buftype=nofile", "nomodifiable", "nobuflisted", "noinsertmode", "nowrap","nonumber","textwidth=0"))
		self.curSelect = 0


	def addKeyMapForCommand(self, com, keys, param):
		'''
		now the public available command is acceptSelect, the param will be pass to the acceptor"
		@Attention: call this function before show(), 
		'''
		try:
			self.keysMap[com].append((keys, param))
		except:
			print "except when addkeyMapForCommnd"

	def setKeysMapForCommand(self, com, keys, param):
		'''
		@Attention: call this function before show()"
		'''
		try:
			self.keysMap[com] = [(keys, param)]
		except:
			print "except when setKeysMapForCommand"

	def show(self):
		self.makeKeyMap()
		self.window.show()

	#private
	def userInputListener(self, userInput):
		result = self.finder.query(userInput)
		self.window.setContent(result)

	def moveSelect(self, stepDescripte):
		stepsMap = {"next":1, "pre": -1, "nextPage":self.getCandidateNumOnOnePage(), "prePage": -1*self.getCandidateNumOnOnePage()}
		try:
			step = stepsMap[stepDescripte]
		except:
			return
		self.curSelect = max(min(self.curSelect + step, self.finder.getSuiteCandidateNum() -1), 0)
		#note: vim lineNum start with 1, not zero.
		print self.curSelect
		self.window.setCursor(self.curSelect + 1, 0)


	def acceptSelect(self, acceptWay):
		if acceptWay == "None":
			acceptWay = None
		candidate = self.getCurSuiteCandiate()
		if candidate:
			shouldKeep = self.acceptor.accept(candidate, acceptWay)
			if not shouldKeep:
				self.window.close()


	#private helpers
	def getCurSuiteCandiate(self):
		return self.finder.getSuiteCandidate(self.curSelect)

	def getCandidateNumOnOnePage(self):
		#currently we think that one line , one candidate
		return self.window.getHeight()

	def makeKeyMap(self):
		for functionName in self.commandMap.keys():
			for com in self.commandMap[functionName]:
				for keys, param in self.keysMap[com]:
					for key in keys:
						self.registerMemberFunction(key, functionName, param)

	def registerMemberFunction(self, key, function, param=None):
		functionName = "%s.%s"%(self.selfName, function)
		self.window.registerKeyMap(key, functionName, param)
	

