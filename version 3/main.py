#!/usr/bin/python
#-*- coding: utf-8 -*-
from Golem.GolemMainClass import *
from GolemAction.ExitCommandAction import *
from GolemAction.OperatorModule import *
from GolemAction.LogModule import *

channel = '#testGolem'

golem = GolemMainClass('testGolem')#'Sholem')
golem.connect('irc.freenode.net', 6667)
golem.join(channel)
golem.addAction(ExitCommandAction('!end!'))
golem.addAction(OperatorModule())
golem.addAction(LogModule(channel))
golem.run()

print "Test przeszedł."
