import subprocess
import vim

class GitAssit:
    @staticmethod
    def gitCmd(cmd_args):
        cmd = ["git"] + cmd_args
        output = subprocess.check_output(cmd)
        return output
    @staticmethod
    def gitkCmd(cmd_args):
        cmd = ["gitk"] + cmd_args
        subprocess.Popen(cmd)
        return

    @staticmethod
    def gitBlame(filePath):
        return GitAssit.gitCmd(["blame",filePath])

    @staticmethod
    def gitkCurrentLine():
        filePath = vim.current.buffer.name
        if filePath:
            lineNum = int(vim.eval("line('.')"))
            blames = GitAssit.gitBlame(filePath).split("\n")
            commitHash = blames[lineNum -1].split()[0]
            GitAssit.gitkCmd([commitHash.strip(),"-5"])

        pass
    @staticmethod
    def gitkLogCurrentBuffer():
        filePath = vim.current.buffer.name
        if filePath:
            GitAssit.gitkCmd(["-p", filePath])
