#!/usr/bin/python
#-*- coding: utf-8 -*-
import time

VERSION = '1.0'
AUTHOR = 'Ziomioslaw'
DATE = '2007.08.05'
timeformat = "[%d %b %Y %H:%M:%S] "

class Loger:
	"""Klasa logera
	Odpowiedzialna za prowadzenia logu bota, bot zapisuje tam wszystko co uwazamy za wazne.
	"""
	def __init__( self, filename, terminator = '\n' ):
		""""Konstruktor" klasy Loger, zaklada plik logu, ustawia pewne zmienne.
		Funkcja przyjmuje:
			(string) nazwe pliku
			(znak)   terminator - czyli znak konczacy (parametr domyslny = '\n')
		Funkcja nie zwraca
		"""
		self.FileName = filename
		self.EndOfLine = terminator

		File = open( self.FileName, 'w' )
		File.write( '------------ :: Loger start :: ------------' + self.EndOfLine )
		File.close()

	def entry( self, txt ):
		"""Zapisz tekst do logu o okreslonej tresci
		Funkcja przyjmuje:
			(string) tresc tekstu do zapisu
		Funkcja nie zwraca
		"""
		File = open( self.FileName, 'at' )
		File.write(  time.strftime( timeformat, time.localtime() )  + txt + self.EndOfLine  )
		File.close()

	def warning( self, txt ):
		"""Zapisz wystapienie ostrzezenia (zostanie ono odpowiednio zaznaczone) do logu o okreslonej tresci
		Funkcja przyjmuje:
			(string) tresc tekstu do zapisu
		Funkcja nie zwraca
		"""
		self.Entry( '#WARNING: ' + txt )

	def error( self, txt ):
		"""Zapisz wystapienie bledu (zostanie ono odpowiednio zaznaczone) do logu o okreslonej tresci
		Funkcja przyjmuje:
			(string) tresc tekstu do zapisu
		Funkcja nie zwraca
		"""
		self.Entry( '#ERROR: ' + txt )


if __name__ == "__main__":
	print "Modul logera: klasa Loger", VERSION
	log = Loger( 'test.log' )

	log.Entry( 'Wpis testowy' )
	log.Warning( 'Wpis testowy - ostrzegawczy' )
	log.Error( 'Wpis testowy - o błędzie' )

	print "Przykład działania: plik 'test.log'"
	print AUTHOR, DATE
