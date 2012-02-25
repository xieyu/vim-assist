"Descrption: vim plugins for Find files in bundles with regular expression
"Author:     xieyu3 at gmail dot com
"Usage:      list the directory in the paths, sperate it with symbol ':'
"
"		     press <ctrl-F> to active the query, if find something,it  will show a
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

paths = "/Users/ic/codes/python:/Users/ic/codes/mypaint/:/Users/ic/codes/Finder/:/Users/ic/demos"
paths = paths.split(':')

def dispather(args):
	parser= optparser.Optionparser()
	parser.add_option("-f", "--findFile", dest="findFile")
	parser.add_option("-g", "--findPatterns", dest="grepPatterns")
	(options, args) = parser.parser_args(args)

def getFilePattern():
	pattern = vim.eval('input("file pattern :)")')
	print "hi"
	if not pattern:
		return None
	try:
		pattern = re.compile(pattern, re.IGNORECASE)
	except:
		print "Sorry, Can not understand it :("
		return None
	return pattern

def findFile():
	pattern = getFilePattern()
	if pattern:
		results = MyFinder.findFileInPaths(pattern, paths)	
		if results:
			showResults("findResults:", results, "findFileHandler")
		else:
			vim.command('echo "So Sorry,cannot Find it"')

def grepPattern(linePattern, Files):
	results = MyFinder.grepPatternInFiles(linePattern, filePaths)	
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
