#!/usr/bin/python
#-*- coding: utf-8 -*-
from Person import *

class PersonsManager:
    """Klasa zarzadza osabami na kanale.	
    """    
    def __init__(self):
        """Konstruktor
        """
        self.persons = {}
    
    def addPerson(self, person):
        """Dodaje nową osobę do klasy
        """
        pass

    def removePerson(self, person):
        """Usuwa osobę z klasy
        """
        pass
		
	def changePersonNick(self, nameString, newNick):
		"""
		"""	
		tmp = self.persons[nameString]
		del self.persons[nameString]
		self.persons[nameString.replace(tmp.getPersonNick(), newNick, 1)] = tmp;
		tmp.setPersonNick(newNick);		
        
    def getPerson(self, nameString):        
        """
        """
        if nameString in self.persons:
            return self.persons[nameString]
        else:
            newPerson = Person(nameString)
            self.persons[nameString] = newPerson
            return newPerson

if __name__ == "__main__":
    pass
