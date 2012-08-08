"Descrption: vim plugins for Find files in bundles
"Author:     xieyu3 at gmail dot com
"
"FileFinder is used for quick edit file just like sublime's command-p under
"certain Dirs, you "can set Dirs paths that will be searched, and quick find files by it's
"prefix.(currently just support prefix, maybe next version will support
"subString);
"
"intereface for user:
"
"Commands:
"
"use EditFinderRepos to edit the dirs paths that will be searched
command EditFinderRepos py editReposFile()

"use RefreshFinderRepos, if files under dirs has been changed
command RefreshFinderRepos py refresh()
command EditRecentList py editRecentFilesList()

"find files by prefix of filename
command FinderFile py find()


"Maps:
map <C-f> :FinderFile<CR>



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

#get repos file path
def getReposFilePath():
	reposPath = os.path.abspath(os.path.join(scriptdir, "reposPaths"))
	return reposPath

def getRecentFilesListPath():
	recentFilesPath = os.path.abspath(os.path.join(scriptdir, "recentFiles"))
	return recentFilesPath
	
def editReposFile():
	vim.command("sp %s"%getReposFilePath()) 
	vim.command("autocmd BufWritePost <buffer> py refresh()")

def editRecentFilesList():
	vim.command("sp %s"%getRecentFilesListPath())


from FileFinder import FileFinderDriver
#must import SharedFactory in *.vim file, see its doc for reason
from Factory import SharedFactory

driver = FileFinderDriver(getReposFilePath(), getRecentFilesListPath())

def find():
	driver.run()

def refresh():
	driver.refresh()
EOF
