import os
import vim
import threading
import time

class FileFinder:
	def __init__(self, paths):
		self.paths = paths
		self.filePathCache = None
		self.cacheLock = threading.Lock()
		self.makeCache()

	def makeCache(self):
		threading.Thread(target = self.doMakeCache, args = (10,)).start()

	def doMakeCache(self, delay):
		self.doMakeCacheEx()

	def doMakeCacheEx(self):
		self.cacheLock.acquire()
		self.filePathCache = []
		for rootDirPath in self.paths:
			for rootDir, dirs, files in os.walk(rootDirPath):
				for filePath in files:
					self.filePathCache.append(os.path.join(rootDir,filePath))
		self.cacheLock.release()

	def search(self, pattern):
		if self.filePathCache is None:
			self.makeCache()
		self.cacheLock.acquire()
		results = [filePath for filePath in self.filePathCache if pattern.match(os.path.basename(filePath))]
		self.cacheLock.release()
		return results

	def searchInBufferList(self, pattern):
		results = []
		for buf in vim.buffers:
			if buf.name and os.path.exists(buf.name):
				if pattern.match(os.path.basename(buf.name)):
					results.append(buf.name)
		return results

def findFileInPaths(pattern, dirPaths):
	results = []
	for dirPath in dirPaths:
		results.extend(findFileInPath(pattern, dirPath))
	return results

def findFileInPath(pattern, dirPath):
	results = []
	for rootDir, dirs, files in os.walk(dirPath):
		for fileName in files:
			if pattern.match(fileName):
				results.append(os.path.join(rootDir, fileName))
	return results

def findFileInBufferList(pattern):
	result = []
	for buf in vim.buffers:
		if buf.name and os.path.exists(buf.name):
			if pattern.match(os.path.basename(buf.name)):
				result.append(buf.name)
	return result

def grepPatternInFiles(pattern, filePaths):
	results = []
	for filePath in filePaths:
		results.extend(grepPatternInFile(pattern, filePath))
	return results

def grepPatternInFile(pattern, filePath):
	return grepPatternInLines(pattern, open(filePath).readlines())

def grepWordInFiles(word, filePaths):
	results = []
	for filePath in filePaths:
		lineNum = 1
		for line in open(filePath).readlines():
			if line.find(word) != -1:
				results.append("%d:%s"%(lineNum,line))
			lineNum = lineNum + 1
	return results
			


def grepPatternInLines(pattern, lines):
	lineNum = 0
	results = []
	for line in lines:
		lineNum = lineNum + 1
		if pattern.match(line):
			results.append("%d:%s"%(lineNum,line))
	return results
