import Controller
import VimUi

''''
This factory is famous for create normal components to make your life more comfortable....:D

@important:
	you must import SharedFactory in this way:
	from Factory import SharedFactory
	see MatchController and promptWindow 's doc for reason

@Attention: function in SharedFactory, will retun a shared object,
'''


class SharedFactory:
	promptWindow = VimUi.PromptWindow("SharedFactory.promptWindow")
	promptMatchController = Controller.PromptMatchController("SharedFactory.promptMatchController")
	@staticmethod
	def getPromptMatchController(title, finder, acceptor):
		'''Note, the returned matcher is shared, the the one you get before will be clean and be reused'''
		SharedFactory.promptMatchController.renew(title, finder, acceptor,
				SharedFactory.promptWindow)
		return SharedFactory.promptMatchController


