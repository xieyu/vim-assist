class Candidate:
	def __init__(self, name, key):
		'''name is the string that will show to user, key is used for compare and search,'''
		self.name = name
		self.key = key
	
	def getName(self):
		return self.name

	def getKey(self):
		return self.key

class FileCandidate(Candidate):
	def __init__(self, name, key, filePath):
		Candidate.__init__(self, name, key)
		self.filePath = filePath
		pass
		
	def getFilePath(self):
		return self.filePath

class LineCandidate(FileCandidate):
	def __init__(self, name, key, filePath, lineNum):
		FileCandidate.__init__(self, name, key, filePath)
		self.lineNum = lineNum

	def getLineNum(self):
		return self.lineNum

class SymbolCandidate(LineCandidate):
	def __init__(self, name, key, filePath, lineNum, wordPos):
		LineCandidate.__init__(self, name, key, filePath, lineNum)
		self.wordPos = wordPos

	def getWordPos(self):
		return self.wordPos
