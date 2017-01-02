#!/usr/bin/python
#-*- coding: utf-8 -*-
from Golem.GolemTalkModule import *
import re

class OperatorModule(GolemTalkModule):
	def privateMessage(self, fromWho, line):
		if fromWho.getPersonNick() == 'Ziomioslaw':
			if line == 'zakończ pracę':
				self.golemInstance.quit()
			else:
				result = re.match('załaduj moduł ([A-Za-z]+)', line)
				if result != None:
					className = result.group(1)
					try:
						module = __import__('GolemAction.' + className, globals(), locals(), [className], -1)
						self.golemInstance.addAction(module.dynamicLoad())
						self.printMsg('Moduł %s został załadowany' % className)
						return
					except Exception:
						self.printMsg('Nie udało się załadować %s' % className)

	def printMsg(self, msg):
		self.golemInstance.sendPrvMsg(msg, 'Ziomioslaw')

def dynamicLoad():
	return ExitCommandAction()

if __name__ == "main":
	pass
