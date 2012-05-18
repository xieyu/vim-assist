import VimUtils

keyMaps={
		"MatchController":[
			("acceptSelect_e",["<cr>",]),
			("acceptSelect_h",["<c-cr>","<c-s>"]),
			("accetpSelect_t", ["<c-t>"]),
			("accetpSelect_v", ["<c-v>"], "<RightMouse>")
		],

		"PromptWindow":[
			("cancel",["<esc>", "<c-c>", "<c-g>"]),
			#del
			("bs", ["<BS>","<c-]>"]),
			("del",["<del>"]),
			("delWord", ["<c-w>"]),
			#cusor move
			("left", ["<c-h>", "<left>"]),
			("right", ["<c-l>", "<right>"]),
			("start", ["<c-a>"]),
			("end", ["<c-e>"]),
		]
}
#change it to yours
reposFilePath='%s/%s'%(VimUtils.getScriptDir(),"repos")
