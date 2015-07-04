# -*- coding: iso-8859-15 -*-
import inspect,os,pygame,random,plfiles,plvideo

shadowCACHE = None
txtCACHE = {}

def videoINIT(plMENU):
	# Inicialización de pyGame, del modo de vídeo y ocultación del ratón
	pygame.init()
	pygame.display.set_caption("pyLAUNCH v1.8")
	
	try:
		pygame.display.set_icon(pygame.image.load(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + "\\pylaunch.png"))
	except:
		plfiles._LOG("ERR.error loading APP icon " + os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + "\\pylaunch.png")

	if plMENU.CFG["screen_resolution"] == (0,0): plMENU.CFG["screen_resolution"] = (640,480)
	plMENU.main_screen = pygame.display.set_mode(plMENU.CFG["screen_resolution"],plMENU.CFG["video_options"])
	if plMENU.CFG["screen_fullscreen"]: pygame.mouse.set_visible(False)
	# Controlador del framerate
	plMENU.menu_clock = pygame.time.Clock()

def videoSPLASH(plMENU,size=(0,0)):
	# Ventana SPLASH para evitar robar el modo de video a otras aplicaciones

	# Ventana CENTRADA
	os.environ['SDL_VIDEO_CENTERED'] = '1'
	pygame.init()
	
	# Ventana SIN BORDE
	plMENU.main_screen = pygame.display.set_mode(size,pygame.NOFRAME)

def loadIMG(imgPATH):
	"""Carga una imagen y devuelve un objeto imagen"""
	if (len(imgPATH) > 0) and os.path.exists(imgPATH) and os.path.isfile(imgPATH):
		try:
			image = pygame.image.load(imgPATH)
			if image.get_alpha is None:	image = image.convert()
			else:					image = image.convert_alpha()
		except:
			plfiles._LOG("ERR.error loading image " + imgPATH)
	else:
		plfiles._LOG("ERR.invalid image path " + imgPATH)
		image = pygame.Surface((320,200)).convert()
		image.fill((255,0,0))
		
	return image

def sizeIMG(name,size=(0,0),type=0):
	"""Redimensiona un objeto imagen, utilizando el escalado más adecuado en cada momento
		name objeto img
		size nuevo tamaño que se le desea asignar
		type tipo de redimensionado a utilizar:
		0: (por defecto) Ajustarse exactamente a size
		1: Ajustarse a size manteniendo el ASPECT/RATIO
		2: Mantiene el aspect ratio pero no respeta el tamaño
		3: Ocupa todo el tamaño manteniendo aspect ratio y recortando sobrantes"""
		
	
	if (type == 1):			# Redimensionado (manteniendo aspect/ratio y ocupando todo el espacio)
		oldx = name.get_width()
		oldy = name.get_height()
		newx = int(round(size[0],0))
		newy = int(round(size[1],0))
		
		# Redimensiono a través del eje más corto (para cubrir/expandir todo)
		if (oldx < oldy):
			# Ajusto adaptando el EJEX al tamaño deseado
			nsize = (newx,(oldy * newx) / oldx)
			# Si no he llegado a la medida Y expando aun más
			if (nsize[1] < newy):
				oldx = nsize[0]
				oldy = nsize[1]
				nsize = ((oldx * newy) / oldy,newy)
		else:
			# Ajusto adaptando el EJEY al tamaño deseado
			nsize = ((oldx * newy) / oldy,newy)
			# Si no he llegado a la medida X expando aun más
			if (nsize[0] < newx):
				oldx = nsize[0]
				oldy = nsize[1]
				nsize = (newx,(oldy * newx) / oldx)
				
	elif (type == 2):		# Redimensionado (manteniendo aspect/ratio y mostrando toda la imágen)
		oldx = name.get_width()
		oldy = name.get_height()
		newx = int(round(size[0],0))
		newy = int(round(size[1],0))
		
		# Redimensiono a través del eje más largo (para mostrar todo)
		if (oldx > oldy):
			# Ajusto adaptando el EJEX al tamaño deseado
			nsize = (newx,int((oldy * newx) / oldx))
			# Si he superado la medida Y contraigo aun más (excepto para el tipo -2)
			if (nsize[1] > newy):
				oldx = nsize[0]
				oldy = nsize[1]
				nsize = (int((oldx * newy) / oldy),newy)
		else:
			# Ajusto adaptando el EJEY al tamaño deseado
			nsize = (int((oldx * newy) / oldy),newy)
			# Si he superado la medida X contraigo aun más (excepto para el tipo -2)
			if (nsize[0] > newx):
				oldx = nsize[0]
				oldy = nsize[1]
				nsize = (newx,int((oldy * newx) / oldx))

	elif (type == 3):		# Redimensionado (manteniendo aspect/ratio y recortando la imágen sobrante)
		copia = pygame.transform.scale(name.copy(), (int(size[0]),int(size[1])))
		name = sizeIMG(name,size,1)
		rect = name.get_rect()
		rect.centerx = copia.get_rect().centerx
		rect.centery = copia.get_rect().centery
		copia.blit(name,rect)
		name = copia.copy()
		nsize = (name.get_width(),name.get_height())

	else:
		# Redimensionamiento (forzado)
		nsize = (size[0],size[1])

	nsize = (int(round(nsize[0],0)),int(round(nsize[1],0)))

	try:
		# El smooth solo funciona a 16 y 24 bits
		name = pygame.transform.smoothscale(name, nsize)
	except:                     
		name = pygame.transform.scale(name, nsize)
	
	return name
	
	
class screenSAVER:
	def __init__(self,plMENU):

		# 1 Creo una lista completa de todas las imágenes almacenadas en theLIST y la desordeno
		self.plMENU = plMENU
		self.lstPHOTOS = []
		for lst in plMENU.LIST.lstCACHE:
			if not (lst in ["__MOST","__ALL","__FOUND"]):
				for img in plMENU.LIST.LST[lst]["_IMAGES_"]:
					img_path = os.path.join(plMENU.LIST.LST[lst]["list_image_dir"] , plMENU.LIST.LST[lst]["_IMAGES_"][img])
					self.lstPHOTOS.append((img_path,plMENU.LIST.LST[lst]["list_name"],plMENU.LIST.LST[lst]["_ITEMS_"][img]))
		random.shuffle(self.lstPHOTOS)
		
		# Superficie semitraslucida en negro para el fundido a negro
		self.blackSURFACE = pygame.Surface((plMENU.main_screen.get_width(),plMENU.main_screen.get_height())).convert()
		#self.blackSURFACE.set_alpha(1,pygame.RLEACCEL)
		self.txtSURFACE = self.blackSURFACE.copy()

		# Indicador de la foto activa, y tiempo restante para el cambio de foto
		self.photoINDEX = 0
		self.photoSPEED = plMENU.CFG["menu_speed"]*2
		
		# Foto transformada
		self.photoIMAGE = None
		self.photoOLD = None
		
		# Controlador de texto (y propiedades específicas)
		self.vTXT = plMENU.vTXTm
		self.txtCOLOR = plMENU.CFG["font2_color"]
		self.vTXT.mainALPHA = plMENU.CFG["font2_alpha"],plMENU.CFG["font2_alpha"],plMENU.CFG["font2_alpha"]
		self.vTXT.shadowALPHA = plMENU.CFG["font2_shadow_alpha"],plMENU.CFG["font2_shadow_alpha"],plMENU.CFG["font2_shadow_alpha"]

		self.photoTITLE = ""
		self.photoNAME = ""
		self.songNAME = ""
		
		self.loops = 0
		self.lastSONG = self.plMENU.MUSIC.song
		
		# Hay que hacer doblebuffer manualmente?
		if (plMENU.CFG["screen_hardware"] or plMENU.CFG["screen_dblbuffer"]):
			self.dblbuffer = False
		else:
			self.dblbuffer = True
				
		
		# Factores de aleatoriedad
		self.rndZOOM = 0.6		# Tamaño relativo con respecto a la pantalla
		self.rndROTATION = 6		# Grados posibles de inclinación
		self.rndPOSITION = 0		# Desviación posible en dimensiones de pantalla
		# En realidad el tamaño no es aleatorio, sino proporcional a las dimensiones de pantalla
		self.rndSIZE = (int(self.plMENU.main_screen.get_width()*self.rndZOOM),int(self.plMENU.main_screen.get_height()*self.rndZOOM))

	def musicSEEK(self):
		if (self.plMENU.eventpress == "next_song"): 
			self.plMENU.SAMPLER.play(self.plMENU.eventpress)
			self.plMENU.MUSIC.next()
		elif (self.plMENU.eventpress == "prev_song"): 
			self.plMENU.SAMPLER.play(self.plMENU.eventpress)
			self.plMENU.MUSIC.prev()

	def scrLOOP(self):
		
		# Calculo los valores iniciales y finales para X, Y, ZOOM y ROTACIÓN
		
		# Margen de desplazamiento en X e Y
		dx = self.plMENU.main_screen.get_width()*self.rndPOSITION
		dy = self.plMENU.main_screen.get_height()*self.rndPOSITION
		
		relTXT = ""
		relTXT2 = ""
		relTXT3 = ""
		relYPOS = int(self.plMENU.CFG["screen_resolution"][1]-(self.vTXT.font.size("O")[1]*3))
		
		self.vTXT.txtALIGN = 0
		self.plMENU.MUSIC.next()

		while (self.plMENU.eventpress in ("no_event","next_song","prev_song")):
			
			self.plMENU.MUSIC.loop()		# Con esto evito que la música pare de sonar
			self.photoOLD = self.photoIMAGE 

			# Valores aleatorios de X, Y, Zoom y Rotación
			aXi =(random.random()*dx)-(dx/2)
			aXf = aXi
			if (dx <> 0): 
				while (aXi == aXf): 
					aXf = (random.random()*dx)-(dx/2)
				
			aYi = (random.random()*dy)-int(dy/2)
			aYf = aYi
			if (dy <> 0): 
				while (aYi == aYf): 
					aYf = (random.random()*dy)-(dy/2)
				
			aZi = round(1 + (self.rndZOOM * random.random()),2)
			aZf = aZi
			while (abs(aZi-aZf) < (self.rndZOOM/10)): 
				aZf = round(1 + (self.rndZOOM * random.random()),2)
				
			aRi = random.randint(0,self.rndROTATION)-int(self.rndROTATION/2)
			aRf = aRi
			while (aRi == aRf): 
				aRf = random.randint(0,self.rndROTATION)-int(self.rndROTATION/2)
			
			self.photoIMAGE = pygame.transform.scale2x(loadIMG(self.lstPHOTOS[self.photoINDEX][0])).convert()
			self.photoIMAGE = sizeIMG(self.photoIMAGE,(self.plMENU.main_screen.get_width(),self.plMENU.main_screen.get_height()),3)
			self.photoTITLE = self.lstPHOTOS[self.photoINDEX][1]
			self.photoNAME = self.lstPHOTOS[self.photoINDEX][2]

			# Preparo los textos que se van a mostrar junto con las imágenes
			try: self.songNAME = os.path.basename(self.plMENU.MUSIC.playlist[self.plMENU.MUSIC.song])
			except: self.songNAME = "NO SONG FOUND"
			relTXT = self.photoNAME
			relTXT2 = self.photoTITLE
			relTXT3 = self.songNAME
			#self.vTXT.msg(self.photoIMAGE,relTXT,(-1,relYPOS),self.txtCOLOR)
			#self.vTXT.msg(self.photoIMAGE,relTXT2,(-1,relYPOS+self.vTXT.font.size("O")[1]),self.txtCOLOR)

			self.photoOLD = self.plMENU.main_screen.copy()

			tmpANIM = clockANIM(6,aXi,aXf,0)

			# Bucle con la animación (donde también evito bucles infinitos en las canciones)
			self.loops = self.loops + 1
			if (self.loops > 30):
				self.loops = 0
				self.plMENU.MUSIC.next()
				self.lastSONG = self.plMENU.MUSIC.song
			else:
				if (self.lastSONG != self.plMENU.MUSIC.song): 
					self.loops = 0
					self.lastSONG = self.plMENU.MUSIC.song
				
			while (not tmpANIM.end()) and (self.plMENU.eventpress in ("no_event","next_song","prev_song")):
				self.plMENU.main_screen.blit(self.txtSURFACE,(aXi,aXf))

				#if self.photoOLD <> None: self.photoOLD.draw(self.plMENU.main_screen,(tmpANIM.pos(relPOS[0],-self.plMENU.CFG["screen_resolution"][0]*1.5),relPOS[1]),relSIZ)
				#if self.photoIMAGE <> None: self.photoIMAGE.draw(self.plMENU.main_screen,(tmpANIM.val(),relPOS[1]),relSIZ)
				
				# Con .val() actualizo la anmación y los demás valores los calculo de forma relativa
				xA = tmpANIM.val()
				yA = tmpANIM.pos(aYi,aYf)
				zA = tmpANIM.pos(aZi,aZf)
				rA = tmpANIM.pos(aRi,aRf)
				aA = tmpANIM.pos(0,900)
				
				if self.photoIMAGE <> None: 
					# Preparo la imágen actual (con la rotación y el ZOOM correspondiente)
					finalIMAGE = pygame.transform.rotozoom(self.photoIMAGE, rA, zA)
					# Establezco la transpearencia (de la imágen actual) 0 trasnparete 255 opaco
					finalIMAGE.set_alpha(aA)
					# Si la imagen actual es trasnlucida pinto la imagen anterior primero
					if (aA <= 255): self.plMENU.main_screen.blit(self.photoOLD,(0,0))
					# Calculo el centro de la imágen (solo si hay rotación)
					rect = finalIMAGE.get_rect()
					rect.centerx = self.plMENU.main_screen.get_rect().centerx + xA
					rect.centery = self.plMENU.main_screen.get_rect().centery + yA
					self.plMENU.main_screen.blit(finalIMAGE,rect)
					# Dibujo los textos en una posición estática de la pantalla
					self.vTXT.msg(self.plMENU.main_screen,relTXT,(-1,relYPOS),self.txtCOLOR)
					self.vTXT.msg(self.plMENU.main_screen,relTXT2,(-1,relYPOS+self.vTXT.font.size("O")[1]),self.txtCOLOR)
					self.vTXT.msg(self.plMENU.main_screen,relTXT3,(-1,relYPOS+self.vTXT.font.size("O")[1]*2),self.txtCOLOR)

				if self.plMENU.JOY.joyPRESSED():
					self.plMENU.eventpress = self.plMENU.JOY.pressed()
				else:
					self.plMENU.eventpress = self.plMENU.KEY.pressed()

				self.musicSEEK()
				pygame.display.flip()
				self.plMENU.frames += 1
				self.plMENU.menu_clock.tick(self.plMENU.CFG["video_fps"])
			
			# al salir de la animación vuelvo a dibujar el último fotograma pero SIN texto
			# Preparo la imágen actual (con la rotación y el ZOOM correspondiente)
			finalIMAGE = pygame.transform.rotozoom(self.photoIMAGE, rA, zA)
			# Establezco la transpearencia (de la imágen actual) 0 trasnparete 255 opaco
			finalIMAGE.set_alpha(aA)
			# Calculo el centro de la imágen (solo si hay rotación)
			rect = finalIMAGE.get_rect()
			rect.centerx = self.plMENU.main_screen.get_rect().centerx + xA
			rect.centery = self.plMENU.main_screen.get_rect().centery + yA
			self.plMENU.main_screen.blit(finalIMAGE,rect)			

			if self.photoINDEX == (len(self.lstPHOTOS)-1): self.photoINDEX = 0
			else:	self.photoINDEX += 1
			
				
		# Restauro la alineación del texto.
		self.vTXT.txtALIGN = self.plMENU.CFG["font2_align"]





# Esta es la clase que gestionará las fotos de los items con su reflejo
class itemPHOTO:
	
	def __init__(self,image,ZOOM=0,EFFECTS=True,SCALE2x=False,SIZE=(0,0),noCACHE=False):
		# Tipo de ZOOM aplicable
		self._zoom = ZOOM	

		# Imágen base
		self._image = loadIMG(image)
		
		# Reflejo/Sombra?
		self._effects = EFFECTS
		self. _shadowsize = 4
		
		# Escala 2x (solo se aplica si la imagen es menor que la pantalla)?
		if SCALE2x:	self._image = pygame.transform.scale2x(self._image)
		
		# En los modos en que se muestran varias imágenes de diferente tamaño no hay caché de sombras
		self._nocache = noCACHE
		
		# Tamaño por defecto (el de la imágen en crudo)
		if ((SIZE[0] + SIZE[1]) <> 0):
			self._image = sizeIMG(self._image,SIZE,self._zoom)
			self._size = [self._image.get_width(),self._image.get_height()]
			self._lastSIZE = SIZE
			if self._effects:
				self._size[0] += self. _shadowsize
				self._size[1] *= 1.2
				self._size[1] = int(self._size[1])

			# Creo la "foto" con la sombra
			self.adapt()
		else:
			# No puedo crear la foto hasta el momento del dibujado
			self._photo = None
	
	def adapt(self,SIZE=(0,0)):
		if ((SIZE[0] + SIZE[1]) <> 0):
			self._lastSIZE = SIZE
			self._image = sizeIMG(self._image,SIZE,self._zoom)
			self._size = [self._image.get_width(),self._image.get_height()]
			if self._effects: 
				self._size[0] += self. _shadowsize
				self._size[1] *= 1.2
				self._size[1] = int(self._size[1])

		global shadowCACHE
		#shadowCACHE = None

		if self._effects:
			# Creo un bloque TEMPORAL de color/textura (que pueda contener la foto + reflejo( sombra)
			tmpSURFACE = pygame.Surface(self._size, pygame.SRCALPHA)
			reflectDIS = int(self._image.get_height()/50)
			
			if (type(shadowCACHE) == type(None)) or (self._zoom != 3) or (self._nocache):
				# Creo un canal alfa que contenga las máscaras (EN NEGRO-GRIS sobre fondo NEGRO)
				# (Si hay reflejo/sombra el canal alfa será el mismo para todo)
				alphaSURFACE = pygame.Surface(self._size, pygame.SRCALPHA)
				# Máscara para la foto
				alphaSURFACE.fill((0,0,0,0))
			
				# Máscara para la sombra
				alphaSURFACE.fill((44,44,44,0),(0,0,self._image.get_width()+self. _shadowsize,self._image.get_height()+self. _shadowsize))
				alphaSURFACE.fill((111,111,111,0),(int(self. _shadowsize/4),int(self. _shadowsize/4),self._image.get_width()+int(self. _shadowsize/2),self._image.get_height()+int(self. _shadowsize/2)))
				
				alphaSURFACE.fill((255,255,255,0),(int(self. _shadowsize/2),int(self. _shadowsize/2),self._image.get_width(),self._image.get_height()))
			
				# Máscara para el reflejo (en degradado)
				col = 155
				dif = self._size[1]-self._image.get_height()
				dif -= (self._image.get_height()/28)
				dif = round(col/dif)+2
				for ycoord in range(self._image.get_height()+reflectDIS,self._size[1]):
					col -= dif
					if (col < 0): col = 0
					pygame.draw.line(alphaSURFACE, (col,col,col), (int(self. _shadowsize/2),ycoord), (self._size[0]-int(self. _shadowsize/2),ycoord))
				photoMASK = pygame.surfarray.pixels3d(alphaSURFACE.convert(32))
				shadowCACHE = photoMASK
			else:
				photoMASK = shadowCACHE
			
			# Establezco la textura para el primer plano (foto+sombra)
			tmpSURFACE.blit(self._image,(int(self. _shadowsize/2),int(self. _shadowsize/2)))

			# Compongo el reflejo
			self._reflect = pygame.Surface((self._image.get_width(),self._image.get_height()*0.2),pygame.SRCALPHA).convert()
			self._reflect.blit(pygame.transform.flip(self._image,0,1),(0,0))
			tmpSURFACE.blit(self._reflect,(int(self. _shadowsize/2),self._image.get_height()+reflectDIS))
			
			# Combino el canal alfa con los bloque TEMPORAL de color/textura
			#self._photo = tmpSURFACE.convert_alpha()
			try:
				pygame.surfarray.pixels_alpha(tmpSURFACE)[:, :] = photoMASK[:, :, 0]
			except:
				pygame.surfarray.pixels_alpha(tmpSURFACE)[:, :] = photoMASK[:tmpSURFACE.get_width(), :tmpSURFACE.get_height(), 0]

			self._photo = tmpSURFACE
		else:
			self._photo = self._image
			
		# Si hay que redimensionar redimensiono, pero redimensionar por redimensionar es tontería
		#if (self._photo.get_width() <> self._size[0]) or (self._photo.get_height() <> self._size[1]): 
		#	self._photo = sizeIMG(self._photo,self._size,0)
		
		self._photoX = self._photo
		self._photoRECT = self._photoX.get_rect()
	
	# Dibuja el objeto en su posición relativa según su posición original, su posición final y un controlador de animación/tempo
	def draw_rel(self,surface,oPOS,nPOS,oSIZ,nSIZ,oANIM):
		# Calculo el tamaño y posición actuales
		aPOS = ( oANIM.pos(oPOS[0],nPOS[0]), oANIM.pos(oPOS[1],nPOS[1]) )
		aSIZ =  ( oANIM.pos(oSIZ[0],nSIZ[0]), oANIM.pos(oSIZ[1],nSIZ[1]) )
		
		self.draw(surface,aPOS,aSIZ)
		
	# La posicion será la posición en surface en la que se CENTRARÁ la imágen
	def draw(self,surface,position = (0,0), size = None):
		if (self._photo == None): 	self.adapt(size)
			
		if (size <> None) and ((size[0] <> self._lastSIZE[0]) or (size[1] <> self._lastSIZE[1])): 
			self._size = size
			self._photoX = sizeIMG(self._photo,self._size,self._zoom)
			self._photoRECT = self._photoX.get_rect()
			
		self._photoRECT.centerx = surface.get_rect(center=position).centerx
		self._photoRECT.centery = surface.get_rect(center=position).centery
		surface.blit(self._photoX,self._photoRECT)
		
		
		
		
		
# Controla la velocidad de una animación según el reloj del sistema
class clockANIM:
	def __init__(self,time,start_val=0,end_val=1,accel = 0,flex = 1):
		
		# Controladores para el tiempo
		
		self.start_time = pygame.time.get_ticks()
		self.end_time = self.start_time + (time * 1000)
		self.actual_time = pygame.time.get_ticks()
		self.total_time = self.end_time-self.start_time
		
		# Controladores para los valores
		self.start_val = start_val
		self.actual_val = start_val
		self.end_val = end_val
		self.range_val = end_val - start_val
		# En el modo de aceleración / deceleración la animación se divide en dos
		if (accel == 2) or (accel == -2):
			self.start_val1 = start_val
			self.mid_range = (self.range_val/2)
			self.start_val2 = (start_val + self.mid_range)
			self.start_time1 = self.start_time
			self.mid_time = self.total_time / 2
			self.start_time2 = self.start_time + self.mid_time
			self.mid_progress = 0.0
		
		# Porcentaje de progreso
		self.progress = 0.0
		
		# Flexibilidad / indice de aceleración de celetración / de la animación
		self.flex = flex
		
		# Tipo de aceleracion 0 = velocidad constante, 1 = aceleración, -1 deceleracion
		self.accel = accel
		

	# Según el reloj del sistema  devuelve el valor correspondiente
	def val(self):
		
		# Actualizo controladores de tiempo
		self.actual_time = pygame.time.get_ticks()
		if (self.actual_time >=  self.end_time): 
			self.actual_time = self.end_time
			self.actual_val = self.end_val
			self.progress = 1
		else:
			# Progreso total de la animación
			self.progress = float(self.actual_time-self.start_time) / float(self.total_time)

			if (self.accel == 1):	# Aceleración
				for num in range(self.flex):	self.progress *=  self.progress
				
			elif (self.accel == -1):	# Deceleración
				self.progress = 1 - self.progress
				for num in range(self.flex):	self.progress *=  self.progress
				self.progress = 1 - self.progress
				
			elif (self.accel == 2):	# Aceleracion (del 0 al 50%) / Deceleracion (del 51% al 100%)
				if (self.progress <= 0.50):
					self.mid_progress = float(self.actual_time-self.start_time1) / float(self.mid_time)
					for num in range(self.flex):	self.mid_progress *=  self.mid_progress
				else:
					self.mid_progress = float(self.actual_time-self.start_time2) / float(self.mid_time)
					self.mid_progress = 1 - self.mid_progress
					for num in range(self.flex):	self.mid_progress *=  self.mid_progress
					self.mid_progress = 1 - self.mid_progress
				
			elif (self.accel == -2):	# Deceleracion (del 0 al 50%) / Aceleracion (del 51% al 100%)
				if (self.progress <= 0.50):
					self.mid_progress = float(self.actual_time-self.start_time1) / float(self.mid_time)
					self.mid_progress = 1 - self.mid_progress
					for num in range(self.flex):	self.mid_progress *=  self.mid_progress
					self.mid_progress = 1 - self.mid_progress
				else:
					self.mid_progress = float(self.actual_time-self.start_time2) / float(self.mid_time)
					for num in range(self.flex):	self.mid_progress *=  self.mid_progress

		if (self.progress < 1) and ((self.accel == 2) or (self.accel == -2)):
			if (self.progress <= 0.50):
				self.actual_val = self.start_val1 + (self.mid_progress * self.mid_range)
			else:
				self.actual_val = self.start_val2 + (self.mid_progress * self.mid_range)
				
		else:
			self.actual_val = self.start_val + (self.progress * self.range_val)

		return self.actual_val
		
	# Según self.progress devuelve el valor actual para un rango	
	def pos(self,start_val,end_val):
		return start_val + (self.progress * (end_val - start_val))
		
			
	def end(self):
		return (self.actual_time >= self.end_time)
		

class bitmapTXT:
	def __init__(self, fontNAME="Arial",fontSIZE=22,shadow=1,shadowDISP=(2,2),shadowCOLOR=(0,0,0),fontBOLD=True):
		"""incialización de del objeto"""
		pygame.font.init()
		
		if os.path.exists(fontNAME) and os.path.isfile(fontNAME): self.font = pygame.font.Font(fontNAME, fontSIZE)	# Tipo y tamaño de letra predeterminado
		else:	self.font = pygame.font.Font(pygame.font.match_font(fontNAME), fontSIZE)	# Tipo y tamaño de letra predeterminado
		
		self.fontNAME = fontNAME
		self.fontSIZE = fontSIZE
		self.fontBOLD = fontBOLD
		self.font.set_bold(fontBOLD)
		self.shadow = shadow						# Tipo de sombra (0 sin sombra, 1 sombra normal, 2 borde)
		self.shadowDISP = shadowDISP				# Desplazamiento de la sombra
		self.shadowCOLOR = shadowCOLOR				# Color de la sombra
		self.mainALPHA = (255,255,255)				# Transparencia del texto principal
		self.shadowALPHA = (155,155,155)				# Transparencia del las sombras
		self.interCHAR = -(shadowDISP[0])				# Espaciado entre caracteres
		self.txtALIGN = 0							# Alineación del texto (-1 izquierda, 0 centrado, 1 derecha)
		self.antiALIAS = True						# Usar antialias en el dibujado?
		
	def get_dim(self,txt=""):
		if (len(txt) == 0): txt = "iOljgK|\({¿$"
		return self.msg(None,txt,(0,0),(255,255,255))
		
	def msg(self,scrSURFACE,txt="",position=(0,0),color=(255,255,255)):
		"""Dibuja un mensaje de texto carácter a carácter"""
		global txtCACHE
		
		bitmapCHARS = range(0,len(txt))
		txtDIM = [0,0]
		xPOS = 0
		yPOS = 0
		
		for lnC in range(0,len(txt)):
			char = txt[lnC]
			char_id = char+self.fontNAME+str(self.fontSIZE)+str(self.shadow)+str(self.fontBOLD)+str(self.shadowDISP)+str(self.shadowCOLOR)+str(color)+str(self.antiALIAS)+str(self.mainALPHA)+str(self.shadowALPHA)
			
			if char_id in txtCACHE.keys():
				# Se encuentra en cache
				bitmapCHARS[lnC] = txtCACHE[char_id]
				xPOS += (bitmapCHARS[lnC].get_width() + self.interCHAR)
				if (yPOS < bitmapCHARS[lnC].get_height()): yPOS = bitmapCHARS[lnC].get_height()
			else:
				# No se encuentra en cache
				
				# Creo un bloque TEMPORAL de color/textura (que pueda contener el texto más la sombra)
				txtW, txtH = self.font.size(char)
				
				if (self.shadow == 1):
					#Sombra proyectada en perspectiva
					txtW += self.shadowDISP[0]
					txtH += self.shadowDISP[1]
				elif (self.shadow == 2):
					#Sombra tipo aureola
					txtW += (self.shadowDISP[0]*2)
					txtH += self.shadowDISP[1]*2
				
				# Simultáneamente creo la superficie de color y la superficie de transparencia
				tmpSURFACE = pygame.Surface((txtW, txtH), pygame.SRCALPHA)
				alphaSURFACE = pygame.Surface((txtW, txtH), pygame.SRCALPHA)
				
				# En la superficie alpha NEGRO ES TRANSPARENTE y BLANCO OPACO
				alphaSURFACE.fill((0,0,0))
				tmpSURFACE.fill((0,0,0))
				
				# La posición de dibujado del texto principal puede verse afectada por la sombra y el tamaño del que disponemos
				txtDIM = (0,0)
				
				# Dibujo la sombras y los colores de forma simultánea
				if (self.shadow == 1): 
					# Reajusto las posiciones para que nada sobrepase los límites de las superficies
					if (self.shadowDISP[0] < 0):
						txtDIM[0] -= self.shadowDISP[0]
						self.shadowDISP[0] = 0
					if (self.shadowDISP[1] < 0):
						txtDIM[1] -= self.shadowDISP[1]
						self.shadowDISP[1] = 0

					# Dibujo dos transparencias, EL TEXTO PRINCIPAL SIEMPRE DESPUES DE LA SOMBRA
					alphaSURFACE.blit(self.font.render(char,self.antiALIAS,self.shadowALPHA,(0,0,0,0)),self.shadowDISP)
					alphaSURFACE.blit(self.font.render(char,self.antiALIAS,self.mainALPHA),txtDIM)
					
					# Dibujo los colores, EL TEXTO PRINCIPAL SIEMPRE DESPUES DE LA SOMBRA
					tmpSURFACE.blit(self.font.render(char,self.antiALIAS,self.shadowCOLOR,(0,0,0,0)),self.shadowDISP)
					tmpSURFACE.blit(self.font.render(char,self.antiALIAS,color),txtDIM)
					
				elif (self.shadow == 2): 
					# Pinto las sombras y sus colores
					for xLOOP in range(0,(self.shadowDISP[0]*2)+1):
						for yLOOP in range(0,(self.shadowDISP[1]*2)+1):
							# Dibujo dos transparencias, EL TEXTO PRINCIPAL SIEMPRE DESPUES DE LA SOMBRA
							txtDIM = xLOOP,yLOOP
							if (xLOOP == 0) and (yLOOP == 0):
								alphaSURFACE.blit(self.font.render(char,self.antiALIAS,self.shadowALPHA,(0,0,0,0)),txtDIM)
								tmpSURFACE.blit(self.font.render(char,self.antiALIAS,self.shadowCOLOR,(0,0,0,0)),txtDIM)
							else:
								alphaSURFACE.blit(self.font.render(char,self.antiALIAS,self.shadowALPHA),txtDIM)
								tmpSURFACE.blit(self.font.render(char,self.antiALIAS,self.shadowCOLOR),txtDIM)
								
					# Pinto el texto principal y sus colores
					alphaSURFACE.blit(self.font.render(char,self.antiALIAS,self.mainALPHA),self.shadowDISP)
					tmpSURFACE.blit(self.font.render(char,self.antiALIAS,color),self.shadowDISP)
				
				# Combino ambas capas
				alphaMASK = pygame.surfarray.pixels3d(alphaSURFACE.convert(32))
				pygame.surfarray.pixels_alpha(tmpSURFACE)[:, :] = alphaMASK[:, :, 0]

				# Guardo en la cache el trabajo realizado para esta letra
				txtCACHE[char_id] = tmpSURFACE
				bitmapCHARS[lnC] = tmpSURFACE
				xPOS += (tmpSURFACE.get_width() + self.interCHAR)
				if (yPOS < tmpSURFACE.get_height()): yPOS = tmpSURFACE.get_height()
		
		# Finalmente las dimensiones totales del texto quedan aquí almacenadas
		txtDIM = xPOS,yPOS

		# Si no se indicó superficie es que solo se pretendía medir
		if (type(scrSURFACE) != type(None)):
			# Los valores -1 de posición solicitan el centrado
			if (position[0] == -1): 
				# Texto centrado
				if (self.txtALIGN == 0):	xPOS = int((scrSURFACE.get_width()/2) - (xPOS/2))
				# Alineación a la derecha
				elif (self.txtALIGN == 1):	xPOS = int(scrSURFACE.get_width()/2) - xPOS
				# (La alineación a la izquierda no varía la posición X)
				else:					xPOS = int(scrSURFACE.get_width()/2)
			else:
				# Texto centrado
				if (self.txtALIGN == 0):	
					xPOS = position[0] - int(xPOS/2)
				# Alineación a la derecha
				elif (self.txtALIGN == 1):	xPOS = position[0] - xPOS
				# (La alineación a la izquierda no varía la posición X)
				else:					xPOS = position[0]

			if (position[1] == -1): 		yPOS = int((scrSURFACE.get_height()/2) - (yPOS/2))
			else:					yPOS = (position[1] - int(yPOS/2))
				
			# Finalmente procedo al dibujado
			for lnC in range(0,len(txt)):
				scrSURFACE.blit(bitmapCHARS[lnC],(xPOS,yPOS))
				xPOS += (bitmapCHARS[lnC].get_width() + self.interCHAR)
			
		return txtDIM


# Esta clase es la encargada de actualizar los textos de las posiciones fijas de pantalla
class vidRENDER:
	"""Objeto encargado de mostrar textos en posiciones fijas de pantalla"""

	def __init__(self,plMENU):
		self.last_song = -1		# Última canción que se ha reproducido
		self.last_list = ""			# Última lista consultada
		self.last_item = ""		# Último item consultado
		self.plMENU = plMENU		# Vínculo con la clase menu
		
		self.show_title = True		# Indica si se muestra o no el título
		self.show_stats = True		# Indica si se muestran o no los stats
		# Las animaciones de title y stats se asocian directamente al wallpaper
		self.show_image = True	# Indica si se muestra o no la imagen del item
		self.anim_image = True		# Indica si se anima o no la imágen del item
		self.show_list = True		# Indica si se muestra o no la lista de items
		self.anim_list = True		# Indica si se anima o no la lista de items
		self.show_wall = True		# Indica si se muestra o no el wallpaper
		self.anim_wall = True		# Indica si se anima o no el cambio de wallpaper
		
		self.key_animation =  False		# Indica si se realizan animaciones (en función de la frecuencia del teclado)
		
		# Controladores para cambios en la lista
		self.song_change = False
		self.list_change = False
		self.item_change = False
		self.search_change = False
		self.inloop = 1
		self.maxLOOP = plMENU.CFG["menu_kloop"]

		
		# Dimensiones de la pantalla
		self.screenWIDTH = plMENU.CFG["screen_resolution"][0]
		self.screenHEIGHT = plMENU.CFG["screen_resolution"][1]
		
		# Dimensiones de la imagen principal (solo utilizadas en modo glaunch)
		self._xsize = (round(self.screenWIDTH/1.15),round(self.screenHEIGHT/1.3))
		
		self.vSEP = self.plMENU.vTXTm.get_dim()[1]  # Separador vertical por tamaño de tipo de fuente
		self.vSEP += self.plMENU.CFG["font2_ver_sep"]
		
		# Variables para la animación/dibujado de la lista de ITEMS/TEXTO
		#self.vINI = int((self.screenHEIGHT / 40)+(self.vSEP/2))	# Posición vertical del primer texto
		self.vINI = int(self.vSEP/1.2)

		if (self.plMENU.CFG["menu_style"] == 0):	# Tipo GLAUNCH
			self.vINI *= 2.5
			self.vINI = int(self.vINI)
		elif (self.plMENU.CFG["menu_style"] == 1) or (self.plMENU.CFG["menu_style"] == 2):	# Estilo CENTRADO
			self.vINI *= 35
			self.vINI = int(self.vINI)

		self.nMAX =  int (self.screenHEIGHT/ self.vSEP) - 3	# Número máximo de elementos
		self.nMED = int(self.nMAX/2)
				
		# Inicializo la lista de fotos y sus rectángulos (posiciones y tamaños)
		if (self.plMENU.CFG["menu_style"] == 1) or (self.plMENU.CFG["menu_style"] == 2) :	# Estilo CENTRADO/DASHBOARD
			self._photo = [[None,[0,0,0,0]],[None,[0,0,0,0]],[None,[0,0,0,0]],[None,[0,0,0,0]],[None,[0,0,0,0,0,0]],[None,[0,0,0,0]],[None,[0,0,0,0]]]
		
		if (self.plMENU.CFG["menu_style"] == 1):	# Estilo CENTRADO
			ycoord = int(self.screenHEIGHT/60)*26
			# 0,1 = posicion X e Y   2,3 = tamaño X e Y  4,5 = temporales
			self._photo[0][1][0] = int(self.screenWIDTH/9)*8 + (int(self.screenWIDTH/9)*2)
			self._photo[0][1][1] = ycoord
			self._photo[0][1][2] = int(self.screenWIDTH/4)
			self._photo[0][1][3] = int(self.screenHEIGHT/4)

			self._photo[1][1][0] = int(self.screenWIDTH/9)*8
			self._photo[1][1][1] = ycoord
			self._photo[1][1][2] = int(self.screenWIDTH/4)
			self._photo[1][1][3] = int(self.screenHEIGHT/4)

			self._photo[2][1][0] = int((self.screenWIDTH/9)*6.5)
			self._photo[2][1][1] = ycoord
			self._photo[2][1][2] = int(self.screenWIDTH/3)
			self._photo[2][1][3] = int(self.screenHEIGHT/3)

			self._photo[3][1][0] = int(self.screenWIDTH/2)
			self._photo[3][1][1] = ycoord
			self._photo[3][1][2] = int(self.screenWIDTH/2)
			self._photo[3][1][3] = int(self.screenHEIGHT/2)

			self._photo[4][1][0] = int((self.screenWIDTH/9)*2.5)
			self._photo[4][1][1] = ycoord
			self._photo[4][1][2] = int(self.screenWIDTH/3)
			self._photo[4][1][3] = int(self.screenHEIGHT/3)

			self._photo[5][1][0] = int(self.screenWIDTH/9)*1
			self._photo[5][1][1] = ycoord
			self._photo[5][1][2] = int(self.screenWIDTH/4)
			self._photo[5][1][3] = int(self.screenHEIGHT/4)

			self._photo[6][1][0] = int(self.screenWIDTH/9)*1 - (int(self.screenWIDTH/9)*2)
			self._photo[6][1][1] = ycoord
			self._photo[6][1][2] = int(self.screenWIDTH/4)
			self._photo[6][1][3] = int(self.screenHEIGHT/4)

		if (self.plMENU.CFG["menu_style"] == 2):	# Estilo DASHBOARD
			ycoord = int(self.screenHEIGHT/60)*26
			# 0,1 = posicion X e Y   2,3 = tamaño X e Y  4,5 = temporales
			self._photo[5][1][0] = -(int(self.screenWIDTH/9)*2.5)
			self._photo[5][1][1] = ycoord
			self._photo[5][1][2] = int(self.screenWIDTH/2)
			self._photo[5][1][3] = int(self.screenHEIGHT/2)

			self._photo[4][1][0] = int(self.screenWIDTH/9)*2.5
			self._photo[4][1][1] = ycoord
			self._photo[4][1][2] = int(self.screenWIDTH/2)
			self._photo[4][1][3] = int(self.screenHEIGHT/2)
			
			ycoord *= 1.10
			self._photo[3][1][0] = int((self.screenWIDTH/9)*5.5)
			self._photo[3][1][1] = ycoord
			self._photo[3][1][2] = int(self.screenWIDTH/3)
			self._photo[3][1][3] = int(self.screenHEIGHT/3)
			
			ycoord *= 1.05
			self._photo[2][1][0] = int((self.screenWIDTH/9)*7)
			self._photo[2][1][1] = ycoord
			self._photo[2][1][2] = int(self.screenWIDTH/4)
			self._photo[2][1][3] = int(self.screenHEIGHT/4)
			
			ycoord *= 1.025
			self._photo[1][1][0] = int((self.screenWIDTH/9)*8)
			self._photo[1][1][1] = ycoord
			self._photo[1][1][2] = int(self.screenWIDTH/5)
			self._photo[1][1][3] = int(self.screenHEIGHT/5)

			self._photo[0][1][0] = int((self.screenWIDTH/9)*8) + (int(self.screenWIDTH/9)*2)
			self._photo[0][1][1] = ycoord
			self._photo[0][1][2] = int(self.screenWIDTH/5)
			self._photo[0][1][3] = int(self.screenHEIGHT/5)

		# Superficie sobre la que se dibujará el texto
		self.txtSURFACE = self.plMENU.main_screen.copy()
		self.txtSURFACE = self.txtSURFACE.convert_alpha()
		self.txtSURFACE.fill((0,0,0,0))	# Realmente el color de esta superficie es indiferente (solo será visible el texto)
		
		self.txtBACKUP = self.txtSURFACE.copy()
		
		# Superficie de transparencias para el texto
		self.alphaSURFACE = self.txtSURFACE.copy()
		self.alphaSURFACE.fill((0,0,0,0))	# Negro transparente, blanco, visible (aquí el color si es importante)
		
		self.alphaBACKUP = self.alphaSURFACE.copy()
		
		self.aTIME = self.plMENU.CFG["menu_speed"] 		# Velocidad de la animacion



	def scan_changes(self):
		disp_change = False
		# Devolverá True si se ha producido cambios y False si no
		
		if (self.last_song <> self.plMENU.MUSIC.song):
			self.last_song = self.plMENU.MUSIC.song
			self.song_change = True
		else:
			self.song_change = False
			

		if (self.last_item <> self.plMENU.LIST.getitem()):
			self.last_item = self.plMENU.LIST.getitem()
			self.item_change = True
		else:
			self.item_change = False

		if (self.last_list <> self.plMENU.LIST.getlist()):
			self.last_list = self.plMENU.LIST.getlist()
			self.list_change = True
		else:
			self.list_change = False
			
		if (self.plMENU.search <> self.plMENU.last_search):
			self.plMENU.last_search = self.plMENU.search
			self.search_change = True
		else:
			self.search_change = False
			
		disp_change = self.song_change or self.list_change or self.item_change or self.search_change

		return disp_change
	


	# Dibuja los textos "fijos" de título y estado
	def title_and_stats(self):
		# 1. Título de la lista (centrado en X)		
		if self.show_title:
			# Situación según alineado del texto IZQUIERDA, CENTRO, DERECHA
			margen = int(self.plMENU.vTXT.get_dim()[1]/2)
			if self.plMENU.CFG["font1_align"] == -1: xcoord = margen
			elif self.plMENU.CFG["font1_align"] == 0: xcoord = -1
			elif self.plMENU.CFG["font1_align"] == 1: xcoord = self.screenWIDTH - margen
			ycoord = int(margen*1.2)
			
			if (self.plMENU.LIST.actual_list_name == "__MOST"):
				txtMSG = self.plMENU.CFG["fav_list_name"]
				txtMSG = txtMSG.replace("*list*",self.plMENU.LIST.getlist("list_name"))
			elif (self.plMENU.LIST.actual_list_name == "__FOUND"):
				if self.plMENU.finding:
					txtMSG = "SEARCH: "+self.plMENU.search
				else:
					txtMSG = self.plMENU.LIST.getlist("list_name")
			else:
				txtMSG = self.plMENU.LIST.getlist("list_name")
			
			self.plMENU.vTXT.msg(self.plMENU.main_screen,txtMSG,(xcoord,ycoord),self.plMENU.CFG["font1_color"])

		# 2. Información de estado
		if self.show_stats:
			txtMSG = self.plMENU.CFG["menu_stats"]
			if len(txtMSG) > 0:
				# list_id, item_id, list_name, item_name, song_name,item_order,item_count,list_order,list_count,song_order,song_count
				if "*list_id*" in txtMSG: txtMSG = txtMSG.replace("*list_id*",self.plMENU.LIST.getlist())
				if "*item_id*" in txtMSG: txtMSG = txtMSG.replace("*item_id*",self.plMENU.LIST.getitem())
				if "*list_name*" in txtMSG: txtMSG = txtMSG.replace("*list_name*",self.plMENU.LIST.getlist("list_name"))
				if "*item_name*" in txtMSG: txtMSG = txtMSG.replace("*item_name*",self.plMENU.LIST.getitem(0,1))
				if "*song_name*" in txtMSG: 
					try: txtMSG = txtMSG.replace("*song_name*",os.path.basename(self.plMENU.MUSIC.playlist[self.plMENU.MUSIC.song]))
					except: txtMSG = txtMSG.replace("*song_name*","NO SONG FOUND")
				if "*list_order*" in txtMSG: txtMSG = txtMSG.replace("*list_order*",str(self.plMENU.LIST.actual_list_index+1))
				if "*list_count*" in txtMSG: txtMSG = txtMSG.replace("*list_count*",str(len(self.plMENU.LIST.LST)))
				if "*item_order*" in txtMSG: 
					try: txtMSG = txtMSG.replace("*item_order*",str(self.plMENU.LIST.LST[self.plMENU.LIST.actual_list_name]["_ACTUAL_ITEM_INDEX"]+1))
					except: txtMSG = "-1"
				if "*item_count*" in txtMSG: txtMSG = txtMSG.replace("*item_count*",str(len(self.plMENU.LIST.LST[self.plMENU.LIST.actual_list_name]["_CACHE_"])))
				if "*song_order*" in txtMSG: txtMSG = txtMSG.replace("*song_order*",str(self.plMENU.MUSIC.song+1))
				if "*song_count*" in txtMSG: txtMSG = txtMSG.replace("*song_count*",str(len(self.plMENU.MUSIC.playlist)))
				if "*fps*" in txtMSG: txtMSG = txtMSG.replace("*fps*",str(round(self.plMENU.menu_clock.get_fps())))
				if "*all_count*" in txtMSG: txtMSG = txtMSG.replace("*all_count*",str(self.plMENU.LIST.globalCOUNT))
				
				# Situación según alineado del texto IZQUIERDA, CENTRO, DERECHA
				margen = int(self.plMENU.vTXTp.get_dim()[1]/2)
				if self.plMENU.CFG["font3_align"] == -1: xcoord = margen
				elif self.plMENU.CFG["font3_align"] == 0: xcoord = -1
				elif self.plMENU.CFG["font3_align"] == 1: xcoord = self.screenWIDTH - margen
				ycoord = int(self.screenHEIGHT-(margen*1.2))

				devTXT = self.plMENU.vTXTp.msg(self.plMENU.main_screen,txtMSG,(xcoord,ycoord),self.plMENU.CFG["font3_color"])


	# Dibuja la lista de items
	def item_list(self):
		"""Existen tres formas de dibujar la lista,
			1.-insertando todos los elementos, 
			2.-insertando un elemento arriba, 
			3.-insertando un elemento abajo"""
		
		if self.show_list:
			drawMODE = 0
			mSEP = int(self.vSEP/2)
			# Situación según alineado del texto IZQUIERDA, CENTRO, DERECHA
			margen = self.plMENU.vTXTm.get_dim()[1]
			if self.plMENU.CFG["font2_align"] == -1: xcoord = margen
			elif self.plMENU.CFG["font2_align"] == 0: xcoord = -1
			elif self.plMENU.CFG["font2_align"] == 1: xcoord = self.screenWIDTH - margen
			ycoord = self.vINI
			main_alpha = 0
			shadow_alpha = 0
			main_color = self.plMENU.CFG["font2_color"]
			
			# Determino la forma en la que tengo que dibujar la lista
			if (self.plMENU.eventpress == "next_item"): drawMODE = -1	# Insertar abajo
			elif (self.plMENU.eventpress == "prev_item"): drawMODE = 1	# Insertar arriba
			else: drawMODE = 0									# Dibujar todo
			
			self.txtSURFACE.fill((0,0,0,0))

			# REDIBUJAR SOLO UNA PARTE
			if (drawMODE <> 0):
				# Desplazo la superficie con las letras
				self.txtSURFACE.blit(self.txtBACKUP,(0,self.vSEP*drawMODE))
				
				# SUBIENDO: Borro todo lo que hay por encima de ycoord
				if (drawMODE == -1): self.txtSURFACE.fill((0,0,0,0),(0,0,self.txtSURFACE.get_width(),ycoord-(mSEP-1)))

				# Actualizo los elementos PRE/POST-CENTRAL,CENTRAL y ÚLTIMO/PRIMERO (los demás no los dibujo)
				for loop in range(self.nMAX+1):
					# PRIMER/ULTIMO ELEMENTO
					if ((drawMODE == -1) and (loop == self.nMAX)) or ((drawMODE == 1) and (loop == 0)):
						# Actualizo las transparencias
						main_alpha =self.plMENU.CFG["text_alpha"]
						shadow_alpha = self.plMENU.CFG["text_alpha"]
						self.plMENU.vTXTm.mainALPHA = main_alpha,main_alpha,main_alpha
						self.plMENU.vTXTm.shadowALPHA = shadow_alpha,shadow_alpha,shadow_alpha
						self.plMENU.vTXTm.msg(self.txtSURFACE,self.plMENU.LIST.getitem((loop-self.nMED),1),(xcoord,ycoord),main_color)
						
					# ANTERIOR/POSTERIOR AL CENTRAL
					elif (loop == (self.nMED+drawMODE)): 
						# Borro ANTES de dibujar
						self.txtSURFACE.fill((0,0,0,0),(0,ycoord-mSEP,self.txtSURFACE.get_width(),self.vSEP))
						main_alpha =self.plMENU.CFG["text_alpha"]
						shadow_alpha = self.plMENU.CFG["text_alpha"]
						self.plMENU.vTXTm.mainALPHA = main_alpha,main_alpha,main_alpha
						self.plMENU.vTXTm.shadowALPHA = shadow_alpha,shadow_alpha,shadow_alpha
						self.plMENU.vTXTm.msg(self.txtSURFACE,self.plMENU.LIST.getitem((loop-self.nMED),1),(xcoord,ycoord),main_color)
						
					# CENTRAL
					elif (loop == self.nMED):
						main_alpha = self.plMENU.CFG["font2_alpha"]
						shadow_alpha = self.plMENU.CFG["font2_shadow_alpha"]
						self.plMENU.vTXTm.mainALPHA = main_alpha,main_alpha,main_alpha
						self.plMENU.vTXTm.shadowALPHA = shadow_alpha,shadow_alpha,shadow_alpha
						self.plMENU.vTXTm.msg(self.txtSURFACE,self.plMENU.LIST.getitem((loop-self.nMED),1),(xcoord,ycoord),main_color)

					ycoord += self.vSEP

				# BAJANDO: Borro todo lo que hay por debajo de ycoord
				if (drawMODE == 1): self.txtSURFACE.fill((0,0,0,0),(0,ycoord-mSEP+1,self.txtSURFACE.get_width(),self.txtSURFACE.get_height()-(ycoord-mSEP)))
			else:
				# Actualizo todo
				for loop in range(self.nMAX+1):
					if (loop <> self.nMED): 
						main_alpha =self.plMENU.CFG["text_alpha"]
						shadow_alpha = self.plMENU.CFG["text_alpha"]
						self.plMENU.vTXTm.mainALPHA = main_alpha,main_alpha,main_alpha
						self.plMENU.vTXTm.shadowALPHA = shadow_alpha,shadow_alpha,shadow_alpha
						self.plMENU.vTXTm.msg(self.txtSURFACE,self.plMENU.LIST.getitem((loop-self.nMED),1),(xcoord,ycoord),main_color)
					else: 
						main_alpha = self.plMENU.CFG["font2_alpha"]
						shadow_alpha = self.plMENU.CFG["font2_shadow_alpha"]
						self.plMENU.vTXTm.mainALPHA = main_alpha,main_alpha,main_alpha
						self.plMENU.vTXTm.shadowALPHA = shadow_alpha,shadow_alpha,shadow_alpha
						self.plMENU.vTXTm.msg(self.txtSURFACE,self.plMENU.LIST.getitem((loop-self.nMED),1),(xcoord,ycoord),main_color)
					ycoord += self.vSEP
				
			# Combino el canal alfa con los bloque TEMPORAL de color/textura
			self.txtBACKUP = self.txtSURFACE.copy()


	# Redibuja la imagen o imagenes de los items
	def draw_scene(self):

		# Situación según alineado del texto IZQUIERDA, CENTRO, DERECHA
		margen = int(self.plMENU.vTXT.get_dim()[1]/2)
		if self.plMENU.CFG["font2_align"] == -1: xcoord = int(self.screenWIDTH / 2) + (margen * 2)
		elif self.plMENU.CFG["font2_align"] == 0: xcoord = int(self.screenWIDTH / 2)
		elif self.plMENU.CFG["font2_align"] == 1: xcoord = int(self.screenWIDTH / 2) - (margen * 2)

		ycoord = int(self.screenHEIGHT/2)
		
		# Si no hay sombra, la imagen está más desplazada hacia arriba
		if self.plMENU.CFG["snap_shadow"] :	ycoord = ycoord + (int(self.screenHEIGHT / 60) * 4)
		else:  						ycoord = ycoord + (int(self.screenHEIGHT / 60) * 2)
		
		# El efecto de sonido correspondiente (salvo que se haya pulsado SALIR)
		if (self.plMENU.eventpress != "exit_menu") : self.plMENU.SAMPLER.play(self.plMENU.eventpress)

		if self.anim_list or self.anim_image:	self.base_screen = self.plMENU.main_screen.copy()

		if (self.plMENU.CFG["menu_style"] == 0):	# MODO GLAUNCH
			if self.anim_list or self.anim_image:
				# Comienzo una animación de scroll (que puede variar de dirección)
				aVEL =  self.aTIME - ((self.aTIME / self.maxLOOP) * self.inloop)
				txtANIM = clockANIM(aVEL,self.vSEP,0,-1)
				
				#if (self.plMENU.KEY.lastEVENT == "next_item"):
				if (self.plMENU.eventpress == "next_item"):	
					while not txtANIM.end():
						self.plMENU.main_screen.blit(self.base_screen, (0,0))
						
						if self.anim_image:
							photoDESP = round(txtANIM.pos(self.screenHEIGHT,0))
							oPOS = (xcoord,ycoord-(self.screenHEIGHT-photoDESP))
							nPOS = (xcoord,ycoord+(photoDESP))
							oPOS = (oPOS[0]+self.plMENU.CFG["snap_position"][0],oPOS[1]+self.plMENU.CFG["snap_position"][1])
							nPOS = (nPOS[0]+self.plMENU.CFG["snap_position"][0],nPOS[1]+self.plMENU.CFG["snap_position"][1])
							try:
								self.lastPHOTO.draw(self.plMENU.main_screen,oPOS,self._xsize)
								self.photoMAIN.draw(self.plMENU.main_screen,nPOS,self._xsize)
							except:
								print "ERR"
								
						
						if self.anim_list:
							txtDESP = round(txtANIM.val())
							self.plMENU.main_screen.blit(self.txtSURFACE, (0,txtDESP))
						
						self.title_and_stats()
						pygame.display.flip()
						
						self.plMENU.frames += 1
						self.plMENU.menu_clock.tick(self.plMENU.CFG["video_fps"])
			
				if (self.plMENU.eventpress == "prev_item"):
					while not txtANIM.end():
						self.plMENU.main_screen.blit(self.base_screen, (0,0))
						
						if self.anim_image:
							photoDESP = round(txtANIM.pos(self.screenHEIGHT,0))
							oPOS = (xcoord,ycoord+(self.screenHEIGHT-photoDESP))
							nPOS = (xcoord,ycoord-(photoDESP))
							oPOS = (oPOS[0]+self.plMENU.CFG["snap_position"][0],oPOS[1]+self.plMENU.CFG["snap_position"][1])
							nPOS = (nPOS[0]+self.plMENU.CFG["snap_position"][0],nPOS[1]+self.plMENU.CFG["snap_position"][1])
							try:
								self.lastPHOTO.draw(self.plMENU.main_screen,oPOS,self._xsize)
								self.photoMAIN.draw(self.plMENU.main_screen,nPOS,self._xsize)
							except:
								print "ERR"

						if self.anim_list:
							txtDESP = round(txtANIM.val())
							self.plMENU.main_screen.blit(self.txtSURFACE, (0,-txtDESP))
						
						self.title_and_stats()
						pygame.display.flip()
						
						self.plMENU.frames += 1
						self.plMENU.menu_clock.tick(self.plMENU.CFG["video_fps"])

			else:
				
				if self.show_image:
					# La fotografía hay que dibujarla siempre que se acaba un bucle...
					nPOS = (xcoord,ycoord)
					nPOS = (nPOS[0]+self.plMENU.CFG["snap_position"][0],nPOS[1]+self.plMENU.CFG["snap_position"][1])
					self.photoMAIN.draw(self.plMENU.main_screen,nPOS,self._xsize)

				# Los textos
				if self.show_list:	self.plMENU.main_screen.blit(self.txtSURFACE,(0,0))
			
		elif (self.plMENU.CFG["menu_style"] == 1):	# MODO CENTRADO

			if self.anim_list or self.anim_image:
				# Comienzo una animación de scroll (que puede variar de dirección)
				txtANIM = clockANIM(self.aTIME,self.vSEP,0)
				if (self.plMENU.eventpress == "next_item"):
					while not txtANIM.end():
						txtDESP =round(txtANIM.val())
						self.plMENU.main_screen.blit(self.base_screen, (0,0))
						
						# Bucle de dibujado de forma ordenada, según "altitud"
						for iTEM in (6,1,5,2,4,3):
							oPOS = (self._photo[iTEM-1][1][0],self._photo[iTEM-1][1][1])
							nPOS = (self._photo[iTEM][1][0],self._photo[iTEM][1][1])
							oPOS = (oPOS[0]+self.plMENU.CFG["snap_position"][0],oPOS[1]+self.plMENU.CFG["snap_position"][1])
							nPOS = (nPOS[0]+self.plMENU.CFG["snap_position"][0],nPOS[1]+self.plMENU.CFG["snap_position"][1])
							oSIZ = (self._photo[iTEM-1][1][2],self._photo[iTEM-1][1][3])
							nSIZ = (self._photo[iTEM][1][2],self._photo[iTEM][1][3])
							try: self._photo[iTEM][0].draw(self.plMENU.main_screen,oPOS,nPOS,oSIZ,nSIZ,txtANIM)
							except: print("ERR. ITEM:",iTEM)

						self.plMENU.main_screen.blit(self.txtSURFACE, (0,txtDESP))
						pygame.display.flip()
						
						self.plMENU.frames += 1
						self.plMENU.menu_clock.tick(self.plMENU.CFG["video_fps"])
				else:
					while not txtANIM.end() :
						txtDESP = round(txtANIM.val())
						self.plMENU.main_screen.blit(self.base_screen, (0,0))
						
						# Bucle de dibujado de forma ordenada, según "altitud"
						for iTEM in (0,1,5,2,4,3):
							oPOS = (self._photo[iTEM+1][1][0],self._photo[iTEM+1][1][1])
							nPOS = (self._photo[iTEM][1][0],self._photo[iTEM][1][1])
							oPOS = (oPOS[0]+self.plMENU.CFG["snap_position"][0],oPOS[1]+self.plMENU.CFG["snap_position"][1])
							nPOS = (nPOS[0]+self.plMENU.CFG["snap_position"][0],nPOS[1]+self.plMENU.CFG["snap_position"][1])
							oSIZ = (self._photo[iTEM+1][1][2],self._photo[iTEM+1][1][3])
							nSIZ = (self._photo[iTEM][1][2],self._photo[iTEM][1][3])
							try:	self._photo[iTEM][0].draw(self.plMENU.main_screen,oPOS,nPOS,oSIZ,nSIZ,txtANIM)
							except: print("ERR. ITEM:",iTEM)

						self.plMENU.main_screen.blit(self.txtSURFACE, (0,-txtDESP))
						pygame.display.flip()
						
						self.plMENU.frames += 1
						self.plMENU.menu_clock.tick(self.plMENU.CFG["video_fps"])
			else:
				# Las imágenes
				if self.show_image:
					for iTEM in (1,5,2,4,3):
						nPOS = (self._photo[iTEM][1][0],self._photo[iTEM][1][1])
						nPOS = (nPOS[0]+self.plMENU.CFG["snap_position"][0],nPOS[1]+self.plMENU.CFG["snap_position"][1])
						nSIZ = (self._photo[iTEM][1][2],self._photo[iTEM][1][3])
						self._photo[iTEM][0].draw(self.plMENU.main_screen,nPOS,nSIZ)

				# Los textos
				if self.show_list:	self.plMENU.main_screen.blit(self.txtSURFACE,(0,0))

		elif (self.plMENU.CFG["menu_style"] == 2):	# MODO DASHBOARD

			if self.anim_list or self.anim_image:
				# Comienzo una animación de scroll (que puede variar de dirección)
				txtANIM = clockANIM(self.aTIME,self.vSEP,0)
				if (self.plMENU.eventpress == "next_item"):
					while not txtANIM.end():
						txtDESP =round(txtANIM.val())
						self.plMENU.main_screen.blit(self.base_screen, (0,0))
						
						# Bucle de dibujado de forma ordenada, según "altitud"
						for iTEM in (1,2,3,4,5):
							oPOS = (self._photo[iTEM-1][1][0],self._photo[iTEM-1][1][1])
							nPOS = (self._photo[iTEM][1][0],self._photo[iTEM][1][1])
							oPOS = (oPOS[0]+self.plMENU.CFG["snap_position"][0],oPOS[1]+self.plMENU.CFG["snap_position"][1])
							nPOS = (nPOS[0]+self.plMENU.CFG["snap_position"][0],nPOS[1]+self.plMENU.CFG["snap_position"][1])
							oSIZ = (self._photo[iTEM-1][1][2],self._photo[iTEM-1][1][3])
							nSIZ = (self._photo[iTEM][1][2],self._photo[iTEM][1][3])
							self._photo[iTEM][0].draw(self.plMENU.main_screen,oPOS,nPOS,oSIZ,nSIZ,txtANIM)

						self.plMENU.main_screen.blit(self.txtSURFACE, (0,txtDESP))
						pygame.display.flip()
						
						self.plMENU.frames += 1
						self.plMENU.menu_clock.tick(self.plMENU.CFG["video_fps"])
				else:
					while not txtANIM.end() :
						txtDESP = round(txtANIM.val())
						self.plMENU.main_screen.blit(self.base_screen, (0,0))
						
						# Bucle de dibujado de forma ordenada, según "altitud"
						for iTEM in (0,1,2,3,4):
							oPOS = (self._photo[iTEM+1][1][0],self._photo[iTEM+1][1][1])
							nPOS = (self._photo[iTEM][1][0],self._photo[iTEM][1][1])
							oPOS = (oPOS[0]+self.plMENU.CFG["snap_position"][0],oPOS[1]+self.plMENU.CFG["snap_position"][1])
							nPOS = (nPOS[0]+self.plMENU.CFG["snap_position"][0],nPOS[1]+self.plMENU.CFG["snap_position"][1])
							oSIZ = (self._photo[iTEM+1][1][2],self._photo[iTEM+1][1][3])
							nSIZ = (self._photo[iTEM][1][2],self._photo[iTEM][1][3])
							self._photo[iTEM][0].draw(self.plMENU.main_screen,oPOS,nPOS,oSIZ,nSIZ,txtANIM)

						self.plMENU.main_screen.blit(self.txtSURFACE, (0,-txtDESP))
						pygame.display.flip()
						
						self.plMENU.frames += 1
						self.plMENU.menu_clock.tick(self.plMENU.CFG["video_fps"])
			else:
				# Las imágenes
				if self.show_image:
					for iTEM in (1,5,2,4,3):
						try:
							nPOS = (self._photo[iTEM][1][0],self._photo[iTEM][1][1])
							nPOS = (nPOS[0]+self.plMENU.CFG["snap_position"][0],nPOS[1]+self.plMENU.CFG["snap_position"][1])
							nSIZ = (self._photo[iTEM][1][2],self._photo[iTEM][1][3])
							self._photo[iTEM][0].draw(self.plMENU.main_screen,nPOS,nSIZ)
						except:
							nPOS = (self._photo[iTEM][1][0],self._photo[iTEM][1][1])
							
						

				# Los textos
				if self.show_list:	self.plMENU.main_screen.blit(self.txtSURFACE,(0,0))
	
	
	# Modo clásico (el más parecido a GLAUNCH)
	def glaunch_style(self):
		
		# Guardo la ultima foto
		try:		self.lastPHOTO = self.photoMAIN
		except:	self.lastPHOTO = None
		
		# Creo la nueva foto (RUTA,TIPO ZOOM, REFLEJO?, SCALE2X?)
		
		if self.show_image: self.photoMAIN = itemPHOTO(self.plMENU.LIST.getitem(0,2),self.plMENU.CFG["snap_zoom"],self.plMENU.CFG["snap_shadow"],self.plMENU.CFG["snap_scale2x"],self._xsize)

		# Si la pulsación de tecla no es contínua... review
		#if (self.inloop <= 1) or self.after_loop:
		# Dibujo sobre el fondo todos los elementos NO animables
		self.title_and_stats()
	
		# Dibujo la lista de elementos si corresponde
		self.item_list()
		
		# Dibujo las imágenes
		self.draw_scene()

	# Modo centrado
	def centered_style(self):		

		# Dibujo sobre el fondo todos los elementos NO animables
		self.title_and_stats()
		
		# Dibujo sobre el fondo todos los elementos SI animables
		self.item_list()

		# Una vez pintados esos textos, me copio la imagen de base
		self.base_screen = self.plMENU.main_screen.copy()

		# Dibujo las imágenes
		self.draw_scene()
		
		# Precargo las fotos que necesito
		if  (self.anim_list or self.anim_image) and (self.plMENU.eventpress == "prev_item"):
			self._photo[0][0] = self._photo[1][0]
			self._photo[1][0] = self._photo[2][0]
			self._photo[2][0] = self._photo[3][0]
			self._photo[3][0] = self._photo[4][0]
			self._photo[4][0] = self._photo[5][0]
			self._photo[5][0] = itemPHOTO(self.plMENU.LIST.getitem(-2,2),self.plMENU.CFG["snap_zoom"],self.plMENU.CFG["snap_shadow"],self.plMENU.CFG["snap_scale2x"],noCACHE=True)
			self._photo[6][0] = None
			
		elif (self.anim_list or self.anim_image) and (self.plMENU.eventpress == "next_item"):
			self._photo[6][0] = self._photo[5][0]
			self._photo[5][0] = self._photo[4][0]
			self._photo[4][0] = self._photo[3][0]
			self._photo[3][0] = self._photo[2][0]
			self._photo[2][0] = self._photo[1][0]
			self._photo[0][0] = None
			self._photo[1][0] = itemPHOTO(self.plMENU.LIST.getitem(2,2),self.plMENU.CFG["snap_zoom"],self.plMENU.CFG["snap_shadow"],self.plMENU.CFG["snap_scale2x"],noCACHE=True)

		else:
			self._photo[0][0] = None
			self._photo[1][0] = itemPHOTO(self.plMENU.LIST.getitem(2,2),self.plMENU.CFG["snap_zoom"],self.plMENU.CFG["snap_shadow"],self.plMENU.CFG["snap_scale2x"],noCACHE=True)
			self._photo[2][0] = itemPHOTO(self.plMENU.LIST.getitem(1,2),self.plMENU.CFG["snap_zoom"],self.plMENU.CFG["snap_shadow"],self.plMENU.CFG["snap_scale2x"],noCACHE=True)
			self._photo[3][0] = itemPHOTO(self.plMENU.LIST.getitem(0,2),self.plMENU.CFG["snap_zoom"],self.plMENU.CFG["snap_shadow"],self.plMENU.CFG["snap_scale2x"],noCACHE=True)
			self._photo[4][0] = itemPHOTO(self.plMENU.LIST.getitem(-1,2),self.plMENU.CFG["snap_zoom"],self.plMENU.CFG["snap_shadow"],self.plMENU.CFG["snap_scale2x"],noCACHE=True)
			self._photo[5][0] = itemPHOTO(self.plMENU.LIST.getitem(-2,2),self.plMENU.CFG["snap_zoom"],self.plMENU.CFG["snap_shadow"],self.plMENU.CFG["snap_scale2x"],noCACHE=True)
			self._photo[6][0] = None
		
	def dashboard_style(self):

		# Dibujo sobre el fondo todos los elementos NO animables
		self.title_and_stats()
		
		# Dibujo sobre el fondo todos los elementos SI animables
		self.item_list()

		# Una vez pintados esos textos, me copio la imagen de base
		self.base_screen = self.plMENU.main_screen.copy()

		# Dibujo las imágenes
		self.draw_scene()
		
		# Precargo las fotos que necesito
		if (self.anim_list or self.anim_image) and (self.plMENU.eventpress == "prev_item"):
			self._photo[0][0] = self._photo[1][0]
			self._photo[1][0] = self._photo[2][0]
			self._photo[2][0] = self._photo[3][0]
			self._photo[3][0] = self._photo[4][0]
			self._photo[4][0] = itemPHOTO(self.plMENU.LIST.getitem(0,2),self.plMENU.CFG["snap_zoom"],self.plMENU.CFG["snap_shadow"],self.plMENU.CFG["snap_scale2x"],noCACHE=True)
			self._photo[5][0] = None
			
		elif (self.anim_list or self.anim_image) and (self.plMENU.eventpress == "next_item"):
			self._photo[5][0] = self._photo[4][0]
			self._photo[4][0] = self._photo[3][0]
			self._photo[3][0] = self._photo[2][0]
			self._photo[2][0] = self._photo[1][0]
			self._photo[1][0] = itemPHOTO(self.plMENU.LIST.getitem(+3,2),self.plMENU.CFG["snap_zoom"],self.plMENU.CFG["snap_shadow"],self.plMENU.CFG["snap_scale2x"],noCACHE=True)
			self._photo[0][0] = None

		else:
			self._photo[0][0] = None
			self._photo[1][0] = itemPHOTO(self.plMENU.LIST.getitem(3,2),self.plMENU.CFG["snap_zoom"],self.plMENU.CFG["snap_shadow"],self.plMENU.CFG["snap_scale2x"],noCACHE=True)
			self._photo[2][0] = itemPHOTO(self.plMENU.LIST.getitem(2,2),self.plMENU.CFG["snap_zoom"],self.plMENU.CFG["snap_shadow"],self.plMENU.CFG["snap_scale2x"],noCACHE=True)
			self._photo[3][0] = itemPHOTO(self.plMENU.LIST.getitem(1,2),self.plMENU.CFG["snap_zoom"],self.plMENU.CFG["snap_shadow"],self.plMENU.CFG["snap_scale2x"],noCACHE=True)
			self._photo[4][0] = itemPHOTO(self.plMENU.LIST.getitem(0,2),self.plMENU.CFG["snap_zoom"],self.plMENU.CFG["snap_shadow"],self.plMENU.CFG["snap_scale2x"],noCACHE=True)
			self._photo[5][0] = None
		
	def refresh(self):
		# Actualiza la información en pantalla

		# Si hay cambio de lista, hay cambio de background
		if self.list_change:
			self.key_animation = False
			self.old_screen = self.plMENU.main_screen.copy()
			if "list_wallpaper" in self.plMENU.LIST.LST[self.last_list]:
				if (len(self.plMENU.LIST.LST[self.last_list]["list_wallpaper"]) == 0):
					self.plMENU.wallpaper =  sizeIMG(plvideo.loadIMG(self.plMENU.CFG["menu_wallpaper"]),self.plMENU.CFG["screen_resolution"])
				else:
					self.plMENU.wallpaper =  sizeIMG(plvideo.loadIMG(self.plMENU.LIST.LST[self.last_list]["list_wallpaper"]),self.plMENU.CFG["screen_resolution"])
			else:
				plfiles._LOG("ERR.error in list (check configuration) " + self.last_list)
			self.plMENU.main_screen.blit(self.plMENU.wallpaper, (0,0))
		else:
			self.plMENU.main_screen.blit(self.plMENU.wallpaper, (0,0))
			
		# La pantalla siempre llega a este punto "limpia" solamente con la imágen de fondo...

		if (self.plMENU.CFG["menu_style"] == 0):
			# Modo clásico (el más parecido al verdadero GLAUNCH)
			self.glaunch_style()

		elif (self.plMENU.CFG["menu_style"] == 1):
			# Modo "centrado"
			self.centered_style()

		elif (self.plMENU.CFG["menu_style"] == 2):
			# Modo "dashboard"
			self.dashboard_style()
		else:
			plfiles._LOG("ERR. menu_style = "+self.plMENU.CFG["menu_style"]+" unknown")


		# Animación del cambio de lista
		if self.list_change and (self.inloop < self.maxLOOP) and self.anim_wall:
			
			self.new_screen = self.plMENU.main_screen.copy()
			
			# Comienzo una animación de scroll (que puede variar de dirección)
			aVEL =  (self.aTIME*1.5) - ((self.aTIME / self.maxLOOP) * self.inloop)
			clkANIM = clockANIM(aVEL,self.screenWIDTH,0,-1)
			
			while not clkANIM.end():
				x_desp = int(clkANIM.val())
				if (self.plMENU.eventpress == "next_list"):
					self.plMENU.main_screen.blit(self.old_screen, (x_desp-self.screenWIDTH,0))
					self.plMENU.main_screen.blit(self.new_screen, (x_desp,0))
				else:
					self.plMENU.main_screen.blit(self.old_screen, (self.screenWIDTH-x_desp,0))
					self.plMENU.main_screen.blit(self.new_screen, (-x_desp,0))
				pygame.display.flip()
				
				self.plMENU.frames += 1
				self.plMENU.menu_clock.tick(self.plMENU.CFG["video_fps"])
		else:
			pygame.display.flip()





# Lanza la animación de salida
def shutdownEFFECT(plMENU):
	# Velocidad de la animación
	aSPEED = plMENU.CFG["menu_speed"]
	
	# Creo una copia de la pantalla en negro y otra en blanco
	scrCOPY = plMENU.main_screen.copy()
	scrBLACK = plMENU.main_screen.copy()
	scrBLACK.fill((0,0,0))
	scrWHITE = plMENU.main_screen.copy().convert()
	scrWHITE.fill((255,255,255))
	
	# Comienzo la animación
	
	# El efecto de sonido correspondiente
	plMENU.SAMPLER.play(plMENU.eventpress)
	
	# Contracción VERTICAL de la imágen (y fundido parcial a blanco)
	nSIZ = int(plMENU.main_screen.get_height() / 50)
	# downANIM Controla el tamaño vertical de la imágen (de momento)
	# whiteANIM Controla la transparencia de la imágen
	downANIM = clockANIM(aSPEED,plMENU.main_screen.get_height(),nSIZ,10)
	whiteANIM = clockANIM(aSPEED,0,100)
	while not downANIM.end() or not whiteANIM.end():
		nSIZ = round(downANIM.val())
		# Establezco el nuevo valor de transparencia para el blanco
		scrWHITE.set_alpha(whiteANIM.val(),pygame.RLEACCEL)
		
		# Redimensiono la imagen de copia y la aclaro progresivamente
		scrCOPYW = sizeIMG(scrCOPY,size=(scrCOPY.get_width(),nSIZ),type=0)
		scrCOPYW.blit(scrWHITE,scrCOPYW.get_rect())
		
		# Compongo la imagen a mostrar, centrando el resultado
		plMENU.main_screen.blit(scrBLACK,(0,0))
		tmpRECT = scrCOPYW.get_rect()
		tmpRECT.centerx = plMENU.main_screen.get_rect().centerx
		tmpRECT.centery = plMENU.main_screen.get_rect().centery
		plMENU.main_screen.blit(scrCOPYW,tmpRECT)
		
		# Actualizo la pantalla
		pygame.display.flip()
		plMENU.frames += 1
		plMENU.menu_clock.tick(plMENU.CFG["video_fps"])

	# Contracción  VERTICAL de la imágen (y fundido final a blanco)
	#nSIZ = int(plMENU.main_screen.get_width() / 100)
	scrCOPY = scrCOPYW.copy()
	# downANIM Controla el tamaño horizontal de la imágen (de momento)
	# whiteANIM Controla la transparencia de la imágen
	downANIM = clockANIM(aSPEED,plMENU.main_screen.get_width(),nSIZ,10)
	whiteANIM = clockANIM(aSPEED,0,255)

	while not downANIM.end() or not whiteANIM.end():
		nSIZ = round(downANIM.val())

		# Establezco el nuevo valor de transparencia para el blanco
		scrWHITE.set_alpha(whiteANIM.val(),pygame.RLEACCEL)

		# Redimensiono la imagen de copia y la aclaro progresivamente
		scrCOPYW = sizeIMG(scrCOPY,size=(nSIZ,scrCOPY.get_height()),type=0)
		scrCOPYW.blit(scrWHITE,scrCOPYW.get_rect())
		
		# Compongo la imagen a mostrar, centrando el resultado
		plMENU.main_screen.blit(scrBLACK,scrCOPYW.get_rect())
		tmpRECT = scrCOPYW.get_rect()
		tmpRECT.centerx = plMENU.main_screen.get_rect().centerx
		tmpRECT.centery = plMENU.main_screen.get_rect().centery
		plMENU.main_screen.blit(scrCOPYW,tmpRECT)
		
		# Actualizo la pantalla
		pygame.display.flip()
		plMENU.frames += 1
		plMENU.menu_clock.tick(plMENU.CFG["video_fps"])

	# Fundido final a negro
	scrCOPY = scrCOPYW.copy()
	scrBLACK = scrCOPYW.copy().convert()
	scrBLACK.fill((0,0,0))
	whiteANIM = clockANIM(aSPEED,0,300,2)
	while not whiteANIM.end():
		nSIZ = round(whiteANIM.val())

		scrBLACK.set_alpha(whiteANIM.val(),pygame.RLEACCEL)
		scrCOPYW = scrCOPY.copy()
		scrCOPYW.blit(scrBLACK,(0,0))
		
		# Compongo la imagen a mostrar, centrando el resultado
		tmpRECT = scrCOPYW.get_rect()
		tmpRECT.centerx = plMENU.main_screen.get_rect().centerx
		tmpRECT.centery = plMENU.main_screen.get_rect().centery
		plMENU.main_screen.blit(scrCOPYW,tmpRECT)
		
		# Actualizo la pantalla
		pygame.display.flip()
		plMENU.frames += 1
		plMENU.menu_clock.tick(plMENU.CFG["video_fps"])
