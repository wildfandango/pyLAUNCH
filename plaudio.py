# -*- coding: iso-8859-15 -*-

import random,os,pygame,plconfig,plfiles
from pygame.locals import *

# La finalidad de esta clase es gestionar las m�sicas y los efectos de sonido
class jukeBOX:
	"""Objeto encargado de gestionar las m�sicas y listas de reproducci�n
	Devuelve: un objeto del tipo jukeBOX
	Funciones: read, write, explore, play, pause, stop, nect, prev, loop, end
	Atributos: path,suffle,playlist,song,volumen,paused,musictypes,cfgFILE,actsngNAME"""

	def __init__(self, musicDIR,cfgPATH="",suffle=True,volume=0.5,types=(".mp3",".ogg",".mod",".xm",".mid",".s3m",".wav"),samplerate=44100,cfgsection="JUKEBOX"):
		"""incializaci�n de del objeto"""
		self.path = musicDIR				# Ruta que contiene los ficheros de m�sica
		self.suffle = suffle				# Reproducir de forma aleatoria?
		self.playlist	= []					# Lista de reproducci�n (vac�a)
		self.song = 0					# Indice de la canci�n que se est� reproduciendo
		self.volume = volume				# Volumen de reproducc�on de la m�sica
		self.paused = False				# Indica si la m�sica est� pausada
		self.musictypes = types			# Tipos de m�sica que se buscar�n
		
		# Para el control del estado/posici�n de reproducci�n al salir/entrar
		self.cfgFILE = cfgPATH				# Ruta del fichero de configuraci�n de control
		self.section = cfgsection			# Secci�n del fichero de configuraci�n
		self.actsngNAME = ""				# Nombre del fichero que se est� reproduciendo
		self.actsngPOS = 0				# Posici�n en la que se est� reproduciendo
		
		pygame.mixer.pre_init(samplerate,-16,2,1024*2)
		pygame.mixer.init()
		pygame.mixer.music.set_volume(self.volume)
		self.explore()					# Busco los ficheros de m�sica en el directorio indicado
		self.read()						# Restauro posiciones, solo despu�s de explorar

	def read(self):
		"""Lee la configuraci�n (recuperando la cancion que se estaba rerpoduciendo) y establece los puntos de reproducci�n"""
		if (len(self.cfgFILE) > 0) and (len(self.playlist) > 1):
			cfgOBJ = plconfig.iniCFG(self.cfgFILE,self.section)
			self.actsngNAME = cfgOBJ.getcfg("actual_song_name","")
			#self.actsngPOS = eval(cfgOBJ.getcfg("actual_song_position","0"))
			# Si se estaba reproduciendo algo, recupero ese elemento
			if (len(self.actsngNAME) > 0):
				try: self.song = self.playlist.index(self.actsngNAME)
				except: self.actsngPOS = 0

	def write(self):
		"""Guarda la configuraci�n (recordando la cancion que se estaba rerpoduciendo)"""
		if (len(self.cfgFILE) > 0) and (len(self.playlist) > 0):
			if (not self.paused): self.pause()
			cfgOBJ = plconfig.iniCFG(self.cfgFILE,self.section)
			cfgOBJ.setcfg("actual_song_name",self.playlist[self.song])
			#cfgOBJ.setcfg("actual_song_position",pygame.mixer.music.get_pos ())
			cfgOBJ.write()

	def explore(self):
		"""Explora el .path en busca de .musictypes e inicializa la .playlist"""
		self.playlist = []

		for root,dirs,files in os.walk(self.path):
			for file in [f for f in files if f.lower().endswith(self.musictypes)]:
				self.playlist.append(os.path.join(root, file))
				
		if self.suffle: random.shuffle(self.playlist)
	
	def play(self):
		"""Reproduce la canci�n del .playlist que indica .song
		devuelve True o False para indicar si se ha reproducido o no"""
		
		sngPLAY = False

		if (self.song != "no_event"):
			# Si se est� reproduciendo otra canci�n, primero la paro
			self.stop()
			# Cargo y reproduzco la canci�n correspondiente
			if len(self.playlist) > 0:
				try:
					pygame.mixer.music.load(self.playlist[self.song]) 
					pygame.mixer.music.play()
					#if (self.actsngPOS > 0):	pygame.mixer.music.play(1,self.actsngPOS/1000)
					#else:					pygame.mixer.music.play()
					
					self.actsngPOS = 0
					sngPLAY = True
				except:
					plfiles._LOG("WAR. unable to play song "+self.playlist[self.song])
			else:
				plfiles._LOG("WAR. no songs in playlist")
			
		return sngPLAY

	def pause(self):
		"""Pausa o reanuda la melod�a"""
		if self.paused: pygame.mixer.music.unpause()
		else:	pygame.mixer.music.pause()
		self.paused = not self.paused
		
	def stop(self):
		"""Para la reproducci�n (si se est� reproduciendo algo)"""
		self.paused = False
		if pygame.mixer.music.get_busy():	pygame.mixer.music.stop()

	def next(self):
		"""Avanza una canci�n en el .playlist"""
		loopBREAK = 0
		# Avanza y reproduce la siguiente
		if (len(self.playlist) > 1):
			if ((self.song+1) < len(self.playlist)): self.song += 1
			else:	self.song = 0
				
			while not self.play():
				self.next()
				loopBREAK += 1
				# Con esto prevengo bucles infinitos
				if (loopBREAK > 5): break
					
			pygame.time.delay(125)
			
	def prev(self):
		"""Retrocede una canci�n en el .playlist"""
		loopBREAK = 0
		# Retrocede y reproduce la anterior
		if (len(self.playlist) > 1):
			if (self.song == 0): self.song = len(self.playlist)-1
			else:	self.song -= 1

			while not self.play():
				self.prev()
				loopBREAK += 1
				# Con esto prevengo bucles infinitos
				if (loopBREAK > 5): break
			
			pygame.time.delay(125)
		
	def loop(self):	
		"""Si corresponde(cuando se acaba la canci�n actual), avanza una canci�n en el .playlist"""
		pygame.mixer.music.unpause()

		if (not pygame.mixer.music.get_busy()) and (len(self.playlist) > 0): jump_next = True
		else: jump_next = False
		return jump_next
			
	def end(self):
		"""Finaliza el jukeBOX"""
		self.write()
		self.stop()
		pygame.mixer.quit()
		
		
class sampler:
	"""Objeto encargado de gestionar loe efectos de sonido
	Devuelve: un objeto sampler
	Funciones: add y play
	Atributos: sound_dic, volume"""

	def __init__(self, volume=0.5, mixer_init=False):
		"""incializaci�n de del objeto"""
		self.sound_dic	= {}				# Diccionario de sonidos
		self.volume = volume				# Volumen de reproducc�on de los efectos

		# El sampler no suele ser el encargado de inicializar el mezclador
		if mixer_init:
			pygame.mixer.pre_init(samplerate,-16,2,1024*2)
			pygame.mixer.init()
	
	def add(self, soundID, soundPATH=""):
		"""A�ade un efecto de sonido al diccionario, o reemplaza uno existente"""
		
		if os.path.exists(soundPATH) and os.path.isfile(soundPATH):
			try: sample = pygame.mixer.Sound(soundPATH)
			except: 
				sample = None
				plfiles._LOG("ERR.(add) error loading "+soundPATH)
		else:
			sample = None
			plfiles._LOG("ERR.(add) file not found "+soundPATH)

		if (sample != None):
			sample.set_volume(self.volume)
			self.sound_dic[soundID] = sample

	def delete(self, soundID):
		"""Borra un efecto de sonido de la lista"""
		try:	del self.sound_dic[soundID]
		except: plfiles._LOG("ERR.(delete) sample not found "+soundID)

	def play(self,soundID):
		try: sample = self.sound_dic[soundID]
		except: 
			if (soundID != "no_event"):	plfiles._LOG("ERR.(play) sample not found "+soundID)
			sample = None
			
		if (sample != None): sample.play()
