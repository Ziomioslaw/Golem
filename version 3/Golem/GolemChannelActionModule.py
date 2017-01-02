#!/usr/bin/python
#-*- coding: utf-8 -*-
from GolemActionModule import *

class GolemChannelActionModule(GolemActionModule):
    def someoneArive(self, channel, person):
        """Obsługa zdarzenia pojawienia się kogoś.
        """
        pass
    
    def someoneLeaft(self, channel, person, reason):
        """Obsługa zdarzenie wyjścia kogoś.
        """
        pass
		
	def someoneChangeNick(self, who, newNick):
		"""Obsługa zdarzenia zmiany nicku przez kogoś
		"""
		pass

    def someoneQuit(self, person, reason):
        """Obsługa zdarzenia rozłączenia się kogoś.
        """
        pass

    def someoneKicked(self, channel, person, reason):
        """Obsługa zdarzenia wykopania kogoś.
        """
        pass

    def someoneBanned(self, person, ip, reason):
        """Obsługa zdarzenia zabanowania.
        """
        pass

	def topicChange(self, person, newTopic):
		pass
