"Descrption: vim plugins for Find files in bundles
"Author:     xieyu3 at gmail dot com
"
"Commands:
"
"Options:
"
"Maps:
map <C-b> :py refresh()<CR>
map <C-f> :py find()<CR>


if !exists("g:reposFile")
	let g:reposFile = "/Users/ic/.vim/bundle/finder/reposPaths"
endif

python<<EOF
import os
import sys
import vim
#include shared lib to sys.path
for path in vim.eval("&runtimepath").split(','):
	lib = "%s/shared"%path
	if lib not in sys.path and os.path.exists(lib):
		sys.path.insert(0, lib)

scriptdir = os.path.dirname(vim.eval('expand("<sfile>")'))
if scriptdir not in sys.path:
    sys.path.insert(0, scriptdir)

from FileFinder import FileFinder
from Factory import SharedFactory

reposFile = vim.eval("g:reposFile")
filefinder = FileFinder(reposFile)

def find():
	filefinder.find()

def refresh():
	filefinder.refresh()
EOF
