import os
import vim

def findFileInPaths(pattern, dirPaths):
	results = []
	for dirPath in dirPaths:
		results.extend(findFileInPath(pattern, dirPath))
	return results

def findFileInPath(pattern, dirPath):
	results = []
	for rootDir, dirName, fileName in os.walk(dirPath):
		if pattern.match(fileName):
			results.append(os.path.join(rootDir, fileName))
	return results

def findFileInBufferList(pattern):
	result = []
	for buf in vim.buffers:
		if pattern.match(buf.name):
			result.append(buf.name)
	return result

def grepPatternInFiles(pattern, filePaths):
	results = []
	for filePath in filePaths:
		results.extend(grepPatternInFile(pattern, filePath))
	return results

def grepPatternInFile(pattern, filePath):
	return grepPatternInLines(pattern, file.readlines(filePath))

def grepPatternInLines(pattern, lines):
	lineNum = 0
	results = []
	for line in lines:
		lineNum = lineNum + 1
		if pattern.match(line):
			results.append("%d:%s)"%(lineNum,line))
	return results
