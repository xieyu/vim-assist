
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

command! -nargs=1 SetTagFile 		   py tag_locate_driver.setTagFile(<q-args>)
command! -nargs=1 FindTagByFullName    py tag_locate_driver.findTagByFullName(<q-args>)
"Maps:
map <C-f> :FinderFile<CR>

