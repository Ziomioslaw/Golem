#!/usr/bin/python
#-*- coding: utf-8 -*-
from Golem.GolemTalkModule import *

class PrintChanelMessages(GolemTalkModule):
    def newLineArrive(self, who, channel, line):
        print channel, who.getPersonNick() + ':', line

def dynamicLoad():
	return PrintChanelMessages()
