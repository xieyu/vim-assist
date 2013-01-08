import string
class CommonUtil:
    @staticmethod
    def fileStrokeMatch(key_stroke, filePath):
        index = 0
        s = filePath.lower()
        strokes = key_stroke.lower()
        for key in strokes:
            index = string.find(s, key, index)
            if index == -1:
                return False
        return True

def myAssert(condition, message=""):
    if condition:
        print message, "pass"
    else:
        print message, "fail"

if __name__=="__main__":
    myAssert(CommonUtil.fileStrokeMatch("hwd", "hello world"))
    myAssert(CommonUtil.fileStrokeMatch("oWd", "hello world"))
