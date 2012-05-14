import VimUtils
class Candidate:
	def __init__(self, name, content, filePath = None, pos = None):
		self.name = name
		self.content = content
		self.filePath = filePath
		self.pos= pos

	def getName(self):
		'''name is the string that will show to user '''
		return self.name
		
	def getFilePath(self):
		''' if file path is None, then it will be treate as buffertype nofile in vim'''
		return self.filePath

	def getPos(self):
		'''pos contains (linenum, col)'''
		return self.pos

	def getContent(self):
		return self.content

class CandidatesFactory:
	@staticmethod
	def createForCurBuffer():
		#TODO:we need get current buffer's name
		contents = VimUtils.getCurBufferContent()
		filePath = VimUtils.getCurBufferName()
		#construct candidate for every line, we also need filename
		lineNum = 0
		candidates = []
		for line in contents:
			lineNum += 1
			name = "%d:%s"%(lineNum, line.strip())
			item = Candidate(name = name, content = line, pos = (lineNum, 0),filePath = filePath)
			
			candidates.append(item)
		return candidates

