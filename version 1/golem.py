#!/usr/bin/python
#-*- coding: utf-8 -*-

VERSION	= '0.0030'
AUTHOR	= 'Ziomioslaw'
DATE	= '2007.08.12'

import socket, time, re
import random
import config
import addons

import loger

endofline = '\r\n'

class Golem:
	"""Klasa Golem
	Klasa bota ircowego
	"""

	ifisConnect = false;

	def __init__( self, nick ):
		"""Inicjacja klasy golem
		"""
		self.start_time = time.time()
		self.nick = nick
		self.user = nick
		self.host = nick
		self.server = nick
		self.real = nick
		self.channel = ''
		self.fwd = { }
		self.operators = config.operators
		self.irc = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
		self.RecTmp = []

	def JoinoC(self, chanel):
		"""Dodanie nowego kanału, do listy
		"""
		self.channel = chanel;
		pass

	def Connect( self, network, port = config.port ):
		"""Polaczenie z serwerem IRC
		"""
		self.irc.connect ( ( network, port ) )
		self.irc.send ( ('NICK %s' + endofline) % self.nick )
		self.irc.send ( ('USER %s %s %s :%s' + endofline) % (self.user,self.host,self.server,self.real) )

	def Join( self, channel ):
		"""Wejscie na kanał
		"""
		self.channel = channel;
		self.irc.send ( ( 'JOIN %s' + endofline ) % self.channel )

	def PING( self, data ):
		"""Odeslanie pinga do serwera
		"""
		self.irc.send ( 'PONG ' + data.split() [ 1 ] + endofline )

	def Recivde( self ):
		"""Odebranie danych
		"""
		if ( self.RecTmp != [] ):
			return self.RecTmp.pop( 0 )

		while True:
			data = self.irc.recv ( 4096 )
			if data.find ( 'PING' ) != -1:
				self.PING(data)
			else:
				self.RecTmp = data.split( endofline )
				return self.RecTmp.pop( 0 )

	def IsOp( self, nick ):
		"""Sprawdzenie, czy podany nick jest operatorem
		Funkcja przyjmuje:
			(string) nick osoby sprawdzanej
		Zwraca:
			(boolen) czy nalzey do grupy operatorów bota.
		"""
		return ( nick in self.operators )

	def AddFwdMsg( self, who, msg ):
		"""
		"""
		if ( self.fwd.has_key( who ) ):
			self.fwd[ who ].Add( msg )
		else:
			self.fwd[ who ] =  addons.Notice( msg )

	def PrintFwdMsg( self, who ):
		"""
		"""
		if ( self.fwd.has_key( who.lower() ) ):
			msg = self.fwd[ who.lower() ]
			self.SendMsg ( who + "; wiadomosci do Ciebie:" )
			for i in range( len( msg.msgtab ) ):
				self.SendMsg( msg.msgtab[i] )

			del self.fwd[ who.lower() ]

	def SendMsg( self, msgt, who='' ):
		"""Wyslanie wiadomości.
		"""
		if ( who == '' ):
			who = self.channel
		self.irc.send( ('PRIVMSG %s :%s' + endofline) % (who, msgt) )

	def SendPrvMsg( self, msgt, who ):
		"""
		"""
		SendMsg( msgt, who )

	def Users( self ):
		"""Zwraca liste nickow (wraz z symbolami uprawien jakie te nicki maja) z kanalu, na jakim znajduje sie bot
		Funkcja nie przyjmuje paramteru
		Zwraca:
			(liste, tablice stringow) liste nikow
		"""
		nicklist = []
		self.irc.send( 'NAMES' + ' ' + config.chanel + endofline )
		while True:
			line = self.Recivde()

			if ( line.find( "End of /NAMES list." ) != -1 ):
				break
			else:
				i = line.find( self.channel + ' :' )
				if ( i != -1 ):
					nicklist += line[ ( i + self.channel.__len__() +2 ): ].split( )
		return nicklist

	def Names( self ):
		"""Zwraca liste nickow (bez symboli uprawien jakie nicki maja) z kanalu, na jakim bot jest
		Funkcja nie przyjmuje paramteru
		Zwraca:
			(liste, tablice stringow) liste nikow
		"""
		userlist = self.Users()
		for i in range( userlist.__len__() ):
			userlist[i] = userlist[i].lstrip( '@*+' )

		return userlist

	def Kick( self, who, reason='bo tak' ):
		"""Wykopuje uzytkonika z okreslonego powodu. Zeby funkcja zadziala, bot musi posiadac uprawienia operatora kanalu.
		Funkcja przyjmuje:
			(string) nick uzytkownika
			(string) przyczyna wykopania (wartosc domyslna "bo tak")
		Funkcja nic nie zwraca.
		"""
		self.irc.send(  "KICK " + self.channel + " " + who + " " + reason + endofline )

	def Leave( self ):
		"""Opuszczenie kanału.
		Funkcja nie przyjmuje i nie zwraca parametrow.
		"""
		self.irc.send( ( 'PART %s' + endofline ) % self.channel )

	def Quit( self ):
		"""Zakonczenie polaczenie.
		Funkcja nie przyjmuje i nie zwraca parametrow.
		"""
		self.irc.send( 'QUIT' + endofline )
		self.irc.close()

	def About( self ):
		"""Bot przedstawia sie.
		Funkcja nie przyjmuje i nie zwraca paramterowa.
		"""
		self.SendMsg( self.nick + " - IRCbot by Ziomioslaw :: Golem :: wersja: " + VERSION )
		self.SendMsg( "Pracuje juz: " + str( time.time() - self.start_time ) + "s" )
		self.SendMsg( "Obecne zadania: witam nowo przybylych," )
		self.SendMsg( "prowadzenie logow (modul jeszcze nie gotowy)," )
		self.SendMsg( "przekazywanie wiadomosci, przyjmowanie tematów SoTW" )
		self.SendMsg( "prowadzenie tabeli karm" )
		self.SendMsg( "Jestem wciaz w fazie testow - stad moge zachowywać się niestabilnie" )

	def CodingTest( self ):
		"""Fukcja służy do testownaia poprawności kodowania, wypisuje tekst z polskimi znakami dialektycznymi.
		Funkcja nie przyjmuje i nie zwraca paramterowa.
		"""
		self.SendMsg( "Zażółć gęślą jaźń :: 再见 :: Ελληνική γλώσσα" )


	#Nowy golem:
	actions = []

	def AddAction(self, action)
		"""
		"""
		if not instansceof(action, GolemActionClass):
			raise WrongGolemAction(action)
		else:
			self.action.append(action)

	def RemoveAction(self, action)
		"""
		"""
		if not instansceof(action, GolemActionClass):
			raise WrongGolemAction(action)
		else:
			if action in self.actions:
				self.action.remove(action)


if __name__ == "__main__":
	print "Modul golema: klasa Golem", VERSION
	print "Klasa bota IRCowego."
	print AUTHOR, DATE
