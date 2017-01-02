#!/usr/bin/python
#-*- coding: utf-8 -*-
from Golem.GolemChannelActionModule import *
from Golem.GolemTalkModule import *
import time

timeformat = "[%d %b %Y %H:%M:%S] "

class LogModule(GolemChannelActionModule, GolemTalkModule):
	def __init__(self, channel):
		self.channel = channel
		self.FileName = 'test.log'
		self.EndOfLine = '\n'

	def getModulName(self):
		"""Zwraca nazwę tego modułu akcji
		\return Nazwę modułu akcji.
		"""
		return 'LogModule'

	def getVersionOfModule(self):
		"""Zwraca numer wersji tego modułu
		\return Numer wersji modułu
		"""
		return '0.01'

	def orderForModule(self, who, order):
		"""Obsługa polecenia wydanego dla tego modułu
		\return string jaki ma zostać wyświetlony
		"""
		pass

	def someoneArive(self, channel, person):
		"""Obsługa zdarzenia pojawienia się kogoś.
		"""
		if channel == self.channel:
			self.entry('Na kanał wszedł: %s' % person.getPersonNick())

	def someoneLeaft(self, channel, person, reason):
		"""Obsługa zdarzenie wyjścia kogoś.
		"""
		if channel == self.channel:
			self.entry('Kanał opuścił %s (%s)' % (person.getPersonNick(), reason))

	def someoneChangeNick(self, who, newNick):
		"""Obsługa zdarzenia zmiany nicku przez kogoś
		"""
		self.entry('%s od tej pory jest jako: %s' % (who.getPersonNick, newNick))

	def someoneQuit(self, person, reason):
		"""Obsługa zdarzenia rozłączenia się kogoś.
		"""
		if channel == self.channel:
			self.entry('%s rozłączył się (z tekstem: %s)' % (person.getPersonNick(), reason))

	def someoneKicked(self, channel, person, reason):
		"""Obsługa zdarzenia wykopania kogoś.
		"""
		if channel == self.channel:
			self.entry('%s został wykopany z kanału (powód: %s)' % (person.getPersonNick(), reason))
		pass

	def someoneBanned(self, person, ip, reason):
		"""Obsługa zdarzenia zabanowania.
		"""
		pass

	def topicChange(self, person, newTopic):
		self.entry('%s zmienił tematu kanału na: "%s"' % (person.getPersonNick(), newTopic))

	def newLineArrive(self, who, channel, line):
		"""Obsługa zdarzenia pojawienia się nowej lini tekstu
		"""
		if channel == self.channel:
			self.entry('< %s>:  %s' % (who.getPersonNick(), line))

	def entry(self, txt):
		f = open(self.FileName, 'at')
		f.write(time.strftime(timeformat, time.localtime()) + txt + self.EndOfLine)
		f.close()

def dynamicLoad():
	return LogModule()

if __name__ == "main":
	pass
