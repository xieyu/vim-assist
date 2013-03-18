import subprocess

class OpenGLDocAssist:
    @staticmethod
    def Man(symbol):
        url = "http://www.opengl.org/sdk/docs/man/xhtml/%s.xml" % symbol
        subprocess.Popen("opera %s" % url, shell=True)

class GoogleSearch:
    @staticmethod
    def Search(symbol):
        #use opera defaulter searcher
        subprocess.Popen("opera %s" % symbol, shell=True)
        
