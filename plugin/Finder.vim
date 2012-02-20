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

scriptdir = os.path.dirname(vim.eval('expand("<sfile>")'))
if scriptdir not in sys.path:
    sys.path.insert(0, scriptdir)

import VimUi

vim.command("map <C-f> :py findFile()<CR>")

def findFile():
	paths="/Users/ic/codes/python:/Users/ic/codes/mypaint/:/Users/ic/codes/Finder/"
	patterns = vim.eval('input("File pattern ? ")')
	if patterns:
		results = findFileInPaths(paths, patterns)	
		windowId = int(vim.eval("winnr()"))
		if results:
			ui = VimUi.UI(title="findResults")
			ui.setContents(results)
			ui.show()
			vim.command("map <buffer> <Space> :py VimUi.openInWindow(%d, hideCurrent=False)<CR>"%windowId)
			vim.command("map <buffer> <Enter> :py VimUi.openInWindow(%d, hideCurrent=True)<CR>"%windowId)
		else:
			vim.command('echo "So Sorry,i cannot Find file with pattern %s"'%patterns)


def findFileInPaths(paths, pattern):
	try:
		m = re.compile(pattern)
	except:
		print "not vaildate patterns"
		return []
	paths = paths.split(':')
	results = []
	for path in paths:
		rootDir = os.path.expandvars(path)
		if not os.path.exists(rootDir):
			print "%s not exists"%rootDir
		for root, dirs, files in os.walk(rootDir):
			for dirPath in dirs:
				if m.match(dirPath):
					results.append(os.path.join(root, dirPath))
			for filePath in files:
				if m.match(filePath):
					results.append(os.path.join(root ,filePath))
	return results

EOF
