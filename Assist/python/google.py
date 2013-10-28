import webbrowser
import vim

def Google(query):
    if query is "":
        query = vim.eval('expand("<cword>")')
    print query
    url = "http://www.google.com/search?\&q=%s" % query
    webbrowser.open(url)

