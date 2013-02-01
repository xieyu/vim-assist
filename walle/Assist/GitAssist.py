import subprocess
import vim

class GitAssist:
    @staticmethod
    def gitCmd(cmd_args):
        cmd = "git %s" % cmd_args
        process = subprocess.Popen(cmd, stdout = subprocess.PIPE, shell = True)
        output = process.stdout.read()
        del process
        return output

    @staticmethod
    def gitkCmd(cmd_args):
        cmd = "gitk %s" % cmd_args
        subprocess.Popen(cmd, shell=True)
        return

    @staticmethod
    def gitBlame(filePath):
        return GitAssist.gitCmd("blame %s" % filePath)

    @staticmethod
    def gitkCurrentLine():
        filePath = vim.current.buffer.name
        if filePath:
            lineNum = int(vim.eval("line('.')"))
            blames = GitAssist.gitBlame(filePath).split("\n")
            commitHash = blames[lineNum -1].split()[0]
            GitAssist.gitkCmd("%s %s" %(commitHash.strip(),"-3"))

    @staticmethod
    def gitkLogCurrentBuffer():
        filePath = vim.current.buffer.name
        if filePath:
            GitAssist.gitkCmd("-p %s" % filePath)
