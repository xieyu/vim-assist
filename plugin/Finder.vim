"Descrption: vim plugins for Find files in bundles with regular expression
"Author:     xieyu3 at gmail dot com
"Usage:      list the directory in the paths, sperate it with symbol ':'
"
"		     press <ctrl-f> to active the query, if find something,it  will show a
"		     output window that list the Found file path. 
"
"		     In output window, move to the line that you want open, press <Eneter> 
"		     to hide the output window and show that File in last window. 
"
"		     press <Space> 's behavior is same with <Enter> But keep the
"		     output window.
python<<EOF

import vim
import os
import sys
import re
import optparse

scriptdir = os.path.dirname(vim.eval('expand("<sfile>")'))
if scriptdir not in sys.path:
    sys.path.insert(0, scriptdir)

import MyFinder
import VimUi

vim.command("map <C-f> :py findFile()<CR>")
vim.command("nmap <?> :py grepPattern()<CR>")

paths = "/Users/ic/codes/python:/Users/ic/codes/mypaint/:/Users/ic/codes/Finder/:/Users/ic/demos:/Users/ic/.vim"
paths = paths.split(':')

def getFindFileArgs():
	args = vim.eval('input("file pattern: ")')
	if not args:
		return (None, None)
	parser = optparse.OptionParser()
	parser.add_option("-b", dest = "onlyfindInBufferList", action = "store_true", help = "just find in current BufferList")
	(options, args) = parser.parse_args(args.split())
	try:
		pattern = args[0]
	except:
		#just list all buffers if no pattern
		if options.onlyfindInBufferList:
			pattern = ".*"
	try:
		pattern = re.compile(pattern, re.IGNORECASE)
	except:
		print "Sorry, Can not understand it :("
		return (None, None)
	return (options.onlyfindInBufferList, pattern)

def findFile():
	(onlyfindInBufferList, pattern) = getFindFileArgs()
	results = []
	if pattern:
		results.extend( MyFinder.findFileInBufferList(pattern))
		if not onlyfindInBufferList:
			results.extend(MyFinder.findFileInPaths(pattern, paths))
		if results:
			showResults("findResults:", results, "findFileHandler")
		else:
			vim.command('echo "So Sorry, cannot Find it"')

def getGrepPatternArgs():
	args = vim.eval('input("grep: ")')
	if not args:
		return(None, None, None)
	parser = optparse.OptionParser()
	parser.add_option("-b", dest ="onlyGrepInBuffer", action = "store_true", help = "just grep in buffer")
	parser.add_option("-f", dest = "fileNamePattern", help = "the files math that pattern that will be greped") 
	(options, args) = parser.parse_args(args.split())
	try:
		linePattern = args[0]
	except:
		return (None, None, None)

	if options.fileNamePattern is None:
		if options.onlyGrepInBuffer:
			options.fileNamepattern = ".*"
			print "options.fileNamePattern is%s"%options.fileNamePattern
		else:
			return (None, None, None)
	try:
		print "fileNamePattern is %s"%options.fileNamePattern
		fileNamePattern = re.compile(options.fileNamePattern)
		print "line pattern is %s"%linePattern
		linePattern =re.compile(linePattern)
	except:
		print "Sorry, Can not undersand it :("
		return (None, None, None)
	return (options.onlyGrepInBuffer, fileNamePattern, linePattern)


def grepPattern():
#(onlyGrepInBuffer, fileNamePattern, linePattern) = getGrepPatternArgs()
	(onlyGrepInBuffer, fileNamePattern, linePattern) = (True, re.compile("vim"), re.compile("grep"))
	print "after assignment"
	if onlyGrepInBuffer is None or fileNamePattern is None or linePattern is None:
		return

	filePaths = []
	filePaths.extend(MyFinder.findFileInBufferList(fileNamePattern))
	if not onlyGrepInBuffer:
		filePaths.extend(MyFinder.findFileInPaths(fileNamePattern))
	if filePaths is []:
		print "file path is None"
		return
		#results = MyFinder.grepPatternInFiles(linePattern, filePaths)
	results = MyFinder.grepPatternInFile(linePattern, filePaths)
	if results:
		showResults("findResults:", results, "grepPatternHandler")
	else:
		vim.command('echoho "Sorry, Cannot find it"')


def showResults(showTitle, results, handler):
	windowId = int(vim.eval("winnr()"))
	ui = VimUi.UI(title=showTitle)
	ui.setContents(results)
	ui.show()
	vim.command("map <buffer> <Space> :py %s(%d, hideCurrent=False)<CR>"%(handler,windowId))
	vim.command("map <buffer> <Enter> :py %s(%d, hideCurrent=True)<CR>"%(handler, windowId))
	
def findFileHandler(windowId, hideCurrent):
	filePath = vim.current.line
	if os.path.exists(filePath):
		if hideCurrent:
			vim.command("hide") #hide current window
		vim.command("%d wincmd w"%windowId) #move focus to windowId
		#TODO:handle when buffer is already loaded
		vim.command("e %s"%filePath)

def grepPatternHandler(windowId, hideCurrent):
	content = vim.current.line
	temp = content.split(":")
	try:
		filePath, lineNum = (temp[0], int(temp[1]))
	except:
		return

	if os.path.exists(filePath):
		if hideCurrent:
			vim.command("hide")
		vim.command("%d wincmd w"%windowId) #move focus to windowId
		vim.command("e %s"%filePath)
		vim.command("%d"%lineNum) #jump to that line
	pass

EOF
