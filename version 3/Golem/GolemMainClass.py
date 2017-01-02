#!/usr/bin/python
#-*- coding: utf-8 -*-
from IrcSocket import *
from PersonsManager import *
from GolemTalkModule import *
from GolemChannelActionModule import *
import re

commonLinePattern = re.compile('^:([^ ]+) ([0-9]*) ?([^ ]+) (.*)$')

class GolemMainClass:
	"""Klasa Golem
	Klasa bota ircowego
	"""

	def __init__(self, nick):
		"""Inicjacja klasy golem
		"""
		# Akcje jakie przetrzymuje Golem.
		self.talkListeners = []
		self.channelActionsListeners = []		
		# Głowny socket - przez niego bot łączy się z sieciom
		self.irc = IrcSocket()
		self.nick = nick
		self.user = nick
		self.host = nick
		self.server = nick
		self.real = nick
		self.channel = ''
		self.recTmp = []
		self.personsManager = PersonsManager()
		self.connectionStatus = False
		''' nieznane przeznaczenie.
		self.start_time = time.time()
		self.fwd = { }
		self.operators = config.operators
		'''

	def connect(self, network, port):
		"""Polaczenie z serwerem IRC
		"""
		self.irc.connect(network, port)
		self.irc.send(('NICK %s') % self.nick)
		self.irc.send(('USER %s %s %s :%s') % (self.user, self.host, self.server, self.real))
		self.connectionStatus = True

	def join(self, channel):
		"""Wejscie na kanał
		"""
		self.channel = channel;
		self.irc.send ('JOIN %s' % self.channel)

	def received(self):
		"""Odebranie danych
		"""
		s = self.irc.received()
		
		print s
		
		matches = commonLinePattern.match(s)
		if matches != None:
			if matches.group(2) == '':
				self.parser(matches.group(1), matches.group(3), matches.group(4))
			else:
				self.errorReplies((int)(matches.group(2)), matches.group(3), matches.group(4))
	
	def errorReplies(self, number, toWho, message):
		"""
		TODO: dokończyć
		"""
		print "Error Replies - numer: %s, toWho: %s %s" % (number, toWho, message)
	
	def run(self):
		"""
		"""
		while self.connectionStatus:
			self.received()
	
	def parser(self, name, command, params):
		"""Metoda parsuje tekst komendy i rozsyła je do obserwatorów
		"""
		if command == 'PRIVMSG':
			# Nowa wiadomość
			params = params.split(' :')
			if params[0] == self.nick:
				# Wiadomość prywatna
				for action in self.talkListeners:
					action.privateMessage(self.personsManager.getPerson(name), params[1])
			else:
				# Wiadomość na jakiś kanał
				for action in self.talkListeners:
					action.newLineArrive(self.personsManager.getPerson(name), params[0], params[1])
			return
			
		elif (command == 'JOIN'):
			# Ktoś wchodzi na kanał		 
			params = params.split(' :')
			for action in self.channelActionsListeners:
				action.someoneArive(params[0], self.personsManager.getPerson(name))
			return			
		elif (command == 'PART'):
			# Ktoś opuszcza kanał
			for action in self.channelActionsListeners:
				action.someoneLeaft(params[0], self.personsManager.getPerson(name), params[1])
			return
		elif (command == 'MODE'):
			# 
			pass
		elif (command == 'TOPIC'):		  
			# Zmiana tematu na kanale
			params = params.split(' :') # nazwa kanału, nowy temat na kanale
			for action in self.channelActionsListeners:
				action.topicChange(params[0], params[1])
			return
			
		elif (command == 'NICK'):
			# Ktoś zmienia sobie nick
			
			return
		elif (command == 'NAMES'):
			# 
			pass
		elif (command == 'LIST'):
			# 
			pass
		elif (command == 'INVITE'):
			# 
			pass
		elif (command == 'KICK'):
			# 
			pass
		elif (command == 'NOTICE'):
			# 
			pass
	
	def users(self):		
		"""Zwraca liste nickow (wraz z symbolami uprawien jakie te nicki maja) z kanalu, na jakim znajduje sie bot
		Funkcja nie przyjmuje paramteru
		Zwraca:
			(liste, tablice stringow) liste nikow
		nicklist = []
		self.irc.send( 'NAMES' + ' ' + config.chanel)
		while True:
			line = self.Recivde()
			if ( line.find( "End of /NAMES list." ) != -1 ):
				break
			else:
				i = line.find( self.channel + ' :' )
				if ( i != -1 ):
					nicklist += line[ ( i + self.channel.__len__() +2 ): ].split( )
		return nicklist
		"""
		pass

	def sendMsg(self, msgt, who=''):
		"""Wyslanie wiadomości.
		"""
		if ( who == '' ):
			who = self.channel
		self.irc.send( ('PRIVMSG %s :%s') % (who, msgt) )

	def sendPrvMsg(self, msgt, who):
		"""
		"""
		self.sendMsg(msgt, who)

	def kick( self, who, channel, reason='bo tak'):
		"""Wykopuje uzytkonika z okreslonego powodu. Zeby funckja zadziala, bot musi posiadac uprawienia operatora kanalu.
		Funkcja przyjmuje:
			(string) nick uzytkownika
			(string) przyczyna wykopania (wartosc domyslna "bo tak")
		Funkcja nic nie zwraca.
		"""
		self.irc.send("KICK " + channel + " " + who + " " + reason)

	def leave(self, channel):
		"""Opuszczenie kanału.
		Funkcja nie przyjmuje i nie zwraca parametrow.
		"""
		self.irc.send(('PART %s') % channel)

	def quit(self):
		"""Zakonczenie polaczenie.
		Funkcja nie przyjmuje i nie zwraca parametrow.
		"""
		self.irc.send('QUIT')
		self.connectionStatus = False
		self.irc.close()

	def addAction(self, action):
		"""Dodanie nowej akcji do Golema.
		"""
		if isinstance(action, GolemTalkModule):
			self.talkListeners.append(action)	   
		if isinstance(action, GolemChannelActionModule):
			self.channelActionsListeners.append(action)	 
		if not isinstance(action, GolemActionModule):
			raise WrongActionException(action)
		else:
			action.install(self)

	def removeAction(self, action):
		"""Usunięcie akcji z Golema.
		"""
		if isinstance(action, GolemTalkModule):
			self.talkListeners.remove(action)	   
		if isinstance(GolemChannelActionModule):
			self.channelActionsListeners.remove(action)	 
		if not isinstance(action, GolemActionModule):
			raise WrongActionException(action)
		else:
			action.uninstall(self)

	def getAction(self, actionName):
		"""Zwraca akcje o podanej nazwie, o ile została załadowana.
		\return Akcja o podanej nazwie.
		"""
		raise Exception("Not implemented!")

class GolemException(Exception):
	"""Klasa bazowa wyjatków golema
	"""
	pass

class GolemWrongActionException(GolemException):
	"""Wyjątek występuje kiedy ktoś każe załadować golemowi nie
	prawidłowy obiekt akcji.
	"""
	pass
