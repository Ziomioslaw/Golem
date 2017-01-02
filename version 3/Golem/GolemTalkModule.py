#!/usr/bin/python
#-*- coding: utf-8 -*-
from GolemActionModule import *

class GolemTalkModule(GolemActionModule):
    def newLineArrive(self, who, channel, line):
        """Obsługa zdarzenia pojawienia się nowej lini tekstu
        """
        pass

    def privateMessage(self, fromWho, line):
        """Obsługa prywatnej wiadomości do golema.
        """
        pass
