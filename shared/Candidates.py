class Candidate:
	def __init__(self, name, content):
		'''name is the string that will show to user, content is used for compare and search,'''
		self.name = name
		self.content = content
	
	def getName(self):
		return self.name

	def getContent(self):
		return self.content

class FileCandidate(Candidate):
	def __init__(self, name, content, filePath):
		Candidate.__init__(self, name, content)
		self.filePath = filePath
		pass
		
	def getFilePath(self):
		return self.filePath

class LineCandidate(FileCandidate):
	def __init__(self, name, content, filePath, lineNum):
		FileCandidate.__init__(self, name, content, filePath)
		self.lineNum = lineNum

	def getLineNum(self):
		return self.lineNum

class WordCandidate(LineCandidate):
	def __init__(self, name, content, filePath, lineNum, wordPos):
		LineCandidate.__init__(self, name, content, filePath, lineNum)
		self.wordPos = wordPos
	def getWordPos(self):
		return self.wordPos
