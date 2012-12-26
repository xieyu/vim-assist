
let s:plugin_path = escape(expand('<sfile>:p:h'), '\')
let g:walle_home = s:plugin_path."/../walle/"
function! RunWalleFile(filename)
	exec "pyfile ".g:walle_home.a:filename
endfunction

function! SetUpPath()
python<<EOF
import sys
import os
import vim

walle_home = vim.eval("g:walle_home")
sys.path.append(os.path.abspath(walle_home))
EOF
endfunction

call SetUpPath()

"locate"
call RunWalleFile("python/SearchAssit.py")
call RunWalleFile("python/VimIDE.py")
"Commands:"
"command! EditReposConfig     py file_locate_driver.editReposConfig()
"command! RefreshFinderRepos  py file_locate_driver.refresh()
"command! FinderFile          py file_locate_driver.run()

"command! -nargs=1 SetTagFile 		   py tag_locate_driver.setTagFile(<q-args>)
"command! -nargs=1 FindTagByFullName    py tag_locate_driver.findTagByFullName(<q-args>)


"for Gtags, please make sure you have GTAGS in your cwd's or its parent's dir
"or parent's parent dir ...
command! -nargs=1 SearchSymbol     	   py SearchAssist.searchSymbol(<q-args>)
command! -nargs=1 SearchSymbolinBuffer     	   py SearchAssist.searchSymbolInBuffer(<q-args>)
command! -nargs=1 SearchSymbolDefine   py SearchAssist.searchSymbolDefine(<q-args>)
command! -nargs=1 SearchFile		   py SearchAssist.searchFile(<q-args>)
command! ChangeBetweenHeaderAndCFile py SearchAssist.changeBetweenHeaderAndcFile(<q-args>)

au BufRead,BufNewFile * 			   py SearchRecentFiles.addToRecent()
command! SearchAssist                  py SearchAssist.increamentSearch()
command! QuickSearch                   py SearchAssist.quickSearch()
command! MakeFilePathTags              py WalleTagsManager.makeFilePathTags()

"Maps:
map <C-f> :SearchAssist<CR>
map <C-g> :QuickSearch<CR>

nmap gs :SearchSymbol <C-R>=expand("<cword>")<CR><CR>
nmap g# :SearchSymbolinBuffer <C-R>=expand("<cword>")<CR><CR>

nmap gd :SearchSymbolDefine <C-R>=expand("<cword>")<CR><CR>
nmap gf :SearchFile <C-R>=expand("<cword>")<CR><CR>
nmap ga :ChangeBetweenHeaderAndCFile<CR>
