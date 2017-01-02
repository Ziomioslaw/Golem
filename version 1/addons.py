#!/usr/bin/python
#-*- coding: utf-8 -*-

class PointsTab:
	"""Klasa PointTab:
	Czyli lista nikcow z ich "karmom" odpowiednio dobra i zla.
	"""
	def __init__( self ):
		"""Zaczynamy od przygotowania tablicy, wczytujemy jesli poprzednio ta klasa byla uzywana
		Funkcja nie przyjmuje parametru, nic nie zwraca
		"""
		self.NickTab = {}
		# sprawdzenie czy plik wynikow istnial
		# wczytanie z pliku

	def Add( self, nick, set = 1 ):
		"""Uzytkownik [nick] zaskarbil sobie przychylnosc operatora:) + do dobrej karmy
		Funkcja przyjmuje:
			(string) nick osoby
			(liczba calkowita) o ile zwiekszyc (domyslna wartosc = 1)
		Zwraca
			(liczba calkowita) jej dobra karme po dodaniu
		"""
		# Dla ujednolicenia:
		nick = nick.capitalize()
		if ( self.NickTab.has_key( nick ) ):
			# Dodajemy mu + dobrej
			self.NickTab[ nick ][0] += set
		else:
			# Ustawiamy 1 dobrej karmy
			self.NickTab[ nick ] = [ set, 0 ]

		return self.NickTab[ nick ][0]

	def Sub( self, nick, set = 1 ):
		"""Uzykownik [nick] cos przeskrobal - dostaje + do zlych uczynkow
		Funkcja przyjmuje:
			(string) nick osoby
			(liczba calkowita) o ile zwiekeszyc (domyslna wartosc = 1)
		Zwraca
			(liczba calkowita) jej zla karme po dodaniu
		"""
		# Dla ujednolicenia
		nick = nick.capitalize()
		if ( self.NickTab.has_key( nick ) ):
			# Dodajemy mu + zlej
			self.NickTab[ nick ][1] += set
		else:
			# Ustawiamy 1 zlej karmy
			self.NickTab[ nick ] = [ 0, set ]

	def Reset( self, nick ):
		"""Wymazanie karmy uzytkownika [nick]
		Funkcja przyjmuje:
			(string) nick osoby
		Nic nie zwraca
		"""
		# Dla ujednolicenia
		nick = nick.capitalize()
		del self.NickTab[ nick ]

	def Reset( self ):
		"""Wymazanie karmy wszystkich uzytkownikow
		Funkcja nie przyjmuje i nie zwraca parametrow
		"""
		self.NickTab = []

	def List( self ):
		"""Zagladamy na liste karmy.
		Funkcja nie przyjmuje parametrow
		Zwraca:
			(tablica stringow) liste: [ '[nick] +[ile dobrej] -[ile zlej] =[ile dobrej - ile zlej]', ... ]
		"""
		strList = []

		for i in self.NickTab:
			strList.append( i + " +" + str( self.NickTab[i][0] ) + " -" + str( self.NickTab[i][1] ) +
					" =" + str( self.NickTab[i][0] - self.NickTab[i][1] ) )

		return strList

	def Save( self ):
		"""Zachowujemy nasz liste karm do pliku, z ktorego potem moze ta liste odczytac.
		Funkcja nie przyjmuje i nie zwraca parametrow
		"""
		file = open( 'karma.txt', 'wt' )
		for i in self.NickTab:
			file.write( i + ":" + str( self.NickTab[i][0] ) + ":" + str( self.NickTab[i][1] ) + '\n' )
		file.close()

	def Load( self ):
		"""Odczytujemy zachowana wczesniej liste karm
		Funkcja nie przyjmuje i nie zwraca parametrow
		"""
		file = open( 'karma.txt', 'rt' )
		try:
			for line in file:
				line = line.split( ':' )

				self.Add( line[0], int( line[1] ) )
				self.Sub( line[0], int( line[2] ) )

		finally:
			file.close()

class Notice:
	"""Klasa Notice
	Klasa wiadomosci zostawianej dla uzytkownika
	"""
	def __init__( self, msg ):
		"""Inicjacja klasy, nowa klasa odrazu dostaje wiadomosc do zapisu.
		Funkcja przyjmuje:
			(string) tresc wiadomosci
		Funckja nic zwraca
		"""
		self.msgtab = [ ]

		self.Add( msg )

	def Add( self, msg ):
		"""Dodaje tekst wiadomosci o okreslonej tresci.
		Funkcja przyjmuje:
			(string) tresc wiadomosci
		Funckja nic zwraca
		"""
		self.msgtab.append( msg )

class SoTW:
	"""Klasa przetrzymujaca
	"""
	def __init__( self ):
		"""Inicjator klasy SoTW
		Funkcja nie przyjmuje i nie zwraca tematow
		"""
		self.SoTWList = []

	def Add( self, nick, subject ):
		"""Dodanie nowego tematu do listy istniejacych
		Funkcja przyjmuje:
			(string) nick - kto zaproponowal
			(string) nowy temat
		Funkcja nic nie zwrca.
		"""
		subject = nick + ': ' + Sb
		self.SoTWList.append( subject )

	def Del( self, what ):
		"""Usuwanie pasuj?cych do wzorca tematow SoTW
		"""
		_sotwtab = []
		delnr = 0

		for i in range( len( sotwtab ) ):
			if sotwtab[i].find( what ) == -1:
				_sotwtab.append( sotwtab[i] )
			else:
				delnr += 1

		sotwtab = _sotwtab
		return delnr

	def List( self ):
		"""Funckcja zwraca list? tematow
		Funkcja nie przyjmuje parametrow
		Zwraca:
			(liste stringow) liste tematow
		"""
		return self.SoTWList

	def Save( self ):
		"""
		"""
		file = open( 'sotw.txt', 'wt' )
		for i in self.SoTWList:
			file.write( i + '\n' )
		file.close()

	def Load( self ):
		"""
		"""
		file = open( 'sotw.txt', 'rt' )
		try:
			for line in file:
				self.SoTWList.append( line )
		finally:
			file.close()

class Questionnaire:
	"""Klasa obslugująca ankiete
	"""
	def __init__( self ):
		self.Clean()
		return

	def Clean( self ):
		self.is_poll = False
		self.poll_str = ''
		self.poll_yes_andserw = 0
		self.poll_no_andserw = 0
		self.who_andserw = []
		return

	def Is( self ):
		return self.is_poll

	def CheckWhoAndserw( self, nick ):
		return (nick in self.who_andserw)

	def Ask( self ):
		return self.poll_str

	def AddNewQuestion( self, ask_str ):
		self.is_poll = True
		self.poll_str = ask_str
		return

	def GiveYes( self, nick ):
		if self.is_poll:
			self.poll_yes_andserw += 1
			self.who_andserw.append( nick )
		return

	def GiveNo( self, nick ):
		if self.is_poll:
			self.poll_no_andserw += 1
			self.who_andserw.append( nick )
		return

	def About( self ):
		if self.is_poll:
			return "Ankieta: \"" + poll_str + "\" wyniki: \nTak: " + str(self.poll_yes_andserw) + " Nie: " + str(self.poll_no_andserw)
		else:
			return "Nie ma aktualnie żadnej ankiety"

	def Kill( self ):
		if self.is_poll:
			return "Nie ma aktualnie żadnej ankiety"
		else:
			self.Clean();
			return "Ankieta została usunięta"


import os

class SaveList:
	"""
	"""
	filename = ""
	list = ""

	def __init__( self, filename ):
		"""
		"""
		self.list = []
		self.filename = filename
		self.Load()

	def Add( self, string ):
		"""
		"""
		self.list.append( string )

	def Del( self, string ):
		"""
		"""
		_list = []
		delnr = 0

		for i in range( len( self.list ) ):

			if self.list[i].find( string ) == -1:
				_list.append( self.list[i] )
			else:
				delnr += 1

		self.list = _list
		return delnr

	def Save( self ):
		"""
		"""
		file = open( self.filename, 'wt' )
		for i in self.list:
			file.write( i + '\n' )
		file.close()

	def Load( self ):
		"""
		"""
		if ( os.path.isfile( self.filename ) ):
			file = open( self.filename, 'rt' )
			try:
				for line in file:
					self.list.append( line )
			finally:
				file.close()

	def Clean( self ):
		"""
		"""
		self.list = []
		self.Save()
