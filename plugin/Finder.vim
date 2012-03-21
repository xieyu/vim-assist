"Descrption: vim plugins for Find files in bundles with regular expression
"Author:     xieyu3 at gmail dot com
"
"Usage:      in .vimrc, set g:paths and g:pathSep, like this way:
"            let g:paths="path1:path2:path3"
"            let g:pathSep=":"
" 			 in windows, you can set pathSep to ';' or whatever you like
"
"		     press <ctrl-f> to active the query, if find something,it  will show a
"		     output window that list the Found file path. 
"
"		     In output window, move to the line that you want open, press <Eneter> 
"		     to hide the output window and show that File in last window. 
"
"		     press <Space> 's behavior is same with <Enter> But keep the
"		     output window.


"Settings:
let g:paths="/Users/ic/codes/:/Users/ic/demos:/Users/ic/.vim"
let g:pathsSep=":"

"Maps:
map <C-f> :py findFile()<CR>

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

#vim.command("map <C-f> :py findFile()<CR>")

#TODO:check if these vars exists
paths = vim.eval('g:paths')
pathsSep = vim.eval('g:pathsSep')
paths = paths.split(pathsSep)

fileFinder = MyFinder.FileFinder(paths)

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
		results.extend( fileFinder.searchInBufferList(pattern))
		if not onlyfindInBufferList:
			results.extend(fileFinder.search(pattern))
		if results:
			#make it unique
			results =list(set(results))
			VimUi.showResults("findResults", results, "findFileHandler")
		else:
			vim.command('echo "So Sorry, cannot Find it :("')

def findFileHandler(line):
	filePath = line
	lineNum = None
	return (filePath, lineNum)
EOF
