
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
call RunWalleFile("client/locate.py")
"Commands:"
"command! EditReposConfig     py file_locate_driver.editReposConfig()
"command! RefreshFinderRepos  py file_locate_driver.refresh()
"command! FinderFile          py file_locate_driver.run()

"command! -nargs=1 SetTagFile 		   py tag_locate_driver.setTagFile(<q-args>)
"command! -nargs=1 FindTagByFullName    py tag_locate_driver.findTagByFullName(<q-args>)


"for Gtags, please make sure you have GTAGS in your cwd's or its parent's dir
"or parent's parent dir ...
command! -nargs=1 GlobalCmd	       py gtagDriver.globalCmd(<q-args>)
command! -nargs=1 FindFile		   py gtagDriver.findFile(<q-args>)
command! -nargs=1 FindSymbol     	   py gtagDriver.findSymbol(<q-args>)
command! -nargs=1 FindSymbolDefine     py gtagDriver.findSymbolDefine(<q-args>)
command! -nargs=1 FindSymbolRef        py gtagDriver.findSymbolRef(<q-args>)
command! ChangeBetweenHeaderAndcFile   py gtagDriver.changeBetweenHeaderAndcFile()

"MRU managerment
command! FindInMRU 		   	   		   py mruDriver.run()
command! AddToRecent 		   		   py mruDriver.addCurrentToRecent()
command! EditRecent  				   py mruDriver.editRecentConfig()
command! -nargs=1 AddPathToRecent 	   py mruDriver.addPathToRecent(<q-args>)
au BufRead,BufNewFile * 			   py mruDriver.addCurrentToRecent()

"quick find
command! -nargs=1 FindInBuffer         py quickFindDriver.findInCurrentBuffer(<q-args>)
command! -nargs=1 FindInAllBuffer      py quickFindDriver.findInAllBuffers(<q-args>)

command! WalleTest  				   py DriverTest()

command! FindVimCommand 		   	   py vimCommandDriver.run()
command! EditVimCommand                py vimCommandDriver.editVimCommandConfig()

"Maps:
map <C-f> :FindInMRU<CR>
map <C-g> :FindFile 
map <C-p>    :FindVimCommand<CR>
nmap ga :ChangeBetweenHeaderAndcFile<CR>
nmap gd :FindSymbolDefine <C-R>=expand("<cword>")<CR><CR>
nmap gs :FindSymbol <C-R>=expand("<cword>")<CR><CR>
nmap gr :FindSymbolRef <C-R>=expand("<cword>")<CR><CR>
nmap g# :FindInBuffer <C-R>=expand("<cword>")<CR><CR>
nmap g? :FindInAllBuffer <C-R>=expand("<cword>")<CR><CR>
