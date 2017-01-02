#!/usr/bin/python
#-*- coding: utf-8 -*-
__author__="Ziomioslaw"
__date__ ="$2009-03-15 20:35:41$"
import re

namePattern = re.compile('^([^! ]+)!([^ ]+)')

class PersonStatus:
	"""Enum zawierający
	"""
    UNKNOWN = 0
    NONE = 1
    VOICE = 2
    OPERATOR = 3
    HALF_OPERATOR = 4

    def correction(status):
        return status >= PersonStatus.UNKNOWN and status <= PersonStatus.HALF_OPERATOR

    def setStatus(status):
        if PersonStatus.correction(status):
            return status
        else:
            raise InvalidStatusValue

class Person:
	"""
	"""

    def __init__(self, nameStr):
        matches = namePattern.match(nameStr)
        if matches != None:
            self.userNick = matches.group(1)
            self.userName = ''
            self.userHost = matches.group(2)
            self.userStatus = PersonStatus.UNKNOWN
        else:
            raise InvalidStringNameException

    def setPersonStatus(self, status):
        self.userStatus = PersonStatus.setStatus(status)

    def getPersonStatus(self):
        return self.userStatus

    def getPersonName(self):
        return self.userName

    def getPersonHost(self):
        return self.userHost

    def getPersonNick(self):
        return self.userNick

    def setPersonNick(self, nick):
        self.userNick = nick

class InvalidStringNameException(Exception):
    pass

class InvalidStatusValue(Exception):
    pass

if __name__ == "__main__":
    pass
