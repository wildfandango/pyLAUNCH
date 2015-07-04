# -*- coding: iso-8859-15 -*-

import pygame,plconfig,plaudio,plvideo,plinput,plconfig,plexecuter,plfiles,os,inspect
from pygame.locals import *

# Coordina los módulos plinput,plaudio,plvideo y plconfig para hacer funcionar el menu correctamente

class MENU:
	"""Coordinador de todos los demás módulos"""

	def __init__(self): 
		"""incialización del objeto, carga de configuraciones"""
		self.main_config_file = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + "\\pyLAUNCH.CFG"
		self.state_config_file = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + "\\cfg\\state.cfg"
		self.changes = False											# Indica si se han producido cambios en la pantalla
		self.eventpress = ""											# Última tecla pulsada (de teclado o joystick)
		self.last_action = 0											# Tiempo transcurrido desde la ultima acción
		self.frames = 0												# Cuenta el número total de fotogramas
		self.loops = 0												# Cuenta el número total de ciclos
		self.search = ""												# Busqueda que se está ejecutando
		self.last_search = self.search										# Almacena la última búsqueda ejecutada
		self.frame_search = 0											# Detector de la actividad de búsqueda
		self.finding = False											# Indica si buscamos True o navegamos por el resultado de la búsqueda False
		self.item_info = False											# Indica si se muestra o no info de un item
		self.dict = "_abcdefghijklmnopqrstuvwxyz0123456789"					# Diccionario de caracteres usado en las busquedas
		
		self.configFILE = plconfig.iniCFG(self.main_config_file)					# Fichero general de configuración
		self.CFG = {}												# Diccionario de configuraciones
		
		self.configFILE.section = "MENU"
		self.CFG["debug_mode"] = self.configFILE.getcfg("debug_mode",False)			# Modo de depuración
		# Aqui se stablece el modo dbug ya configurado
		self.CFG["menu_wallpaper"] = self.configFILE.getcfg("menu_wallpaper","")	# Fondo de pantalla general
		self.CFG["menu_list"] = self.configFILE.getcfg("menu_list",("",""))			# Listas de ITEMS
		self.CFG["menu_screensaver"] = self.configFILE.getcfg("menu_screensaver",1)	# Tiempo para el salto del salvapantallas
		self.CFG["menu_style"] = self.configFILE.getcfg("menu_style",0)			# Estilo del menú
		self.CFG["menu_speed"] = self.configFILE.getcfg("menu_speed",0.19)			# Velocidad de las animaciones
		self.CFG["menu_kloop"] = self.configFILE.getcfg("menu_kloop",8)			# Repeticiones de teclado antes de entrar en modo continuo
		self.CFG["menu_stats"] = self.configFILE.getcfg("menu_stats","")			# Información de estado
		
		self.configFILE.section = "VIDEO"
		self.CFG["screen_resolution"] = self.configFILE.getcfg("screen_resolution",(0,0))	# Resolución de pantalla (0,0) utilizar la actual
		self.CFG["screen_fullscreen"] = self.configFILE.getcfg("screen_fullscreen",False)	# Pantalla completa?
		self.CFG["screen_hardware"] = self.configFILE.getcfg("screen_hardware",False)		# Aceleración por hardware?
		self.CFG["screen_dblbuffer"] = self.configFILE.getcfg("screen_dblbuffer",False)	# Doble buffer de video?
		self.CFG["video_fps"] = self.configFILE.getcfg("video_fps",25)				# Frames por segundo de video?
		
		self.CFG["text_alpha"] = self.configFILE.getcfg("text_alpha",100)				# Transparencia del texto seleccionado
		
		self.CFG["font1_name"] = self.configFILE.getcfg("font1_name","Verdana")				# Nombre de la fuente
		self.CFG["font1_size"] = self.configFILE.getcfg("font1_size",32)					# Tamaño de la fuente
		self.CFG["font1_bold"] = self.configFILE.getcfg("font1_bold",False)					# Negrita?
		self.CFG["font1_color"] = self.configFILE.getcfg("font1_color",(255,255,255))			# Color de la fuente
		self.CFG["font1_shadow_disp"] = self.configFILE.getcfg("font1_shadow_disp",(2,2))		# Desplazamiento de la sombra
		self.CFG["font1_shadow_type"] = self.configFILE.getcfg("font1_shadow_type",0)		# Tipo de sombra
		self.CFG["font1_shadow_color"] = self.configFILE.getcfg("font1_shadow_color",(0,0,0))	# Color de la sombra
		self.CFG["font1_alpha"] = self.configFILE.getcfg("font1_alpha",255)				# Nivel transparencia principal
		self.CFG["font1_shadow_alpha"] = self.configFILE.getcfg("font1_shadow_alpha",125)		# Nivel transparencia de la sombra
		self.CFG["font1_hor_sep"] = self.configFILE.getcfg("font1_hor_sep",0)				# Modificador de la separación hotizontal de las letras
		self.CFG["font1_ver_sep"] = self.configFILE.getcfg("font1_ver_sep",0)				# Modificador de la separación vertical de las letras
		self.CFG["font1_align"] = self.configFILE.getcfg("font1_align",0)					# Alineación del texto
		
		self.CFG["font2_name"] = self.configFILE.getcfg("font2_name","Verdana")				# Nombre de la fuente
		self.CFG["font2_size"] = self.configFILE.getcfg("font2_size",16)					# Tamaño de la fuente
		self.CFG["font2_bold"] = self.configFILE.getcfg("font2_bold",False)					# Negrita?
		self.CFG["font2_color"] = self.configFILE.getcfg("font2_color",(255,255,255))			# Color de la fuente
		self.CFG["font2_shadow_disp"] = self.configFILE.getcfg("font2_shadow_disp",(2,2))		# Desplazamiento de la sombra
		self.CFG["font2_shadow_type"] = self.configFILE.getcfg("font2_shadow_type",0)		# Tipo de sombra
		self.CFG["font2_shadow_color"] = self.configFILE.getcfg("font2_shadow_color",(0,0,0))	# Color de la sombra
		self.CFG["font2_alpha"] = self.configFILE.getcfg("font2_alpha",255)				# Nivel transparencia principal
		self.CFG["font2_shadow_alpha"] = self.configFILE.getcfg("font2_shadow_alpha",125)		# Nivel transparencia de la sombra
		self.CFG["font2_hor_sep"] = self.configFILE.getcfg("font2_hor_sep",0)				# Modificador de la separación hotizontal de las letras
		self.CFG["font2_ver_sep"] = self.configFILE.getcfg("font2_ver_sep",0)				# Modificador de la separación vertical de las letras
		self.CFG["font2_align"] = self.configFILE.getcfg("font2_align",0)					# Alineación del texto

		self.CFG["font3_name"] = self.configFILE.getcfg("font3_name","Verdana")				# Nombre de la fuente
		self.CFG["font3_size"] = self.configFILE.getcfg("font3_size",8)					# Tamaño de la fuente
		self.CFG["font3_bold"] = self.configFILE.getcfg("font3_bold",False)					# Negrita?
		self.CFG["font3_color"] = self.configFILE.getcfg("font3_color",(255,255,255))			# Color de la fuente
		self.CFG["font3_shadow_disp"] = self.configFILE.getcfg("font3_shadow_disp",(1,1))		# Desplazamiento de la sombra
		self.CFG["font3_shadow_type"] = self.configFILE.getcfg("font3_shadow_type",0)		# Tipo de sombra
		self.CFG["font3_shadow_color"] = self.configFILE.getcfg("font3_shadow_color",(0,0,0))	# Color de la sombra
		self.CFG["font3_alpha"] = self.configFILE.getcfg("font3_alpha",255)				# Nivel transparencia principal
		self.CFG["font3_shadow_alpha"] = self.configFILE.getcfg("font3_shadow_alpha",125)		# Nivel transparencia de la sombra
		self.CFG["font3_hor_sep"] = self.configFILE.getcfg("font3_hor_sep",0)				# Modificador de la separación hotizontal de las letras
		self.CFG["font3_ver_sep"] = self.configFILE.getcfg("font3_ver_sep",0)				# Modificador de la separación vertical de las letras
		self.CFG["font3_align"] = self.configFILE.getcfg("font3_align",0)					# Alineación del texto
		
		self.CFG["snap_zoom"] = self.configFILE.getcfg("snap_zoom",1)						# Tipo de ZOOM
		self.CFG["snap_scale2x"] = self.configFILE.getcfg("snap_scale2x",True)				# SCALE2X?
		self.CFG["snap_shadow"] = self.configFILE.getcfg("snap_shadow",True)				# Sombra en snaps?
		self.CFG["snap_position"] = self.configFILE.getcfg("snap_position",(0,0))			# Posición de los pantallazos
		
		self.CFG["fav_list_name"] = self.configFILE.getcfg("fav_list_name","MOST PLAYED (*list*)")		# Titulo de la lista de favoritos
		self.CFG["fav_item_name"] = self.configFILE.getcfg("fav_item_name","*item* (*played*)")	# Nombres de los elementos
		self.CFG["fav_list_size"] = self.configFILE.getcfg("fav_list_size",20)				# Número de elementos máximos en la lista de favoritos
		

		self.configFILE.section = "AUDIO"
		self.CFG["music_dir"] = self.configFILE.getcfg("music_dir","")				# Directorio que contiene las músicas
		self.CFG["music_type"] = self.configFILE.getcfg("music_type",(".mid",".mod",".mp3",".s3m",".xm",".ogg"))				# Tipos de formato de música soportados
		self.CFG["music_suffle"] = self.configFILE.getcfg("music_suffle",True)			# Reproducción aleatoria
		self.CFG["music_samplerate"] = self.configFILE.getcfg("music_samplerate",44100)	# Frecuencia de mustreo
		self.CFG["music_volume"] = self.configFILE.getcfg("music_volume",0.5)			# Volumen de la música
		self.CFG["effects_volume"] = self.configFILE.getcfg("effects_volume",0.5)		# Volumen de los efectos
		self.CFG["video_options"] = 0										# Opciones de video "concentradas"
		if self.CFG["screen_fullscreen"]: self.CFG["video_options"] += FULLSCREEN 
		if self.CFG["screen_hardware"]: self.CFG["video_options"] += HWSURFACE 
		if self.CFG["screen_dblbuffer"]: self.CFG["video_options"] += DOUBLEBUF
		#self.CFG["video_options"] += (SRCALPHA+RESIZABLE)
			
		# Interceptador de teclado
		self.KEY = plinput.keySCAN(self.main_config_file,"INPUT")

		# Interceptador de joystick
		self.JOY = plinput.joySCAN(self.main_config_file,"INPUT")
		
		# Música de fondo (E INICIALIZACIÓN DEL AUDIO)
		self.MUSIC = plaudio.jukeBOX(self.CFG["music_dir"],self.state_config_file,self.CFG["music_suffle"],self.CFG["music_volume"],self.CFG["music_type"],self.CFG["music_samplerate"],"JUKEBOX")
		self.MUSIC.play()
		
		# Efectos de sonido (inicialización, su ubicación, nombre y número, son fijos)
		self.SAMPLER = plaudio.sampler(self.CFG["effects_volume"])
		self.SAMPLER.add("next_item","sound\\next_item.wav")
		self.SAMPLER.add("prev_item","sound\\prev_item.wav")
		self.SAMPLER.add("next_list","sound\\next_list.wav")
		self.SAMPLER.add("prev_list","sound\\prev_list.wav")
		self.SAMPLER.add("next_song","sound\\next_song.wav")
		self.SAMPLER.add("prev_song","sound\\prev_song.wav")
		self.SAMPLER.add("start_item","sound\\start_item.wav")
		self.SAMPLER.add("item_info","sound\\item_info.wav")
		self.SAMPLER.add("exit_menu","sound\\exit_menu.wav")
		self.SAMPLER.add("launch_fav","sound\\launch_fav.wav")
		self.SAMPLER.add("launch_search","sound\\launch_search.wav")
		
		# Textos (inicialización)
		self.vTXT = plvideo.bitmapTXT(self.CFG["font1_name"],self.CFG["font1_size"],self.CFG["font1_shadow_type"],self.CFG["font1_shadow_disp"],self.CFG["font1_shadow_color"],self.CFG["font1_bold"])
		self.vTXT.mainALPHA = self.CFG["font1_alpha"],self.CFG["font1_alpha"],self.CFG["font1_alpha"]
		self.vTXT.shadowALPHA = self.CFG["font1_shadow_alpha"],self.CFG["font1_shadow_alpha"],self.CFG["font1_shadow_alpha"]
		self.vTXT.interCHAR = self.CFG["font1_hor_sep"]
		self.vTXT.txtALIGN = self.CFG["font1_align"]
		
		self.vTXTm = plvideo.bitmapTXT(self.CFG["font2_name"],self.CFG["font2_size"],self.CFG["font2_shadow_type"],self.CFG["font2_shadow_disp"],self.CFG["font2_shadow_color"],self.CFG["font2_bold"])
		self.vTXTm.mainALPHA = self.CFG["font2_alpha"],self.CFG["font2_alpha"],self.CFG["font2_alpha"]
		self.vTXTm.shadowALPHA = self.CFG["font2_shadow_alpha"],self.CFG["font2_shadow_alpha"],self.CFG["font2_shadow_alpha"]
		self.vTXTm.interCHAR = self.CFG["font2_hor_sep"]
		self.vTXTm.txtALIGN = self.CFG["font2_align"]
		
		self.vTXTp = plvideo.bitmapTXT(self.CFG["font3_name"],self.CFG["font3_size"],self.CFG["font3_shadow_type"],self.CFG["font3_shadow_disp"],self.CFG["font3_shadow_color"],self.CFG["font3_bold"])
		self.vTXTp.mainALPHA = self.CFG["font3_alpha"],self.CFG["font3_alpha"],self.CFG["font3_alpha"]
		self.vTXTp.shadowALPHA = self.CFG["font3_shadow_alpha"],self.CFG["font3_shadow_alpha"],self.CFG["font3_shadow_alpha"]
		self.vTXTp.interCHAR = self.CFG["font3_hor_sep"]
		self.vTXTp.txtALIGN = self.CFG["font3_align"]
		
		
		plvideo.videoINIT(self)
		
		# Actualizador de los textos mostrados (a través de vTXT y vTXTp)
		self.vDISP = plvideo.vidRENDER(self)

		# Cargo la imágen de fondo
		self.wallpaper =  plvideo.sizeIMG(plvideo.loadIMG(self.CFG["menu_wallpaper"]),self.CFG["screen_resolution"])
		self.main_screen.blit(self.wallpaper, (0,0))

		# Texto de espera
		self.vTXT.msg(self.main_screen,"loading data...",(-1,self.vTXT.get_dim()[1]*2),self.CFG["font1_color"])
		pygame.display.flip()
		
		# Controlador de salida del menu
		self.exitMENU = False
		# Gestionador de listas
		self.LIST = plconfig.theLIST(self.CFG["menu_list"],self.state_config_file,self)
		# Ejecutor de aplicaciones
		self.EXE = plexecuter.launcher()
		self.scrSAVER = None
		
		# iniciamos en modo búsqueda
		if (self.LIST.actual_list_name == "__FOUND"):  self.finding = True

		# La primera carga se hace sin animaciones
		self.vDISP.anim_list = False
		self.vDISP.anim_image = False
		
		# Velocidad de retardo en bucles infinitos (tecla permanentemente pulsada)
		self.ret = self.CFG["video_fps"] / 5

	def loop(self):	
		self.changes = False
		self.loops += 1
		
		if (self.loops < 2):  last_eventpress = self.eventpress
		
		last_loop = self.KEY.loop_key or self.JOY.loop_joy
		
		if self.JOY.joyPRESSED():
			last_event = self.JOY.lastEVENT
			self.eventpress = self.JOY.pressed()
		else:
			last_event = self.KEY.lastEVENT
			self.eventpress = self.KEY.pressed()

		# Si se ha dejado de pulsar se cortan los bucles
		if (self.KEY.loop_buffer == 0):	self.KEY.loop_key = False
		if (self.JOY.loop_buffer == 0):	self.JOY.loop_joy = False
		
		act_loop = self.KEY.loop_key or self.JOY.loop_joy
		
		# Compruebo si acaba de terminar un bucle
		if last_loop and not act_loop:
			if (last_event in ["next_item","prev_item"]):
				if not self.finding and not self.vDISP.show_image:
					self.vDISP.anim_list = False
					self.vDISP.show_list = True
					self.vDISP.anim_image = False
					self.vDISP.show_image = True
					
					self.vDISP.show_title = True
					self.vDISP.show_stats = True
					self.vDISP.show_wall = True
					self.vDISP.anim_wall = False
					
					self.vDISP.refresh()
			
		# Contador de ciclos en el bucle
		if act_loop:		self.vDISP.inloop += 1
		else:				self.vDISP.inloop = 1
		
		# A los X minutos configurados en el salvapantallas (0 = sin savapantallas)
		if (self.CFG["menu_screensaver"] > 0) and (self.last_action > (self.CFG["video_fps"]*60*self.CFG["menu_screensaver"])): 
		#if (self.CFG["menu_screensaver"] > 0) and (self.last_action > (self.CFG["video_fps"]*60*0.1)): 
			if (self.scrSAVER == None): scrSAVER = plvideo.screenSAVER(self)
			scrSAVER.scrLOOP()
			self.MUSIC.next()
			
			if (not last_event in ["next_item","prev_item","next_list","prev_list"]):
				self.vDISP.show_list = True
				self.vDISP.anim_image = False
				self.vDISP.show_image = True
				self.vDISP.anim_list = False
				
				self.vDISP.show_title = True
				self.vDISP.show_stats = True
				self.vDISP.show_wall = True
				self.vDISP.anim_wall = False
			
				self.vDISP.refresh()

				
		# Emito el efecto de sonido asociado a la tecla pulsada
		if (not (self.eventpress in ["no_event","next_song","prev_song"])): 	self.last_action = 0
		else: self.last_action += 1


		if (self.eventpress == "exit_menu"):
			if self.item_info:
				self.item_info = False
				self.vDISP.show_list = True
				self.vDISP.anim_image = False
				self.vDISP.show_image = True
				self.vDISP.anim_list = False
				
				self.vDISP.show_title = True
				self.vDISP.show_stats = True
				self.vDISP.show_wall = True
				self.vDISP.anim_wall = False
			
				self.vDISP.refresh()
				
			# De esta forma evito la salida del front-end con pulsaciones accidentales de ESC
			if (self.vDISP.inloop > (self.CFG["video_fps"]*4)): 
				self.exitMENU = True
			else:
				if act_loop:		self.vDISP.inloop += 1
				else:			self.vDISP.inloop = 1
					
			
		elif self.MUSIC.loop() or (self.eventpress == "next_song"): 
			self.menu_clock.tick(self.ret)
			self.vDISP.anim_list = False
			self.vDISP.show_list = True
			self.vDISP.anim_image = False
			self.vDISP.show_image = True
			
			self.vDISP.show_title = True
			self.vDISP.show_stats = True
			self.vDISP.show_wall = True
			self.vDISP.anim_wall = False
			self.MUSIC.next()

			
			
		elif (self.eventpress == "prev_song"):
			self.menu_clock.tick(self.ret)
			self.vDISP.anim_list = False
			self.vDISP.show_list = True
			self.vDISP.anim_image = False
			self.vDISP.show_image = True
			
			self.vDISP.show_title = True
			self.vDISP.show_stats = True
			self.vDISP.show_wall = True
			self.vDISP.anim_wall = False
			self.MUSIC.prev()
			
			
		elif self.finding and (self.eventpress == "next_list"): 
			# Nueva Letra (hasta un máximo de 16)
			# Si no hay letras cojo la primera y si las hay copio la anterior
			self.menu_clock.tick(self.ret)
			if (len(self.search) == 0): self.search += self.dict[0]
			elif (len(self.search) < 16): self.search += self.search[-1]
				
			self.vDISP.anim_list = False
			self.vDISP.show_list = True
			self.vDISP.anim_image = False
			self.vDISP.show_image = False
			
			self.vDISP.show_title = True
			self.vDISP.show_stats = True
			self.vDISP.show_wall = True
			self.vDISP.anim_wall = False

			self.frame_search = self.frames

			
			
		elif self.finding and (self.eventpress == "prev_list"): 
			# Borrar una letra (salvo la primera)
			self.menu_clock.tick(self.ret)
			if (len(self.search) > 1): self.search = self.search[:len(self.search)-1]
			
			self.vDISP.anim_list = False
			self.vDISP.show_list = True
			self.vDISP.anim_image = False
			self.vDISP.show_image = False
			
			self.vDISP.show_title = True
			self.vDISP.show_stats = True
			self.vDISP.show_wall = True
			self.vDISP.anim_wall = False

			self.frame_search = self.frames
			
			
		elif self.finding and (self.eventpress == "next_item"): 
			# Letra arriba (o volver a empezar desde el principio)
			self.menu_clock.tick(self.ret)
			if len(self.search) == 0:
				self.search = self.dict[0]
			else:
				nfind = self.dict.find(self.search[-1]) 
				self.search = self.search[:-1]
				
				if nfind < (len(self.dict)-1):	self.search += self.dict[nfind+1]
				else:					self.search += self.dict[0]
			
			self.frame_search = self.frames

			self.vDISP.show_list = True
			self.vDISP.anim_image = False
			self.vDISP.show_image = False
			self.vDISP.anim_list = False
			
			self.vDISP.show_title = True
			self.vDISP.show_stats = True
			self.vDISP.show_wall = True
			self.vDISP.anim_wall = False
			
				
		elif self.finding and (self.eventpress == "prev_item"): 
			# Letra abajo (o volver a empezar desde el final)
			self.menu_clock.tick(self.ret)
			if len(self.search) == 0:
				self.search = self.dict[-1]
			else:
				nfind = self.dict.find(self.search[-1]) 
				self.search = self.search[:-1]
				
				if nfind == 0:	self.search += self.dict[-1]
				else:			self.search += self.dict[nfind-1]
			
			self.frame_search = self.frames			
			
			self.vDISP.show_list = True
			self.vDISP.anim_image = False
			self.vDISP.show_image = False
			self.vDISP.anim_list = False
			
			self.vDISP.show_title = True
			self.vDISP.show_stats = True
			self.vDISP.show_wall = True
			self.vDISP.anim_wall = False
			
		
		elif (self.eventpress == "next_list"): 
			if act_loop: 
				self.vDISP.anim_list = False
				self.vDISP.show_list = True
				self.vDISP.anim_image = False
				self.vDISP.show_image = True
				
				self.vDISP.show_title = True
				self.vDISP.show_stats = True
				self.vDISP.show_wall = True
				self.vDISP.anim_wall = False
				self.menu_clock.tick(self.ret/1.5)
			else:
				self.vDISP.show_list = True
				self.vDISP.anim_image = False
				self.vDISP.show_image = True
				self.vDISP.anim_list = False
				
				self.vDISP.show_title = True
				self.vDISP.show_stats = True
				self.vDISP.show_wall = True
				self.vDISP.anim_wall = True

			if (self.vDISP.inloop > 1) and (self.LIST.actual_list_index >= (len(self.LIST.lstCACHE)-4)):
				if (self.frames % (self.ret*4)) == 0: self.SAMPLER.play(self.eventpress)
			else:
				self.LIST.nextlist()
				

		elif (self.eventpress == "prev_list"): 
			if act_loop: 
				self.vDISP.anim_list = False
				self.vDISP.show_list = True
				self.vDISP.anim_image = False
				self.vDISP.show_image = True
				
				self.vDISP.show_title = True
				self.vDISP.show_stats = True
				self.vDISP.show_wall = True
				self.vDISP.anim_wall = False
				self.menu_clock.tick(self.ret/1.5)
			else:
				self.vDISP.show_list = True
				self.vDISP.anim_image = False
				self.vDISP.show_image = True
				self.vDISP.anim_list = False
				
				self.vDISP.show_title = True
				self.vDISP.show_stats = True
				self.vDISP.show_wall = True
				self.vDISP.anim_wall = True

			if (self.vDISP.inloop > 1) and (self.LIST.actual_list_index == 0):
				if (self.frames % (self.ret*4)) == 0: self.SAMPLER.play(self.eventpress)
			else:
				self.LIST.prevlist()
				
			
		elif (self.eventpress == "next_item"): 
			if act_loop: 
				self.vDISP.anim_list = False
				self.vDISP.show_list = True
				self.vDISP.anim_image = False
				self.vDISP.show_image = False
				
				self.vDISP.show_title = True
				self.vDISP.show_stats = True
				self.vDISP.show_wall = True
				self.vDISP.anim_wall = True
			else:
				self.vDISP.show_list = True
				self.vDISP.anim_image = True
				self.vDISP.show_image = True
				self.vDISP.anim_list = True
				
				self.vDISP.show_title = True
				self.vDISP.show_stats = True
				self.vDISP.show_wall = True
				self.vDISP.anim_wall = True

			try:
				if (self.vDISP.inloop > 1) and (self.LIST.LST[self.LIST.actual_list_name]["_ACTUAL_ITEM_INDEX"] >= (len(self.LIST.LST[self.LIST.actual_list_name]["_CACHE_"])-1)):
					if (self.frames % (self.ret*3)) == 0: self.SAMPLER.play(self.eventpress)
				else:
					self.LIST.nextitem()
			except:
				self.LIST.nextitem()
				plfiles._LOG("ERR. NEXT ITEM IN LIST "+self.LIST.actual_list_name)

				
			
		elif (self.eventpress == "prev_item"): 
			if act_loop: 
				self.vDISP.anim_list = False
				self.vDISP.show_list = True
				self.vDISP.anim_image = False
				self.vDISP.show_image = False
				
				self.vDISP.show_title = True
				self.vDISP.show_stats = True
				self.vDISP.show_wall = True
				self.vDISP.anim_wall = True
			else:
				self.vDISP.show_list = True
				self.vDISP.anim_image = True
				self.vDISP.show_image = True
				self.vDISP.anim_list = True
				
				self.vDISP.show_title = True
				self.vDISP.show_stats = True
				self.vDISP.show_wall = True
				self.vDISP.anim_wall = True

			try:
				if (self.vDISP.inloop > 1) and (self.LIST.LST[self.LIST.actual_list_name]["_ACTUAL_ITEM_INDEX"] == 0):
					if (self.frames % (self.ret*3)) == 0: self.SAMPLER.play(self.eventpress)
				else:
					self.LIST.previtem()
			except:
				self.LIST.previtem()
				plfiles._LOG("ERR. PREV ITEM IN LIST "+self.LIST.actual_list_name)
				
				
		elif (self.eventpress == "item_info"):
			self.item_info = not self.item_info

			if self.item_info:
				self.SAMPLER.play(self.eventpress)
				item_img = self.LIST.getitem(0,2)
				splashRES = self.CFG["screen_resolution"]
				
				cfgFAV = plconfig.iniCFG(self.state_config_file,"__MOST")
				playCOUNT = cfgFAV.getcfg(self.LIST.getListID()+"_"+self.LIST.getItemID(),0)
				
				# Carga de la imágen y Escala 2x (solo si está configurada)
				splIMG = plvideo.loadIMG(item_img).convert()
				if self.CFG["snap_scale2x"]:  splIMG = pygame.transform.scale2x(splIMG)
				self.main_screen.blit(plvideo.sizeIMG(splIMG,splashRES), (0,0))

				# Calculo las posiciones de los textos y el tamaño del recuadro traslúcido del fondo
				txt1Y = int(splashRES[1]/2)-(self.vTXT.get_dim()[1]/2)
				txt2Y = int(splashRES[1]/2)+(self.vTXT.get_dim()[1]/2)
				
				x1 = 0
				y1 = txt1Y-self.vTXT.get_dim()[1]
				x2 = splashRES[0]
				y2 = self.vTXT.get_dim()[1]*3

				# Dibujo un recuadro traslúcido 
				tmpSURFACE = pygame.Surface((x2-x1, y2), pygame.SRCALPHA)
				tmpSURFACE.fill(pygame.Color(0,0,0,150))
				self.main_screen.blit(tmpSURFACE,(x1,y1))
				
				# Textos de carga
				self.vTXT.msg(self.main_screen,self.LIST.getitem(0,1),(-1,txt1Y),self.CFG["font1_color"])
				self.vTXT.msg(self.main_screen,self.LIST.getListID()+"."+self.LIST.getItemID()+" (played "+str(playCOUNT)+" times)",(-1,txt2Y),self.CFG["font1_color"])
				pygame.display.flip()
			else:
				self.vDISP.show_list = True
				self.vDISP.anim_image = False
				self.vDISP.show_image = True
				self.vDISP.anim_list = False
				
				self.vDISP.show_title = True
				self.vDISP.show_stats = True
				self.vDISP.show_wall = True
				self.vDISP.anim_wall = False
			
				self.vDISP.refresh()

			self.menu_clock.tick(self.ret)



		elif (self.eventpress == "start_item") : 
			self.SAMPLER.play(self.eventpress)
			self.EXE.launch(self)

			self.vDISP.show_list = True
			self.vDISP.anim_image = False
			self.vDISP.show_image = True
			self.vDISP.anim_list = False
			
			self.vDISP.show_title = True
			self.vDISP.show_stats = True
			self.vDISP.show_wall = True
			self.vDISP.anim_wall = False
			
			
		elif (self.eventpress == "launch_fav"): 
			self.LIST.actual_list_name = "__MOST"
			self.vDISP.show_list = True
			self.vDISP.anim_image = False
			self.vDISP.show_image = True
			self.vDISP.anim_list = False
			
			self.vDISP.show_title = True
			self.vDISP.show_stats = True
			self.vDISP.show_wall = True
			self.vDISP.anim_wall = True
			self.finding = False
			
			
		elif (self.eventpress == "launch_search"): 
			if (self.LIST.actual_list_name == "__FOUND"):
				self.finding = not self.finding
			else:
				self.LIST.actual_list_name = "__FOUND"
				self.finding = True
							
			if self.finding:
				self.vDISP.show_list = True
				self.vDISP.anim_image = False
				self.vDISP.show_image = False
				self.vDISP.anim_list = False
				
				self.vDISP.show_title = True
				self.vDISP.show_stats = True
				self.vDISP.show_wall = True
				self.vDISP.anim_wall = False
			else:
				self.vDISP.show_list = True
				self.vDISP.anim_image = False
				self.vDISP.show_image = True
				self.vDISP.anim_list = False
				
				self.vDISP.show_title = True
				self.vDISP.show_stats = True
				self.vDISP.show_wall = True
				self.vDISP.anim_wall = False
				
			self.menu_clock.tick(self.ret)
			self.vDISP.refresh()				
			
		self.frames += 1
		self.changes = self.vDISP.scan_changes()
		
		if self.changes:
			if self.finding:  self.LIST.find(self.search)
			self.vDISP.refresh()

		self.menu_clock.tick(self.CFG["video_fps"])

		# Tras el primer ciclo reactivo las animaciones
		if (self.loops == self.ret):
			self.vDISP.anim_list = True
			self.vDISP.anim_image = True
			
		if self.item_info and (self.eventpress not in ["item_info","no_event"]):	self.item_info = False
		self.MUSIC.loop()
		
		# pygame.display.set_caption("pyLAUNCH (frame:"+self.JOY.joyNAME()+")")
		# pygame.display.set_caption(self.KEY.lastEVENT+" - "+self.JOY.lastEVENT + " - " + last_event)
		
		if (self.frames % (self.ret*600)) == 0:  
			self.MUSIC.next()
			self.vDISP.anim_list = False
			self.vDISP.show_list = True
			self.vDISP.anim_image = False
			self.vDISP.show_image = True
			self.vDISP.show_title = True
			self.vDISP.show_stats = True
			self.vDISP.show_wall = True
			self.vDISP.anim_wall = False
			self.vDISP.refresh()

		last_event = self.eventpress
			

