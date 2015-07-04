# -*- coding: iso-8859-15 -*-

# La librería configparser cambió de nombre en la versión 3.0 de Python
import os,plfiles,pdb,pygame
try:		import configparser
except:	import ConfigParser
	


# La finalidad de este módulo es gestionar las configuraciones almacenadas en ficheros .CFG/.INI
	

# Esta clase es la encargada de interactuar a nivel básico con los ficheros de texto de configuración (.cfg/.ini)
class iniCFG:
	"""Objeto encargado de gestionar las configuraciones de un fichreo .CFG/.INI
	Devuelve: un objeto del tipo iniCFG
	Funciones: read, write, getcfg, setcfg
	Atributos: path,section,cfg"""

	def __init__(self, cfgFILE,defSECT="DEFAULT"):
		"""incialización de del objeto"""
		self.path = cfgFILE						# Ruta del fichero .CFG (para buscar en la ruta actual os.getcwd()+"\\CFG.INI")
		self.section = defSECT						# Sección de configuración que se utilizará en cada momento
		try: 		self.cfg = configparser.ConfigParser()	# Objeto que gestionará la comunicación con el fichero .CFG
		except:	self.cfg = ConfigParser.ConfigParser()	# Objeto que gestionará la comunicación con el fichero .CFG
		if len(cfgFILE) > 0: self.read()
		
	def read(self):
		""" Carga los valores del fichero hacia el diccionario en memoria"""
		# Carga del fichero .CFG a memoria
		try: 
			self.cfg.read(self.path)
			plfiles._LOG("OK."+self.section+" > "+self.path+" loaded")
			OK = True
		except: 
			OK = False
			plfiles._LOG("ERR."+self.section+" > "+self.path+" NOT loaded")
		return OK
	
	def write(self):
		""" Escribe en el fichero los valores encontrados en el diccionario en memoria"""
		try:
			tmpFILE = open(self.path, 'wb')
			self.cfg.write(tmpFILE)
			OK = True
			plfiles._LOG("OK."+self.section+" > "+self.path+" saved")
		except: 
			OK = False
			plfiles._LOG("ERR."+self.section+" > "+self.path+" write error")
			
		return OK
		
	def setcfg(self,cfgNOM,cfgVAL):
		"""Establece el valor de una opción de configuración en memoria, a través de su nombre
		utilizando la sección .section"""

		# Compruebo que exista la sección (si no existe la creo)
		if not self.cfg.has_section(self.section):
			self.cfg.add_section(self.section)
			plfiles._LOG("OK."+self.section+" created")
			
		# Establezco/actualizo el valor de la nueva sección
		self.cfg.set(self.section,cfgNOM,cfgVAL)
		
		return cfgVAL
		
	def getcfg(self,cfgNOM,cfgDEF=None):
		"""Recupera el valor de una opción de configuración en memoria, a través de su nombre
		utilizando la sección .section"""
		
		cfgVAL = cfgDEF
		
		# Compruebo que exista la sección
		if self.cfg.has_section(self.section):
			if self.cfg.has_option(self.section,cfgNOM):
				try:
					# Si se especifica un valor por defecto el tipo del valor recuperado será el mismo que el tipo del valor por defecto
					if (type(cfgVAL) == type(None)): cfgVAL = self.cfg.get(self.section,cfgNOM)
					elif (type(cfgVAL) == type("X")): cfgVAL = str(self.cfg.get(self.section,cfgNOM))
					elif (type(cfgVAL) == type(1)): cfgVAL = int(self.cfg.get(self.section,cfgNOM))
					elif (type(cfgVAL) == type(0.5)): cfgVAL = float(self.cfg.get(self.section,cfgNOM))
					elif (type(cfgVAL) == type(True)): cfgVAL = eval(self.cfg.get(self.section,cfgNOM))
					elif (type(cfgVAL) == type((1,2))): 
						cfgVAL = self.cfg.get(self.section,cfgNOM)
						if (cfgVAL.find(" ") == -1): cfgVAL = (eval(cfgVAL),"")
						else:	 cfgVAL = eval("("+cfgVAL.replace(" ",",")+")")
							
					elif (type(cfgVAL) == type([1,2])): 
						cfgVAL = self.cfg.get(self.section,cfgNOM)
						if (cfgVAL.find(" ") == -1): cfgVAL = [eval(cfgVAL),""]
						else:	cfgVAL = eval("["+cfgVAL.replace(" ",",")+"]")
							
				except:
					cfgVAL = None
						
		return cfgVAL


# Esta clase "MOSTRUO" es la encargada de gestionar TODO, las listas y sus elementos
# La LISTA puede estar copuesta por una o varias sublistas que a su vez  pueden contener uno o varios elementos (en diccionarios)
# Estructura:
# .LST{"nombrelista",elementoslista,"nombrelista",elementoslista}
# .elementoslista{"cfg_xxx","valor"}	<- todos los valores del fichero cfg\lista.cfg
# .elementoslista{"ITEMS",(item1,tiem2,itemX)}
# .elementoslista{"IMAGES",imageneslista}
# .imageneslista{"itemA","x:\image.pic","itemB","x:\image2.pic"}
# .elementoslista{"NAMES",nombreslista}
# .nombreslista{"itemA","name item A","itemB","name item B"}
class theLIST:

	def __init__(self, cfgLST = ("MAME",), cfgFILE = "",plMENU="" ):
		"""incialización de del objeto"""

		self.cfgFILE = cfgFILE				# Fichero que almacena el estado del menu y el nº de ejecuciones de cada juego
		
		self.CFG = iniCFG("","CFG")			# Objeto que se utilizará para la manipulación de los ficheros de configuración
		self.cfgFAV = iniCFG(plMENU.state_config_file,"__MOST")
		self.favSIZE = plMENU.CFG["fav_list_size"]
		
		self.LST = {}					# Diccionario que lo contendrá TODO (y cuando digo, todo quiero decir "todo")
		self.lstCACHE = ("","")			# Lista de LISTAS ordenadas alfabéticamente
		self.actual_list_index = 0			# Índice de la lista activa
		self.fav_item_name = plMENU.CFG["fav_item_name"] 
		
		self.globalCOUNT = 0				# Recuento total de ITEMS

		# Cominezo la carga e inicialización de todos los elementos de todas las listas

		# CREO LA LISTA DE FAVORITOS
		self.LST["__MOST"] = {}
		self.LST["__MOST"]["list_name"] = "MOST PLAYED"
		self.LST["__MOST"]["list_item_dir"] = ""
		self.LST["__MOST"]["list_wallpaper"] = ""
		self.LST["__MOST"]["list_image_def"] = ""
		self.LST["__MOST"]["list_image_dir"] = ""
		self.LST["__MOST"]["list_launcher_file"] = ""
		self.LST["__MOST"]["list_launcher_options"] = ""
		self.LST["__MOST"]["list_name_file"] = ""
		self.LST["__MOST"]["list_item_extension"] = ""
		self.LST["__MOST"]["list_image_extension"] = ""
		self.LST["__MOST"]["_ITEMS_"] = {}			# Diccionario de elementos/nombres
		self.LST["__MOST"]["_IMAGES_"] = {}			# Diccionario de elementos/imágenes
		self.LST["__MOST"]["_PLAYED_"] = {}			# Identificador de la lista a la que pertenece cada juego
		self.LST["__MOST"]["_CACHE_"] = ("","")		# Lista de elementos indexados y ordenados por ID 
		self.LST["__MOST"]["_ACTUAL_ITEM_INDEX"] = 0	# ID del elemento seleccionado actualmente
		self.LST["__MOST"]["_ACTUAL_ITEM_NAME"] = ""	# Nombre del elemento seleccionado actualmente

		# CREO LA LISTA TOTAL DE ELEMENTOS
		self.LST["__ALL"] = {}
		self.LST["__ALL"]["list_name"] = "ALL ITEMS"
		self.LST["__ALL"]["list_item_dir"] = ""
		self.LST["__ALL"]["list_wallpaper"] = ""
		self.LST["__ALL"]["list_image_def"] = ""
		self.LST["__ALL"]["list_image_dir"] = ""
		self.LST["__ALL"]["list_launcher_file"] = ""
		self.LST["__ALL"]["list_launcher_options"] = ""
		self.LST["__ALL"]["list_name_file"] = ""
		self.LST["__ALL"]["list_item_extension"] = ""
		self.LST["__ALL"]["list_image_extension"] = ""
		self.LST["__ALL"]["_ITEMS_"] = {}			# Diccionario de elementos/nombres
		self.LST["__ALL"]["_IMAGES_"] = {}			# Diccionario de elementos/imágenes
		self.LST["__ALL"]["_PLAYED_"] = {}			# Identificador de la lista a la que pertenece cada juego
		self.LST["__ALL"]["_CACHE_"] = ("","")			# Lista de elementos indexados y ordenados por ID 
		self.LST["__ALL"]["_ACTUAL_ITEM_INDEX"] = 0	# ID del elemento seleccionado actualmente
		self.LST["__ALL"]["_ACTUAL_ITEM_NAME"] = ""	# Nombre del elemento seleccionado actualmente

		# CREO LA LISTA DE ELEMENTOS FILTRADOS
		self.LST["__FOUND"] = {}
		self.LST["__FOUND"]["list_name"] = "FOUND ITEMS"
		self.LST["__FOUND"]["list_item_dir"] = ""
		self.LST["__FOUND"]["list_wallpaper"] = ""
		self.LST["__FOUND"]["list_image_def"] = ""
		self.LST["__FOUND"]["list_image_dir"] = ""
		self.LST["__FOUND"]["list_launcher_file"] = ""
		self.LST["__FOUND"]["list_launcher_options"] = ""
		self.LST["__FOUND"]["list_name_file"] = ""
		self.LST["__FOUND"]["list_item_extension"] = ""
		self.LST["__FOUND"]["list_image_extension"] = ""
		self.LST["__FOUND"]["_ITEMS_"] = {}			# Diccionario de elementos/nombres
		self.LST["__FOUND"]["_IMAGES_"] = {}			# Diccionario de elementos/imágenes
		self.LST["__FOUND"]["_PLAYED_"] = {}			# Identificador de la lista a la que pertenece cada juego
		self.LST["__FOUND"]["_CACHE_"] = ("","")		# Lista de elementos indexados y ordenados por ID 
		self.LST["__FOUND"]["_ACTUAL_ITEM_INDEX"] = 0	# ID del elemento seleccionado actualmente
		self.LST["__FOUND"]["_ACTUAL_ITEM_NAME"] = ""	# Nombre del elemento seleccionado actualmente

		bck_screen = plMENU.main_screen.copy()
		# Cargo la LISTA de LISTAS (los nombres de esta lisa deben corresponderse con ficheros .CFG existentes o no serán tenidos en cuenta) 
		for lstID in cfgLST:
			
			plMENU.main_screen.blit(bck_screen,(0,0))
			plMENU.vTXT.msg(plMENU.main_screen,lstID,(-1,plMENU.vTXT.get_dim()[1]*4),plMENU.CFG["font1_color"])
			pygame.display.flip()

			lstCFG = "cfg\\"+lstID.lower()+".cfg"
			if os.path.exists(lstCFG) and os.path.isfile(lstCFG):
				self.CFG.path = lstCFG
				if self.CFG.read():
					if plMENU.CFG["debug_mode"]:
						plfiles._LOG("")
						plfiles._LOG("DBUG.list item CFG "+lstID)
					
					# Si todo ha ido bien intento recuperar todos los valores que necesito
					# Los que su valor por defecto es * son obligatorios
					OK = True
					self.LST[lstID] = {}
					list_item_dir = self.CFG.getcfg("list_item_dir","*")				# (OBLIGATORIO) El directorio de ELEMENTOS para la lista
					# Solo cargo el resto de los elementos, si los obligatorios son correctos
					if (list_item_dir != "*") and os.path.exists(list_item_dir):
						list_name = self.CFG.getcfg("list_name",lstID)							# Si no se ha indicado nombre, se utilizará el identificador de la lista
						list_wallpaper = self.CFG.getcfg("list_wallpaper","")						# Si no se ha indicado wallpaper, se utilizará el del menu principal (menu_wallpaper)
						list_image_def = self.CFG.getcfg("list_image_def","")						# Si no se indica imagen por defecto se mostrará del menú principal (menu_picture)
						list_image_dir = self.CFG.getcfg("list_image_dir","")						# Directorio de IMÁGENES para la lista
						list_launcher_file = self.CFG.getcfg("list_launcher_file","")					# Programa lanzador de los elementos (si lo hay)
						list_launcher_options = self.CFG.getcfg("list_launcher_options","")			# Opciones para el programa lanzador (si las hay)
						list_name_file = self.CFG.getcfg("list_name_file","")						# Fichero de nombres para los elementos (si lo hay)
						list_item_extension = self.CFG.getcfg("list_item_extension",(".zip",".rom"))		# Extensión de los elementos
						list_image_extension = self.CFG.getcfg("list_image_extension",(".png",".jpg"))	# Extensión de las imágenes
					else:
						OK = False
						plfiles._LOG("ERR. list_item_dir ["+lstID+"] error")
						
					if OK:
						self.LST[lstID]["list_name"] = list_name
						self.LST[lstID]["list_item_dir"] = list_item_dir
						self.LST[lstID]["list_wallpaper"] = list_wallpaper
						self.LST[lstID]["list_image_def"] = list_image_def
						self.LST[lstID]["list_image_dir"] = list_image_dir
						self.LST[lstID]["list_launcher_file"] = list_launcher_file
						self.LST[lstID]["list_launcher_options"] = list_launcher_options
						self.LST[lstID]["list_name_file"] = list_name_file
						self.LST[lstID]["list_item_extension"] = list_item_extension
						self.LST[lstID]["list_image_extension"] = list_image_extension
						self.LST[lstID]["_ITEMS_"] = {}			# Diccionario de elementos/nombres
						self.LST[lstID]["_IMAGES_"] = {}			# Diccionario de elementos/imágenes
						self.LST[lstID]["_CACHE_"] = ("","")		# Lista de elementos indexados y ordenados por ID 
						self.LST[lstID]["_ACTUAL_ITEM_INDEX"] = 0	# ID del elemento seleccionado actualmente
						self.LST[lstID]["_ACTUAL_ITEM_NAME"] = ""	# Nombre del elemento seleccionado actualmente
						
					# Cargo los ID de elementos, junto con sus nombres (que por defecto tb es su ID)
					# No almaceno el path porque esos datos los tengo en (list_item_dir)
					# La extensión se le presupone solo una (list_item_extension)
					# Hago lo mismo con las imágenes (list_image_dir y list_image_extension)
					
					if OK:
						# BÚSQUEDA DE ITEMS EN EL DIRECTORIO list_item_dir {elementoID,nombre_completo}
						for f in os.listdir(list_item_dir):
							fne = os.path.splitext(f)	# Separo nombre de extensión
							if fne[1].lower() in list_item_extension:
								# Si hay fichero de nombres .map asociado al sistema utilizo minúsculas
								fileNAME = fne[0]
								if os.path.exists(list_name_file) and os.path.isfile(list_name_file):
									fileNAME = fileNAME.lower()
								
								if plMENU.CFG["debug_mode"]:
									plfiles._LOG("DBUG.item file "+list_item_dir+" -> "+fileNAME)
								
								self.LST[lstID]["_ITEMS_"][fileNAME] = fileNAME				# Identificador de ITEM
								self.LST["__ALL"]["_ITEMS_"][lstID+":"+fileNAME] = fileNAME		# Nombre del item y SIN numero de veces ejecutadas
								self.LST["__FOUND"]["_ITEMS_"][lstID+":"+fileNAME] = fileNAME	# Nombre del item y SIN numero de veces ejecutadas
								
								self.LST["__MOST"]["_PLAYED_"][lstID+":"+fileNAME] = self.cfgFAV.getcfg(lstID+"_"+fileNAME,0)
								self.LST["__ALL"]["_PLAYED_"][lstID+":"+fileNAME] = self.cfgFAV.getcfg(lstID+"_"+fileNAME,0)
								self.LST["__FOUND"]["_PLAYED_"][lstID+":"+fileNAME] = self.cfgFAV.getcfg(lstID+"_"+fileNAME,0)
								
								lcTXT = self.fav_item_name
								lcTXT = lcTXT.replace("*item*",fileNAME)
								lcTXT = lcTXT.replace("*played*",str(self.LST["__MOST"]["_PLAYED_"][lstID+":"+fileNAME]))
								self.LST["__MOST"]["_ITEMS_"][lstID+":"+fileNAME] = lcTXT	# Nombre del item y numero de veces ejecutadas

						# ACOTAR LISTA A LA LISTA INDICADA EN EL FICHERO .LST (si existe)
						list_filter_lst = os.path.splitext(lstCFG)[0] + ".lst"
						if os.path.exists(list_filter_lst) and os.path.isfile(list_filter_lst):
							item_lst = []
							file = open(list_filter_lst)
							# Compongo la lista de elmentos que quiero filtrar
							# (solo se monstrarán estos)
							for line in file:
								itemKEY = line[:line.find(" ")].lower()
								item_lst.append(itemKEY)
							file.close()
							if (len(item_lst) > 0):
								# Cualquier elemento que no exista en la lista de filtrado, es eliminado de _items_ 
								for itemKEY in self.LST[lstID]["_ITEMS_"].keys():
									if not (itemKEY in item_lst):
										if (itemKEY in self.LST[lstID]["_ITEMS_"]): 
											del self.LST[lstID]["_ITEMS_"][itemKEY]
											del self.LST["__MOST"]["_ITEMS_"][lstID+":"+itemKEY]
											del self.LST["__ALL"]["_ITEMS_"][lstID+":"+itemKEY]
											del self.LST["__FOUND"]["_ITEMS_"][lstID+":"+itemKEY]

						# BÚSQUEDA DE IMÁGENES EN EL DIRECTORIO list_image_dir {elementoID,ruta_imágen}
						if os.path.exists(list_image_dir):
							for f in os.listdir(list_image_dir):
								fne = os.path.splitext(f)	# Separo nombre de extensión
								if fne[1].lower() in list_image_extension:
									# Solo añado las imágenes si se corresponden con algún ITEM
									fileNAME = fne[0]
									if os.path.exists(list_name_file) and os.path.isfile(list_name_file):
										fileNAME = fileNAME.lower()
										
									if (fileNAME in self.LST[lstID]["_ITEMS_"]): 
										self.LST[lstID]["_IMAGES_"][fileNAME] = f
										self.LST["__MOST"]["_IMAGES_"][lstID+":"+fileNAME] = f
										self.LST["__ALL"]["_IMAGES_"][lstID+":"+fileNAME] = f
										self.LST["__FOUND"]["_IMAGES_"][lstID+":"+fileNAME] = f
										
									#self.LST[lstID]["_IMAGES_"][fne[0]] = f
						else:
							plfiles._LOG("ERR. list_image_dir ["+list_image_dir+"] not exist?")
						
						# BÚSQUEDA DE NOMBRES EN EL FICHERO list_name_file
						if os.path.exists(list_name_file) and os.path.isfile(list_name_file):
							file = open(list_name_file)
							for line in file:
								# ####################################################################
								# Aqui falta controlar temas de listas peronalizadas, " iniciales/finales y posibles items que no aparezcan en _ITEMS_
								if line.find("=") != -1:
									itemKEY = line[:line.find("=")].lower()
									itemNAME = line[line.find("=")+1:].strip()
								else:
									itemKEY = line[:line.find(" ")].lower()
									itemNAME = line[line.find(" "):].strip()
									
								itemNAME = itemNAME.replace('"',"")
								itemNAME = itemNAME.replace("'","")
								if (itemKEY in self.LST[lstID]["_ITEMS_"]): 
									self.LST[lstID]["_ITEMS_"][itemKEY] = itemNAME
									self.LST["__ALL"]["_ITEMS_"][lstID+":"+itemKEY] = itemNAME
									self.LST["__FOUND"]["_ITEMS_"][lstID+":"+itemKEY] = itemNAME
									
									lcTXT = self.fav_item_name
									lcTXT = lcTXT.replace("*item*",itemNAME)
									lcTXT = lcTXT.replace("*played*",str(self.LST["__MOST"]["_PLAYED_"][lstID+":"+itemKEY]))
									self.LST["__MOST"]["_ITEMS_"][lstID+":"+itemKEY] = lcTXT	# Nombre del item y numero de veces ejecutadas

									if len(itemKEY) > 0 and plMENU.CFG["debug_mode"]:
											plfiles._LOG("DBUG."+itemKEY+" -> "+itemNAME)
								else:
									if len(itemKEY) > 0 and plMENU.CFG["debug_mode"]:
											plfiles._LOG("ERR."+itemKEY+" not found in list "+lstID)
										
								# ####################################################################
							file.close()

						self.lstSORT(lstID,plMENU)
						
						# Finalmente en modo dbug reordeno la lista
							

				else:
					plfiles._LOG("ERR. LIST CFG ["+lstCFG+"] not valid")
			else:
				plfiles._LOG("ERR. LIST CFG ["+lstCFG+"] not exist?")

		plMENU.main_screen.blit(bck_screen,(0,0))
		plMENU.vTXT.msg(plMENU.main_screen,"indexing items...",(-1,plMENU.vTXT.get_dim()[1]*4),plMENU.CFG["font1_color"])
		pygame.display.flip()

		self.lstSORT("__MOST",plMENU)
		self.lstSORT("__ALL",plMENU)
		
		# Al terminar indexo todas las listas por ID
		# Esta cache la utilizaré después para recorrer las listas de forma ordenada
		self.lstCACHE = sorted(self.LST.keys())

		self.actual_list_name = self.lstCACHE[self.actual_list_index]		# Nombre de la lista activa
		
		if (len(self.cfgFILE) > 0): self.read()

	def lstSORT(self,lstID,plMENU=""):
		# En cualquier caso al terminar indexo todos los elementos por NOMBRE (EJECUCIONES+NOMBRE PARA MOST PLAYED)
		# Esta cache la utilizaré para recorrer despues los elementos de forma ordenada
		# La forma de ordenar cambia sustancialmente para la lista "__MOST"
		self.LST[lstID]["_CACHE_"] = list(self.LST[lstID]["_ITEMS_"].keys())
		idorder = 0

		for idname in self.LST[lstID]["_CACHE_"]: 
			if (lstID != "__MOST"):
				keyORDER = self.LST[lstID]["_ITEMS_"][self.LST[lstID]["_CACHE_"][idorder]] + chr(9) + self.LST[lstID]["_CACHE_"][idorder]
			else:
				keyORDER = str(9999999999-self.LST[lstID]["_PLAYED_"][self.LST[lstID]["_CACHE_"][idorder]]) + chr(9) + self.LST[lstID]["_CACHE_"][idorder]
				
				
			self.LST[lstID]["_CACHE_"][idorder] = keyORDER
			idorder += 1
			
		self.LST[lstID]["_CACHE_"].sort()
		
		#En el caso de la lista "__MOST" Me quedo con los primeros XX elementos
		if (lstID == "__MOST"): del self.LST[lstID]["_CACHE_"][self.favSIZE:]

		if not (lstID in ["__MOST","__FOUND","__ALL"]): self.globalCOUNT += len(self.LST[lstID]["_CACHE_"])

		idorder = 0
		for idname in self.LST[lstID]["_CACHE_"]: 
			keyORDER = self.LST[lstID]["_CACHE_"][idorder].split(chr(9))[1]
			self.LST[lstID]["_CACHE_"][idorder] = keyORDER
			idorder += 1
		try:
			self.LST[lstID]["_ACTUAL_ITEM_NAME"] = self.LST[lstID]["_CACHE_"][self.LST[lstID]["_ACTUAL_ITEM_INDEX"]]
		except:
			self.LST[lstID]["_ACTUAL_ITEM_NAME"] = "NOT_FOUND:"+lstID
			
		if (lstID != "__ALL") & (lstID != "__MOST") & (lstID != "__FOUND") & (lstID != "_CACHE_"):
			if plMENU.CFG["debug_mode"]:
				for idname in sorted(self.LST[lstID]["_ITEMS_"].items()):
					# Nombre de la lista
					lstNAME = self.LST[lstID]["list_name"] 
					# Nombre del item/juego
					itemNAME = idname[1]
					# Vuelco a disco
					plfiles._writeTXT(lstNAME+"  ->  "+itemNAME,"FULL_LIST.LOG")
					
			


	def read(self):
		"""Lee la configuración las posiciones de todas las listas y la lista activa"""
		if (len(self.cfgFILE) > 0):
			cfgOBJ = iniCFG(self.cfgFILE,"MENU")
			actual_list_id = cfgOBJ.getcfg("actual_list_id","")
			
			# Recupero la lista activa
			if (len(actual_list_id) > 0) and (actual_list_id in self.lstCACHE):
				self.actual_list_name = actual_list_id
				self.actual_list_index = self.lstCACHE.index(actual_list_id)
				
			# Recupero el elemento activo de cada lista
			for tmplst in self.lstCACHE:
				actual_item_id = cfgOBJ.getcfg(tmplst+"_actual_item_id","")
				try:
					if (len(actual_item_id) > 0) and (actual_item_id in self.LST[tmplst]["_CACHE_"]):
						self.LST[tmplst]["_ACTUAL_ITEM_NAME"] = actual_item_id
						self.LST[tmplst]["_ACTUAL_ITEM_INDEX"] = self.LST[tmplst]["_CACHE_"].index(actual_item_id)
				except:
					plfiles._LOG("ERR. CACHE ITEM NOT FOUND ["+tmplst+"."+actual_item_id+"]")

	def write(self):
		"""Guarda la configuración (recordando la lista activa y el elemento activo de cada lista)"""
		if (len(self.cfgFILE) > 0):
			cfgOBJ = iniCFG(self.cfgFILE,"MENU")
			cfgOBJ.setcfg("actual_list_id",self.actual_list_name)
			
			# Me recorro todas las listas y guardo el elemento activo d cada una de ellas
			for tmplst in self.lstCACHE:
				try:
					cfgOBJ.setcfg(tmplst+"_actual_item_id",self.LST[tmplst]["_ACTUAL_ITEM_NAME"])
				except:
					plfiles._LOG("ERR. WRITING CFG ["+tmplst+"]")

			cfgOBJ.write()			


	# Devuelve una propiedad de la lista activa (si no se indica ninguna opción, simplemente devuelve el ID de la lista)
	# Si la opción solicitada no existe se devolverá una cadena en blanco
	def getlist(self,lstOPT=""):
		if (len(lstOPT) == 0): 
			valOPT = self.actual_list_name
		else:
			valOPT = ""
			try:
				idLST="¿?"
				if (self.actual_list_name in ["__MOST","__FOUND","__ALL"]):	
					# En __MOST y __ALL debo determinar la lista original a la que pertenece el elemento
					idITM = self.LST[self.actual_list_name]["_CACHE_"][self.LST[self.actual_list_name]["_ACTUAL_ITEM_INDEX"]]
					idLST = idITM.split(":")[0]
				else:
					idLST = self.actual_list_name

				valOPT += self.LST[idLST][lstOPT]
			except: valOPT = "NOT_FOUND:"+idLST
				
		return valOPT
	
	# Avanza hasta la siguiente lista (si es posible)
	# Las listas son siempre tratas ordenadas alfabéticamente
	def nextlist(self):
		if (len(self.LST) > 1):
			# Avanzo una posición
			self.actual_list_index += 1
			if self.actual_list_index > (len(self.lstCACHE)-1): self.actual_list_index = 0
			# Actualizo la lista actual
			self.actual_list_name = self.lstCACHE[self.actual_list_index]

		if (self.actual_list_name in ["__MOST","__ALL","__FOUND"]): self.nextlist()
		
		return self.actual_list_name
				
	# Retrocede hasta la siguiente lista (si es posible)
	# Las listas son siempre tratas ordenadas alfabéticamente
	def prevlist(self):
		if (len(self.LST) > 1):
			# Avanzo una posición
			self.actual_list_index -= 1
			if self.actual_list_index < 0: self.actual_list_index = len(self.lstCACHE)-1
			# Actualizo la lista actual
			self.actual_list_name = self.lstCACHE[self.actual_list_index]
		
		if (self.actual_list_name in ["__MOST","__ALL","__FOUND"]): self.prevlist()
		
		return self.actual_list_name
				
	# Devuelve el ID u otros valores del item activo (o de X items anteriores/posteriores)
	def getitem(self,itemNDX=0,itemNFO=0):
		# Si se especificó avanzar o retroceder X elementos
		
		if (self.actual_list_name in self.LST) and (len(self.LST[self.actual_list_name]) > 0):
			lenLST = len(self.LST[self.actual_list_name]["_CACHE_"])
			
			if (itemNDX != 0) and (lenLST > 0):
				if (abs(itemNDX) > lenLST): itemNDX %= lenLST
				tmpNDX = self.LST[self.actual_list_name]["_ACTUAL_ITEM_INDEX"] + itemNDX
				if (tmpNDX > (lenLST-1)): tmpNDX -= lenLST
			else:
				tmpNDX = self.LST[self.actual_list_name]["_ACTUAL_ITEM_INDEX"]
			
			try:	
				valOPT = self.LST[self.actual_list_name]["_CACHE_"][tmpNDX]
			except:  
				valOPT = ""
			
			if len(valOPT) > 0:
				# Nombre del ITEM
				if (itemNFO == 1): valOPT = self.LST[self.actual_list_name]["_ITEMS_"][valOPT]
				# Imagen del ITEM
				elif (itemNFO == 2): 
					if (self.actual_list_name in ["__MOST","__ALL","__FOUND"]):	
						# En __MOST y __ALL debo determinar la lista original a la que pertenece el elemento
						idITM = self.LST[self.actual_list_name]["_CACHE_"][self.LST[self.actual_list_name]["_ACTUAL_ITEM_INDEX"]]
						idLST = idITM.split(":")[0]
						valOPT = idITM.split(":")[1]
					else:
						idLST = self.actual_list_name
					
					try: 
						valOPT = self.LST[idLST]["_IMAGES_"][valOPT]
						valOPT = os.path.join(self.LST[idLST]["list_image_dir"] , valOPT)
					except: 
						plfiles._LOG("WAR. no image for "+idLST+"."+valOPT)
						valOPT = self.LST[idLST]["list_image_def"] 
			else:
				valOPT = "NOT_FOUND:"+self.actual_list_name
				
		else:
			valOPT = "NOT_FOUND:"+self.actual_list_name
		
		return valOPT


	# Avanza hasta la siguiente lista (si es posible)
	# Las listas son siempre tratas ordenadas alfabéticamente
	def nextitem(self,skipITEM=1):
		if ("_ITEMS_" in self.LST[self.actual_list_name]) and (len(self.LST[self.actual_list_name]["_ITEMS_"]) > 1):
			# Avanzo una posición (por vuelta)
			for loop in range(skipITEM):
				self.LST[self.actual_list_name]["_ACTUAL_ITEM_INDEX"] += 1
				if self.LST[self.actual_list_name]["_ACTUAL_ITEM_INDEX"] > (len(self.LST[self.actual_list_name]["_CACHE_"])-1): self.LST[self.actual_list_name]["_ACTUAL_ITEM_INDEX"] = 0
			# Actualizo la lista actual
			self.LST[self.actual_list_name]["_ACTUAL_ITEM_NAME"] = self.LST[self.actual_list_name]["_CACHE_"][self.LST[self.actual_list_name]["_ACTUAL_ITEM_INDEX"]]
			return self.LST[self.actual_list_name]["_ACTUAL_ITEM_NAME"]
		else: return "NOT_FOUND:"+self.actual_list_name
			
				
	# Retrocede hasta la siguiente lista (si es posible)
	# Las listas son siempre tratas ordenadas alfabéticamente
	def previtem(self,skipITEM=1):
		if ("_ITEMS_" in self.LST[self.actual_list_name]) and (len(self.LST[self.actual_list_name]["_ITEMS_"]) > 1):
			# Avanzo una posición (por vuelta)
			for loop in range(skipITEM):
				self.LST[self.actual_list_name]["_ACTUAL_ITEM_INDEX"] -= 1
				if self.LST[self.actual_list_name]["_ACTUAL_ITEM_INDEX"] < 0: self.LST[self.actual_list_name]["_ACTUAL_ITEM_INDEX"] = (len(self.LST[self.actual_list_name]["_CACHE_"])-1)
			# Actualizo la lista actual
			self.LST[self.actual_list_name]["_ACTUAL_ITEM_NAME"] = self.LST[self.actual_list_name]["_CACHE_"][self.LST[self.actual_list_name]["_ACTUAL_ITEM_INDEX"]]
			return self.LST[self.actual_list_name]["_ACTUAL_ITEM_NAME"]
		else: return "NOT_FOUND:"+self.actual_list_name
			
	
	# Filtra según los parámetros de búsqueda	
	def find(self,filter_text):
		# RESETEO LA LISTA DE BUSQUEDA
		del self.LST["__FOUND"]["_ITEMS_"]
		self.LST["__FOUND"]["_ITEMS_"] = {}			# Diccionario de elementos/nombres
		
		#Añado los elementos a la lista que coincidan con el parámetro de búsqueda
		# El filtro solo afecta a la lista de ITEMS
		filter_text = filter_text.replace("_"," ")
		
		for found_item in self.LST["__ALL"]["_ITEMS_"]:
			found_name = self.LST["__ALL"]["_ITEMS_"][found_item]
			if found_name.lower().find(filter_text) > -1:
				self.LST["__FOUND"]["_ITEMS_"][found_item] = found_name
		
		del self.LST["__FOUND"]["_CACHE_"]
		self.LST["__FOUND"]["_CACHE_"] = ("","")		
		self.lstSORT("__FOUND")

	# Devuelve el ID de la lista activa
	def getListID(self):
		if (self.actual_list_name in ["__MOST","__FOUND","__ALL"]):
			# En estas listas debo determinar la lista original a la que pertenece el elemento
			idITM = self.LST[self.actual_list_name]["_CACHE_"][self.LST[self.actual_list_name]["_ACTUAL_ITEM_INDEX"]]
			idLST = idITM.split(":")[0]
			idITM = idITM.split(":")[1]
		else:
			idLST = self.actual_list_name
			idITM = self.LST[idLST]["_ACTUAL_ITEM_NAME"]
		
		return idLST
	
	# Devuelve el ID del item activo
	def getItemID(self):
		if (self.actual_list_name in ["__MOST","__FOUND","__ALL"]):
			# En estas listas debo determinar la lista original a la que pertenece el elemento
			idITM = self.LST[self.actual_list_name]["_CACHE_"][self.LST[self.actual_list_name]["_ACTUAL_ITEM_INDEX"]]
			idLST = idITM.split(":")[0]
			idITM = idITM.split(":")[1]
		else:
			idLST = self.actual_list_name
			idITM = self.LST[idLST]["_ACTUAL_ITEM_NAME"]
		
		return idITM
		



