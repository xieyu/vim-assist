import os

def findFileInPaths(pattern, dirPaths):
	results = []
	for dirPath in dirPaths:
		results.extend(findFileInPath(dirPath))
	return results

def findFileInPath(pattern, dirPath):
	results = []
	for rootDir, dirName, fileName in os.walk(dirPath):
		if pattern.match(fileName):
			results.append(os.path.join(rootDir, fileName))
	return results

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
	for line in file.readlines(filePath):
		lineNum = lineNum + 1
		if pattern.match(line):
			results.append("%d:%s)"%(lineNum,line))
	return results
