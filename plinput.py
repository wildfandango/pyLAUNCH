# -*- coding: iso-8859-15 -*-

import pygame,plconfig,plfiles
from pygame.locals import *

# Interpreta las pulsaciones de teclado

class keySCAN:
	"""Objeto encargado de gestionar las pulsaciones de teclado"""

	def __init__(self, keyPATH, keySECTION = "keyboard"):
		"""incialización de del objeto"""
		self.path = keyPATH			# Ruta del fichero de configuración
		self.section = keySECTION		# Sección que contiene las configuraciones
		self.lastEVENT = "no_event"		# Último evento producido
		self.loop_key = False			# Indica si la tecla pulsada esta siendo pulsada dentro de un bucle
		self.loop_buffer = 0			# Tecla pulsada en bucle?

		# Acciones de teclado disponibles (y sus valores por defecto)
		self.next_item = K_RIGHT		# Siguiente elemento
		self.prev_item = K_LEFT		# Anterior elemento
		self.item_info = K_SPACE		# Información del elemento
		self.start_item = K_RETURN		# Ejecutar elemento
		
		self.next_list = K_DOWN		# Ir a la siguiente lista
		self.prev_list = K_UP			# Ir a la anterior lista
		
		self.next_song = K_RCTRL		# Siguiente canción
		self.prev_song = K_LCTRL		# Anterior canción

		self.launch_fav = K_f			# Favoritos
		self.launch_search = K_s		# Buscar

		self.exit_menu = K_ESCAPE		# Abandonar el menu

		self.read()					# Leo la configuración
		
	def keyPRESSED(self):
		"""Devuelve True o False en función de si hay alguna tecla pulsada o no"""

		pygame.event.pump()
		if 1 in pygame.key.get_pressed(): K_pressed = True
		else: K_pressed = False

		return K_pressed
	
	# Devuelve el nombre de la tecla KEY
	# Si se le indica una lista de estado de teclas devuelve el nombre de la "primera" pulsada
	def keyNAME(self,key,key_status=(0,0)):
		
		if (len(key_status) < 3):
			if key == self.next_item:	eventNAME = "next_item"
			elif key == self.prev_item:	eventNAME = "prev_item"
			elif key == self.item_info:	eventNAME = "item_info"
			elif key == self.start_item:	eventNAME = "start_item"
			elif key == self.next_list:	eventNAME = "next_list"
			elif key == self.prev_list:	eventNAME = "prev_list"
			elif key == self.next_song:	eventNAME = "next_song"
			elif key == self.prev_song:	eventNAME = "prev_song"
			elif key == self.exit_menu:	eventNAME = "exit_menu"
			elif key == self.launch_fav:	eventNAME = "launch_fav"
			elif key == self.launch_search: eventNAME = "launch_search"
			else: 				eventNAME = "no_event"
		else:
			if key_status[self.next_item]:		eventNAME = "next_item"
			elif key_status[self.prev_item]:	eventNAME = "prev_item"
			elif key_status[self.item_info]:	eventNAME = "item_info"
			elif key_status[self.start_item]:	eventNAME = "start_item"
			elif key_status[self.next_list]:	eventNAME = "next_list"
			elif key_status[self.prev_list]:	eventNAME = "prev_list"
			elif key_status[self.next_song]:	eventNAME = "next_song"
			elif key_status[self.prev_song]:	eventNAME = "prev_song"
			elif key_status[self.exit_menu]:	eventNAME = "exit_menu"
			elif key_status[self.launch_fav]:	eventNAME = "launch_fav"
			elif key_status[self.launch_search]: eventNAME = "launch_search"
			else: 					eventNAME = "no_event"
		
		# Si no hay evento compruebo que no se haya indicado un evento de salida
		if (eventNAME == "no_event") and pygame.event.peek(QUIT): eventNAME = "exit_menu"

		return eventNAME
		
	def pressed(self):
		"""Devuelve el nombre de la tecla pulsada o 'no_event' si no hay teclas pulsadas"""
		
		# 1 obengo la lista de teclas que estan siendo pulsadas
		pygame.event.pump()
		keyboard_status = pygame.key.get_pressed()
		
		# 2 Determino si hay alguna pulsación o evento de salida
		if pygame.event.peek(QUIT): nKEY = self.exit_menu
		elif keyboard_status[self.next_item] == 1: nKEY = self.next_item
		elif keyboard_status[self.prev_item] == 1: nKEY = self.prev_item
		elif keyboard_status[self.item_info] == 1: nKEY = self.item_info
		elif keyboard_status[self.start_item] == 1: nKEY = self.start_item
		elif keyboard_status[self.next_list] == 1: nKEY = self.next_list
		elif keyboard_status[self.prev_list] == 1: nKEY = self.prev_list
		elif keyboard_status[self.next_song] == 1: nKEY = self.next_song
		elif keyboard_status[self.prev_song] == 1: nKEY = self.prev_song
		elif keyboard_status[self.exit_menu] == 1: nKEY = self.exit_menu
		elif keyboard_status[self.launch_fav] == 1: nKEY = self.launch_fav
		elif keyboard_status[self.launch_search] == 1: nKEY = self.launch_search
		else: nKEY = 0
				
		# Doy nombre al evento, actualizo el minibuffer de ultima tecla pulsada y si se trata de pulsaciones consecutivas
		if (nKEY != self.loop_buffer): 
			self.loop_buffer = nKEY
			self.loop_key = False
			self.lastEVENT = self.keyNAME(nKEY,keyboard_status)
		else: self.loop_key = True
		
		return self.lastEVENT
		
	def event(self,keyUD=KEYDOWN):
		"""Devuelve el nombre del evento de teclado que se ha producido o 'no_event' si no se ha producido ninguno
		keyUD determina el evento en que hay que detectar la pulsación
		keyUD = KEYDOWN se lanzará la primera vez que se pulse una tecla
		keyUD = KEYUP se lanzará la primera vez que se libere una tecla pulsada"""
		eventNAME = "no_event"
		for event in pygame.event.get():
			if event.type in [QUIT]:			eventNAME = "exit_menu"
			elif (event.type == keyUD):			eventNAME = self.keyNAME(event.key)
		self.lastEVENT = eventNAME
		
		return eventNAME

	def read(self):
		"""Lee la configuración de teclas"""
		cfgOBJ = plconfig.iniCFG(self.path,self.section)
		self.next_item = eval(cfgOBJ.getcfg("next_item","K_RIGHT"))
		self.prev_item = eval(cfgOBJ.getcfg("prev_item","K_LEFT"))
		self.item_info = eval(cfgOBJ.getcfg("item_info","K_SPACE"))
		self.start_item = eval(cfgOBJ.getcfg("start_item","K_RETURN"))
		self.next_list = eval(cfgOBJ.getcfg("next_list","K_DOWN"))
		self.prev_list = eval(cfgOBJ.getcfg("prev_list","K_UP"))
		self.next_song = eval(cfgOBJ.getcfg("next_song","K_LCTRL"))
		self.prev_song = eval(cfgOBJ.getcfg("prev_song","K_RCTRL"))
		self.exit_menu = eval(cfgOBJ.getcfg("exit_menu","K_ESCAPE"))
		self.launch_fav = eval(cfgOBJ.getcfg("launch_fav","K_f"))
		self.launch_search = eval(cfgOBJ.getcfg("launch_search","K_s"))

	def write(self):
		"""Guarda la configuración de teclas"""
		cfgOBJ = plconfig.iniCFG(self.path,self.section)
		cfgOBJ.setcfg("next_item",self.next_item)
		cfgOBJ.setcfg("prev_item",self.prev_item)
		cfgOBJ.setcfg("item_info",self.item_info)
		cfgOBJ.setcfg("start_item",self.start_item)
		cfgOBJ.setcfg("next_list",self.next_list)
		cfgOBJ.setcfg("prev_list",self.prev_list)
		cfgOBJ.setcfg("exit_menu",self.exit_menu)
		cfgOBJ.setcfg("next_song",self.next_song)
		cfgOBJ.setcfg("prev_song",self.prev_song)
		cfgOBJ.setcfg("launch_fav",self.launch_fav)
		cfgOBJ.setcfg("launch_search",self.launch_search)
		cfgOBJ.write()
	
	
	
	
class joySCAN:
	"""Objeto encargado de gestionar las pulsaciones del joystick"""

	def __init__(self, joyPATH, joySECTION = "joystick"):
		"""incialización de del objeto"""
		pygame.joystick.init()

		try:
			if pygame.joystick.get_count() < 1:	
				self.joyPRESENT = False
				plfiles._LOG("WAR. 0 Joysticks found")
			else:							
				self.joyPRESENT = True
		except:
			plfiles._LOG("WAR. JoyStick system initializated?")
			self.joyPRESENT = False
		
		if self.joyPRESENT:
			self.JOY = pygame.joystick.Joystick(0)
			self.JOY.init()
			
		if self.joyPRESENT:
			plfiles._LOG("OK. JoyStick found!")
			try:
				self.JOY = pygame.joystick.Joystick(1)
				self.joyPRESENT = True
			except:
				plfiles._LOG("ERR. JoyStick 0 not initialized!")
				
		else:
			plfiles._LOG("WAR. JoyStick not found")
			
		self.path = joyPATH			# Ruta del fichero de configuración
		self.section = joySECTION		# Sección que contiene las configuraciones
		self.lastEVENT = "no_event"		# Último evento producido
		self.loop_joy = False			# Indica si la tecla pulsada esta siendo pulsada dentro de un bucle
		self.loop_buffer = ""			# Tecla pulsada en bucle?

		# Acciones de teclado disponibles (y sus valores por defecto)
		self.next_item = "J_A1+"		# Siguiente elemento
		self.prev_item = "J_A1-"		# Anterior elemento
		self.item_info = "J_B1"			# Información del elemento
		self.start_item = "J_B2"		# Ejecutar elemento
		
		self.next_list = "J_A2+"		# Ir a la siguiente lista
		self.prev_list = "J_A2-"		# Ir a la anterior lista
		
		self.next_song = "J_A3+"		# Siguiente canción
		self.prev_song = "J_A3-"		# Anterior canción

		self.launch_fav = "J_B3"		# Favoritos
		self.launch_search = "JB_4"		# Buscar

		self.exit_menu = "J_B5"		# Abandonar el menu

		self.read()					# Leo la configuración
		
	def joyPRESSED(self):
		"""Devuelve True o False en función de si hay alguna función del joystick activa o no"""
		
		J_pressed = False
		
		if self.joyPRESENT:
			if self.joySTATUS(self.next_item) == 1: J_pressed = True
			elif self.joySTATUS(self.prev_item) == 1: J_pressed = True
			elif self.joySTATUS(self.item_info)== 1: J_pressed = True
			elif self.joySTATUS(self.start_item) == 1: J_pressed = True
			elif self.joySTATUS(self.next_list) == 1: J_pressed = True
			elif self.joySTATUS(self.prev_list) == 1: J_pressed = True
			elif self.joySTATUS(self.next_song) == 1: J_pressed = True
			elif self.joySTATUS(self.prev_song) == 1: J_pressed = True
			elif self.joySTATUS(self.exit_menu) == 1: J_pressed = True
			elif self.joySTATUS(self.launch_fav) == 1: J_pressed = True
			elif self.joySTATUS(self.launch_search) == 1: J_pressed = True

		return J_pressed
	
	# Devuelve el nombre de la tecla JOY
	# Si no se le idica ningna tecla devuelve el nombre de la primera pulsada
	def joyNAME(self,joy=""):
		if (len(joy) > 0):
			if joy == self.next_item:			eventNAME = "next_item"
			elif joy == self.prev_item:			eventNAME = "prev_item"
			elif joy == self.item_info:			eventNAME = "item_info"
			elif joy == self.start_item:			eventNAME = "start_item"
			elif joy == self.next_list:			eventNAME = "next_list"
			elif joy == self.prev_list:			eventNAME = "prev_list"
			elif joy == self.next_song:			eventNAME = "next_song"
			elif joy == self.prev_song:			eventNAME = "prev_song"
			elif joy == self.exit_menu:			eventNAME = "exit_menu"
			elif joy == self.launch_fav:			eventNAME = "launch_fav"
			elif joy == self.launch_search: 		eventNAME = "launch_search"
			else: 						eventNAME = "no_event"
		else:
			if self.joySTATUS(self.next_item)==1:		eventNAME = "next_item"
			elif self.joySTATUS(self.prev_item)==1:		eventNAME = "prev_item"
			elif self.joySTATUS(self.item_info)==1:		eventNAME = "item_info"
			elif self.joySTATUS(self.start_item)==1:		eventNAME = "start_item"
			elif self.joySTATUS(self.next_list)==1:		eventNAME = "next_list"
			elif self.joySTATUS(self.prev_list)==1:		eventNAME = "prev_list"
			elif self.joySTATUS(self.next_song)==1:		eventNAME = "next_song"
			elif self.joySTATUS(self.prev_song)==1:		eventNAME = "prev_song"
			elif self.joySTATUS(self.exit_menu)==1:		eventNAME = "exit_menu"
			elif self.joySTATUS(self.launch_fav)==1:	eventNAME = "launch_fav"
			elif self.joySTATUS(self.launch_search)==1: 	eventNAME = "launch_search"
			else: 							eventNAME = "no_event"
		
		# Si no hay evento compruebo que no se haya indicado un evento de salida
		if (eventNAME == "no_event") and pygame.event.peek(QUIT): eventNAME = "exit_menu"

		return eventNAME
		
	def joySTATUS(self,jevent="???"):
		"""Devuelve el estado de un control concreto del JOYSTICK 1 activado 0 desactivado
		interpretación 
		J_ -> joystick
		A Axis o Analog (el más o el menos indica que dirección se usa) ej: J_A1+ (Axis 1 en positivo)
		B Buttom nº de botón (pulsado o no pulsado no hay más) ej: J_B2 (Botón 2 pulsado)
		C Cruceta nº de cruceta (1, 2, 4, 8 o combinaciones) ej: J_C14 (cruceta 1 botón 4 pulsado)
		"""
		try:
			jcontrol = int(jevent[3:4])	# Número de control (usado en AXIS o en cruceta)
		except:
			plfiles._LOG("ERR. NO jevent! ")
			jcontrol=-1
		jval = -1				# Valor devuelto por el control
		jstatus = 0				# Estado de ese evento concreto
		if not self.joyPRESENT: jcontrol=-1

		try:
			if (jcontrol > -1):
				if (jevent[:3] == "J_A"):
					# Estamos detectando un AXIS o ANALOG (número de AXIS y positivo o negativo)
					jcontrol = int(jevent[3:4])
					jval = self.JOY.get_axis(jcontrol)
					if (jevent[4:5] == "+") and (jval >=0.5): jstatus = 1
					elif (jevent[4:5] == "-")and (jval <=-0.5): jstatus = 1
					
				elif (jevent[:3] == "J_B"):
					# Estamos detectando un botón (pulsado o no)
					jval = self.JOY.get_button(jcontrol)
					if (jval == 1): jstatus = 1
					
				elif (jevent[:3] == "J_C"):
					# Estamos detectando una CRUCETA (número de cruceta y valor)
					jval = self.JOY.get_hat(jcontrol)
					if (jval == int(jevent[4:])): jstatus = 1
		except:
			jstatus = 0				# Estado de ese evento concreto
			plfiles._LOG("ERR. JoyStick status fail")
			self.joyPRESENT = False
		
		return jstatus
		
	def pressed(self):
		"""Devuelve el nombre de la tecla pulsada o 'no_event' si no hay teclas pulsadas"""
		
		nJOY = "no_event"
		
		# 1 Determino si hay alguna pulsación o evento de salida
		if self.joyPRESENT:
			if pygame.event.peek(QUIT): nJOY = self.exit_menu
			elif self.joySTATUS(self.next_item) == 1: nJOY = self.next_item
			elif self.joySTATUS(self.prev_item) == 1: nJOY = self.prev_item
			elif self.joySTATUS(self.item_info) == 1: nJOY = self.item_info
			elif self.joySTATUS(self.start_item) == 1: nJOY = self.start_item
			elif self.joySTATUS(self.next_list) == 1: nJOY = self.next_list
			elif self.joySTATUS(self.prev_list) == 1: nJOY = self.prev_list
			elif self.joySTATUS(self.next_song) == 1: nJOY = self.next_song
			elif self.joySTATUS(self.prev_song) == 1: nJOY = self.prev_song
			elif self.joySTATUS(self.exit_menu) == 1: nJOY = self.exit_menu
			elif self.joySTATUS(self.launch_fav) == 1: nJOY = self.launch_fav
			elif self.joySTATUS(self.launch_search) == 1: nJOY = self.launch_search
				
		# Doy nombre al evento, actualizo el minibuffer de ultima tecla pulsada y si se trata de pulsaciones consecutivas
		if (nJOY != self.loop_buffer): 
			self.loop_buffer = nJOY
			self.loop_joy = False
			self.lastEVENT = self.joyNAME(nJOY)
		else: self.loop_joy = True
		
		return self.lastEVENT
		
	def event(self,keyUD=KEYDOWN):
		"""Devuelve el nombre del evento de teclado que se ha producido o 'no_event' si no se ha producido ninguno
		keyUD determina el evento en que hay que detectar la pulsación
		keyUD = KEYDOWN se lanzará la primera vez que se pulse una tecla
		keyUD = KEYUP se lanzará la primera vez que se libere una tecla pulsada"""
		eventNAME = "no_event"
		for event in pygame.event.get():
			if event.type in [QUIT]:			eventNAME = "exit_menu"
			elif (event.type == keyUD):			eventNAME = self.keyNAME(event.key)
		self.lastEVENT = eventNAME
		
		return eventNAME

	def read(self):
		"""Lee la configuración de joystick
		interpretación 
		J_ -> joystick
		A Axis o Analog (el más o el menos indica que dirección se usa) ej: J_A1+ (Axis 1 en positivo)
		B Buttom nº de botón (pulsado o no pulsado no hay más) ej: J_B2 (Botón 2 pulsado)
		C Cruceta nº de cruceta (1, 2, 4, 8 o combinaciones) ej: J_C14 (cruceta 1 botón 4 pulsado)
		"""
		cfgOBJ = plconfig.iniCFG(self.path,self.section)
		self.next_item = cfgOBJ.getcfg("jnext_item","J_A1+")
		self.prev_item = cfgOBJ.getcfg("jprev_item","J_A1-")
		self.item_info = cfgOBJ.getcfg("jitem_info","J_B1")
		self.start_item = cfgOBJ.getcfg("jstart_item","J_B2")
		self.next_list = cfgOBJ.getcfg("jnext_list","J_A2+")
		self.prev_list = cfgOBJ.getcfg("jprev_list","J_A2-")
		self.next_song = cfgOBJ.getcfg("jnext_song","J_A3+")
		self.prev_song = cfgOBJ.getcfg("jprev_song","J_A3-")
		self.exit_menu = cfgOBJ.getcfg("jexit_menu","J_B3")
		self.launch_fav = cfgOBJ.getcfg("jlaunch_fav","J_B4")
		self.launch_search = cfgOBJ.getcfg("jlaunch_search","J_B5")

	def write(self):
		"""Guarda la configuración de teclas"""
		cfgOBJ.write()
	