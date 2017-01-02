#!/bin/python
#-*- coding: utf-8 -*-

VERSION = '0.0031'

import config
import golem
import loger
import addons
import time
import re
import random

endofline = '\r\n'

loger.timeformat = config.timeformat
Log = loger.Loger( "ircbot.log" )
Siraiye = golem.Golem( config.nick )
Siraiye.Connect( config.network )
Siraiye.SendMsg(  "IDENTIFY " + config.nick_pass, "NickServ" )
Siraiye.Join( config.chanel )
#logfile = open('log.txt','wt')

print "ok"
sotwtab = addons.SaveList( "sowt" )
karma = addons.PointsTab()
karma.Load()

is_poll = False
poll_str = ''
poll_yes_andserw = 0
poll_no_andserw = 0
who_andserw = []

Poll = addons.Questionnaire()

while True:
	data = Siraiye.Recivde()
	print data

	nick = data.split ( '!' ) [ 0 ].replace ( ':', '' )

	if data.find( 'JOIN' ) != -1:
		if ( nick != Siraiye.nick ):
			time.sleep( random.randint(3,8) )
			Siraiye.SendMsg ( random.choice( ['Aloha','Ai', 'גוט מאָרגן',  'დილა მშვიდობისა', 'Kaixo', 'доброго ранку', 'Günaydin', 'Tervist','Moi', '你好', 'Γεια σου', 'здрав', 'नमसते',  'Tere', 'おはよう', 'Salute', 'Hi','Hello', 'En taro adun', 'Cześć', 'Witaj', 'Hej', 'Cze'] ) + ' ' + nick)
			Siraiye.PrintFwdMsg( nick )
			if Poll.Is():
				if not Poll.CheckAndserw( nick ):
					Siraiye.SendMsg( "Witaj, czy weźmiesz udział w ankiecie? Jeśli tak, odpowiedź na poniższe pytanie pisząc tutaj: tak lub nie, jesli nie chcesz odpowiedać - zignoruj tą wiadomość. Dziekuje:)", nick )
					Siraiye.SendMsg( Poll.Ask(), nick )
		else:
			Siraiye.SendMsg ( "Cześć" )

	elif data.find ( 'PRIVMSG' ) != -1:
		message = ':'.join ( data.split ( ':' ) [ 2: ] )

		if Siraiye.IsOp( nick ):
			tmp = re.findall( config.chanel + " :.*[-+]", data )

			if ( tmp != None ) and ( tmp != [] ):
				person = tmp[0][ (config.chanel.__len__() +2) :]

				print person[:-1]

				if ( person[:-1] in Siraiye.Names() ):
					Log.Entry( nick + ": " + person )
					if ( person[-1:] == '+' ):
						karma.Add( person[:-1] )
					if ( person[-1:] == '-' ):
						karma.Sub( person[:-1] )
					if ( person[-1:] == '0' ):
						karma.Reset( person[:-1] )

				karma.Save()

	if data.find( 'PRIVMSG ' + Siraiye.nick ) != -1:
		# Czyli prywatana wiadomosc do Siraiye
		if ( nick == config.owner ):
			# Prywatna wiadomosc od wlasciciela
			if data.find('!say') != -1:
				tmp = data.split( Siraiye.nick + ' :!say ' )
				if ( len( tmp ) > 1 ):
					Siraiye.SendMsg( tmp[1] )
				continue

		if nick == config.owner:
			if data.find('!kick') != -1:
				tmp = data.split( Siraiye.nick + ' :!kick ' )
				if len( tmp ) > 1:
					tmp = tmp[1].split()
					if len( tmp ) > 1:
						Siraiye.Kick(tmp[0], tmp[1])
					else:
						Siraiye.Kick(tmp[0],'')

		if Siraiye.IsOp( nick ):
			if data.find('!poll') != -1:
				tmp = data.split( Siraiye.nick + ' :!poll ' )
				if len(tmp) > 1:
					Poll.AddNewQuestion( tmp[1] )
					Siraiye.SendMsg( "Ankieta:", nick )
					Siraiye.SendMsg( tmp[1], nick )
					Siraiye.SendMsg( "została dodana", nick )
					continue
		if is_poll:
			if data.find('tak') != -1:
				Poll.GiveYes( nick )

			if data.find('nie') != -1:
				Poll.GiveNo( nick )

	if data.find( '!ends!' ) != -1:
		if ( nick == config.owner ):
			Siraiye.SendMsg( "Było miło, ale czas na mnie.")
			Siraiye.Leave()
			Siraiye.Quit()
			Log.Entry( "Koniec" )
			exit(0);
		else:
			Siraiye.Kick( nick, "precz z lapami" )
			Log.Warning( nick + " próbował podszyć się pod właściciela (!ends!)" )

	if data.find( '!karma!' ) != -1:
		if Siraiye.IsOp( nick ):
			list = karma.List()
			if ( list != [] ):
				for i in list:
					Siraiye.SendMsg( i )
			else:
				Siraiye.SendMsg( "Nie ma na razie żadnych karm", nick )

	if data.find( Siraiye.nick + ': fwd:' ) != -1:
		tmp = re.findall( ": fwd:.*", data )[0][7:]
		ToNick, Msg = tmp.split( ' ',  1 )
		ToNick = ToNick.lower()
		Log.Entry( nick + " zostawił " + ToNick + " wiadomość: " + Msg )
		Msg = "(Od: " + nick + "): " + Msg
		Siraiye.AddFwdMsg( ToNick, Msg )
		Siraiye.SendMsg( "Potwierdzam przyjecie wiadomosci (%s) do użytkownika %s" % (Msg, ToNick), nick )

	if data.find( Siraiye.nick + ': SoTW:' ) != -1:
		Subject = re.findall( ": SoTW:.*",data )[0][8:]

		if Subject.find('!del') == -1 :
			Siraiye.SendMsg( "Temat (%s) przyjęty" % (Subject), nick )
			Log.Entry( nick + " dodał nowy temat SoTW: " + Subject )
			Subject = nick + ': ' + Subject
			sotwtab.Add( Subject )
		else:
			if Siraiye.IsOp( nick ):
				what = Subject.split( ' ', 1 )[1]
				delnr = sotwtab.Del( what )

				if delnr != 0:
					Siraiye.SendMsg( "Usunięto %d tematów zgodnych z wzorcem %s" % ( delnr, what ) )
					Log.Entry( "Usunięto z sotw: " + what )
				else:
					Siraiye.SendMsg( "Nie znaleziono pasującego wzorca" )
					Log.Entry( "Próbowano usunąć: " + what )
			else:
				Siraiye.SendMsg( "Nie masz odpowiednich uprawnień" )
				Log.Warning( nick + " próbował podszyć się pod właściciela (!del)" )

		sotwtab.Save();

	if data.find( '!sotw!' ) != -1:
		if Siraiye.IsOp( nick ):
			sotwtab.Load()
			if len( sotwtab.list )  == 0:
				Siraiye.SendMsg( "Nikt nie zaproponował żadnego tematu na SoTW" )
			for i in range( len( sotwtab.list ) ):
				Siraiye.SendMsg( sotwtab.list[i] )

	if data.find( '!info!' ) != -1:
		if Siraiye.IsOp( nick ):
			Siraiye.About()

	if data.find( '!pollstat!' ) != -1:
		if Siraiye.IsOp( nick ):
			Siraiye.SendMsg( Poll.About() )

	if data.find( '!killpoll!' ) != -1:
		if Siraiye.IsOp( nick ):
			Siraiye.SendMsg( Poll.Kill(), nick )

	if data.find( '!test!' ) != -1:
		if Siraiye.IsOp( nick ):
			Siraiye.CodingTest()
