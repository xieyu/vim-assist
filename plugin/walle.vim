
function RunWalleFile(filename)
	exec "pyfile ".g:walle_home.a:filename
endfunction

function SetUpPath()
python<<EOF
import sys
import os
import vim
walle_home = vim.eval("g:walle_home")
sys.path.append(os.path.abspath(walle_home))
EOF
endfunction

call SetUpPath()

"locate files"
call RunWalleFile("client/locate.py")
"Commands:"
command! EditReposConfig     py file_locate_driver.editReposConfig()
command! EditRecentConfig    py file_locate_driver.editRecentConfig()
command! RefreshFinderRepos  py file_locate_driver.refresh()
command! FinderFile          py file_locate_driver.run()

"command! -nargs=1 SetTagFile 		   py tag_locate_driver.setTagFile(<q-args>)
"command! -nargs=1 FindTagByFullName    py tag_locate_driver.findTagByFullName(<q-args>)
command! -nargs=1 GtagsFindFile		   py gtagDriver.findFile(<q-args>)
command! -nargs=1 GtagsFindCmd	       py gtagDriver.globalCmd(<q-args>)
command! ChangeBetweenHeaderAndcFile   py gtagDriver.changeBetweenHeaderAndcFile()
command! -nargs=1 FindSymbol     	   py gtagDriver.findSymbol(<q-args>)
command! -nargs=1 FindSymbolDefine     py gtagDriver.findSymbolDefine(<q-args>)
command! -nargs=1 FindSymbolRef        py gtagDriver.findSymbolRef(<q-args>)

command! FindInMRU 		   	   		   py mruDriver.run()
command! AddCurrentToRecent 		   py mruDriver.addCurrentToRecent()
command! -nargs=1 AddPathToRecent 	   py mruDriver.addPathToRecent(<q-args>)

command! WalleTest  				   py DriverTest()

au BufRead,BufNewFile * py mruDriver.addCurrentToRecent()
"Maps:
map <C-f> :FindInMRU<CR>
map <C-g> :GtagsFindFile 
nmap ga :ChangeBetweenHeaderAndcFile<CR>
nmap gd :FindSymbolDefine <C-R>=expand("<cword>")<CR><CR>
nmap gs :FindSymbol <C-R>=expand("<cword>")<CR><CR>
nmap gr :FindSymbolRef <C-R>=expand("<cword>")<CR><CR>
