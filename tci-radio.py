#!/usr/bin/python3
'''
Autor: Thoams Cigolla, 10.01.2021
Version: 0.1

Ein kleines Programm um ein eigenes Radioprogramm zu erzeugen.
Das Programm bietet die Möglichkeit zu bestimmten Zeitpunkten
automatisch den Sender zu wechseln. 
Das ist Praktisch wenn man wärend der Arbeit nicht duch 
Gespräche gestört werden möchte aber die wichtigsten Nachrichten
trotz dem nicht verpassen will.

Voraussetzungen:

Es muss das Komandline Program mpg123 instaliert und im Path vorhanden sein.
https://www.mpg123.de/
Zusätzlich wird das Python Modul schedul benötigt.
https://github.com/dbader/schedule

Copyright 2021 Thomas Cigolla <tcicit@gmail.com>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
MA 02110-1301, USA.

'''
import subprocess
import shlex
import time
import sys
import schedule
from datetime import datetime

'''
Global variable for process id
Das Modul schedule untersützt leider keine return-codes deshalb muss 
man mit globalen Variabeln arbeiten.
'''
p = 0 

######################### Radisender #############################
radio_urls = {
	"srf1_gr" : shlex.split( "mpg123 -@ http://stream.srg-ssr.ch/regi_gr/mp3_128.m3u" ),
	"swiss_pop" : shlex.split("mpg123 -@ http://stream.srg-ssr.ch/rsp/mp3_128.m3u" )
	}

######################## Schedules ###############################
# Zeit von, bis, Sender gemäss Senderliste (radoo_urls)
# Achtung für den Tageswechsel sollte 00:00 h verwendet 
# werden und nicht 24:00 h
timeschema = [
	("00:00", "12:30", "swiss_pop"),
	("12:30", "13:00", "srf1_gr"),
	("13:00", "16:00", "swiss_pop"),
	("16:00", "19:00", "srf1_gr"),
	("19:00", "00:00", "swiss_pop")
    ]

######################## functions ###############################
def find_start_radio(timeschema):
	now = datetime.now()
	cuTime = now.strftime("%H%M")

	for t in timeschema:
		tt = (t[1].replace(':', ''))
		
		if (int(cuTime) < int(tt)):
			return t[2]
			break
    
def start_radio(url_radio):
	global p
	p = subprocess.Popen(url_radio)

def kill_radio():
	global p
	p.kill()

def stop_start_radio(url_radio):
	global p
	kill_radio()
	p = subprocess.Popen(url_radio)
	
def set_schedules(timeschema):
	for t in timeschema:
		schedule.every().day.at(t[0]).do(stop_start_radio, radio_urls[t[2]])

####################### Set Schedules ##################################
set_schedules(timeschema)
print ("Schow registert jops")
for s in schedule.jobs:
	print (s)

########################## START ###################################

cur_radio = find_start_radio(timeschema)
start_radio(radio_urls[cur_radio])

while True:
	try:
		schedule.run_pending()
		time.sleep(1)
		
	except KeyboardInterrupt:
		kill_radio()
		break

sys.exit(0)
