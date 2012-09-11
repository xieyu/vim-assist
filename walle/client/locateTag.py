from ctags import CTags, TagEntry
import ctags

class TagFinderDriver:
	def setTagFile(self, tagFile):
		self.tagFinder.setTagFile(tagFile)

	def findTagByFullName(self, name):
		result = self.tagFinder.findTagByFullName(name)


class TagCandidate:
	def __init__(self, name, filePath, lineNumber):
		self.name = name
		self.filePath = filePath
		self.lineNumber = lineNumber

	def getPath(self):
		return self.filePath

	def getlineNumber(self):
		return int(self.lineNumber)

	def getDisplayName(self):
		pass

class TagFinder:
	def setTagFile(self, tagFile):
		self.tagFilePath = tagFile
		self.tagFile=CTags(tagFile)

	def getAllEntryInKind(self, kind):
		entry = TagEntry()
		result = []
		while self.tagFile.next(entry):
			if entry['kind'] == kind:
				result.append(entry['name'])
		return result

	def findTagByFullName(self, name):
		entry = TagEntry()
		result = []
		if self.tagFile.find(entry,name, ctags.TAG_FULLMATCH):
			result.append(TagCandidate(entry['name'], entry['file'], entry['lineNumber']))
		while self.tagFile.findNext(entry):
			result.append(TagCandidate(entry['name'], entry['file'], entry['lineNumber']))
		return result


