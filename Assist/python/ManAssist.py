import subprocess
from Common import SettingManager

class OpenGLDocAssist:
    @staticmethod
    def Man(symbol):
        browser = SettingManager.getBrowser()
        url = "http://www.opengl.org/sdk/docs/man/xhtml/%s.xml" % symbol
        subprocess.Popen("%s %s" % (browser, url), shell=True)

class GoogleSearch:
    @staticmethod
    def Search(symbol):
        browser = SettingManager.getBrowser()
        url = "http://www.google.com/search?\&q=%s" % symbol
        subprocess.Popen("%s %s" % (browser, url), shell=True)

class OperaBts:
    @staticmethod
    def browserBug(bugNumber):
        browser = SettingManager.getBrowser()
        url = "http://bugs.opera.com/browse/SPX-%s" % bugNumber
        subprocess.Popen("%s %s" % (browser, url), shell=True)

class StackOverFlow:
    @staticmethod
    def Search(symbol):
        browser = SettingManager.getBrowser()
        url = "http://stackoverflow.com/search?q=%s" % symbol
        subprocess.Popen("%s %s" % (browser, url), shell=True)

        
