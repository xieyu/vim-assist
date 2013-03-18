import subprocess

class OpenGLDocAssist:
    @staticmethod
    def Man(symbol):
        url = "http://www.opengl.org/sdk/docs/man/xhtml/%s.xml" % symbol
        subprocess.Popen("opera %s" % url, shell=True)
