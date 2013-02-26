import vim

class BashAssist:
    activeBashNr = None
    @staticmethod
    def BashMode():
        if BashAssist.activeBashNr is None:
            vim.command("ConqueTerm bash")
            BashAssist.activeBashNr = vim.eval("bufnr('%')")
        else:
            vim.command("bn %s" %BashAssist.activeBashNr)
