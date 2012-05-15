import VimUtils

keyMaps={
		"MatchController":[
		("<C-j>", "selectPre"),
		("<C-p>", "selectPre"), #Don't know why C-p does NOT work
		("<C-n>","selectNext"), 
		("<Up>", "selectPre"),
		("<Down>", "selectNext"),
		("<CR>", "openInOldWinThenHideSelf"),
		("<C-o>","openInOldWin"),
		("<C-t>","openInNewTab"),
		],

		"PromptWindow":[
		("<ESC>","cancel"),
		("<Left>","left"),
		("<Right>","right"),
		("<C-a>", "home"), 
		("<C-e>","end"),
		("<C-h>","left"),
		("<C-l>","right"),
		("<BS>","bs"), 
		("<Del>","del"), 
		("<C-d>","del"),
		("<C-k>","kill"),#like emacs way, del from cursor to end
		]
}
#change it to yours
reposFilePath='%s/%s'%(VimUtils.getScriptDir(),"repos")
