# -*- coding: iso-8859-15 -*-

import os,pygame,plvideo,plfiles,plconfig
import subprocess,time

# La finalidad de esta clase es gestionar las músicas y los efectos de sonido
class launcher:
	"""Objeto encargado de ejecutar ITEMS y devolver el control al menu"""

	def __init__(self):
		"""incialización de del objeto"""

	def launch(self,plMENU):
		"""Ejecuta el item activo de thelist"""

		# IDS de Item y lista
		idLST = plMENU.LIST.getListID()
		idITM = plMENU.LIST.getItemID()

		# Ruta del elemento
		item_path = plMENU.LIST.LST[idLST]["list_item_dir"]
		# Nombre del fichero
		item_name = idITM
		# Extensión del fichero
		item_ext = plMENU.LIST.LST[idLST]["list_item_extension"][0]
		# Imagen del fichero seleccionado actualmente
		item_img = plMENU.LIST.getitem(0,2)
		# Identificador interno del elemento/juego
		item_id = idITM
		# Nombre del elemento/juego
		item_txt = plMENU.LIST.getitem(0,1)

		# Los 2 elementos anteriores sumados FICHERO+EXTENSION
		item_fullname = item_name+item_ext
		# Los 3 elementos anteriores sumados RUTA+FICHERO+EXTENSION
		item_fullpath = item_path+"\\"+item_name+item_ext

		# Ruta del ejecutor
		launcher_path = os.path.dirname(plMENU.LIST.LST[idLST]["list_launcher_file"])
		tmp_file = os.path.splitext(os.path.basename(plMENU.LIST.LST[idLST]["list_launcher_file"]))
		# Nombre del ejecutor
		launcher_name = tmp_file[0]
		# Extensión del ejecutor
		if (len(tmp_file) > 1):	launcher_ext = tmp_file[1]
		else:				launcher_ext = ""
		
		# Los 2 elementos anteriores sumados FICHERO+EXTENSION
		launcher_fullname = os.path.basename(plMENU.LIST.LST[idLST]["list_launcher_file"])
		# Los 3 elementos anteriores sumados RUTA+FICHERO+EXTENSION
		launcher_fullpath = plMENU.LIST.LST[idLST]["list_launcher_file"]
		#Directorio actual
		current_dir = str(os.getcwd())
		
		# Cuento el número de veces que se ha ejecutado cada item
		cfgFAV = plconfig.iniCFG(plMENU.state_config_file,"__MOST")
		playCOUNT = cfgFAV.getcfg(idLST+"_"+item_id,0) + 1
		cfgFAV.setcfg(idLST+"_"+item_id,playCOUNT)
		cfgFAV.write()

		# Se sale del modo gráfico (para detectar la resolución real de windows)
		pygame.display.quit() 
		pygame.init()
		splashRES = (pygame.display.Info().current_w,pygame.display.Info().current_h)
		plvideo.videoSPLASH(plMENU,splashRES)

		# Carga de la imágen y Escala 2x (solo si está configurada)
		splIMG = plvideo.loadIMG(item_img).convert()
		if plMENU.CFG["snap_scale2x"]:  splIMG = pygame.transform.scale2x(splIMG)
		plMENU.main_screen.blit(plvideo.sizeIMG(splIMG,splashRES), (0,0))

		# Calculo las posiciones de los textos y el tamaño del recuadro traslúcido del fondo
		txt1Y = int(splashRES[1]/2)-(plMENU.vTXT.get_dim()[1]/2)
		txt2Y = int(splashRES[1]/2)+(plMENU.vTXT.get_dim()[1]/2)
		
		x1 = 0
		y1 = txt1Y-plMENU.vTXT.get_dim()[1]
		x2 = splashRES[0]
		y2 = plMENU.vTXT.get_dim()[1]*3

		# Dibujo un recuadro traslúcido 
		tmpSURFACE = pygame.Surface((x2-x1, y2), pygame.SRCALPHA)
		tmpSURFACE.fill(pygame.Color(0,0,0,200))
		plMENU.main_screen.blit(tmpSURFACE,(x1,y1))
		
		# Textos de carga
		plMENU.vTXT.msg(plMENU.main_screen,"loading...  ("+str(playCOUNT)+" times)",(-1,txt1Y),plMENU.CFG["font1_color"])
		plMENU.vTXT.msg(plMENU.main_screen,item_txt,(-1,txt2Y),plMENU.CFG["font1_color"])
		pygame.display.flip()
		pygame.image.save(plMENU.main_screen, "splash.jpg")


		# Transformo rutas relativas en absolutas
		# Esto habrá que revisarlo en LINUX
		if not ":" in item_fullpath:
			item_fullpath = current_dir + "\\" + item_fullpath
			item_path = current_dir + "\\" + item_path

		if not ":" in launcher_fullpath:
			launcher_fullpath = current_dir + "\\" + launcher_fullpath
			launcher_path = current_dir + "\\" + launcher_path
		
		# Los espacios en blanco en las rutas de ficheros no puede ir al comando o generarán un error
		if " " in item_fullpath: item_fullpath = '"'+item_fullpath+'"'
		if " " in item_fullname: item_fullname = '"'+item_fullname+'"'
		if " " in item_name: item_name = '"'+item_name+'"'
		if " " in item_path: item_path = '"'+item_path+'"'

		# Cadena de lanzamiento
		launcher_options =  plMENU.LIST.LST[idLST]["list_launcher_options"]
		if len(launcher_options) == 0: launcher_options = "*launcher_fullpath* *item_fullpath*"
		
		# Compongo la cadena de lanzamiento
		old_launcher_options = launcher_options
		if "*item_path*" in launcher_options: launcher_options = launcher_options.replace("*item_path*",item_path)
		if "*item_name*" in launcher_options: launcher_options = launcher_options.replace("*item_name*",item_name)
		if "*item_ext*" in launcher_options: launcher_options = launcher_options.replace("*item_ext*",item_ext)
		if "*item_fullname*" in launcher_options: launcher_options = launcher_options.replace("*item_fullname*",item_fullname)
		if "*item_fullpath*" in launcher_options: launcher_options = launcher_options.replace("*item_fullpath*",item_fullpath)
		
		if "*launcher_path*" in launcher_options: launcher_options = launcher_options.replace("*launcher_path*",launcher_path)
		if "*launcher_name*" in launcher_options: launcher_options = launcher_options.replace("*launcher_name*",launcher_name)
		if "*launcher_ext*" in launcher_options: launcher_options = launcher_options.replace("*launcher_ext*",launcher_ext)
		if "*launcher_fullname*" in launcher_options: launcher_options = launcher_options.replace("*launcher_fullname*",launcher_fullname)
		if "*launcher_fullpath*" in launcher_options: launcher_options = launcher_options.replace("*launcher_fullpath*",launcher_fullpath)
			
		if "*current_dir*" in launcher_options: launcher_options = launcher_options.replace("*current_dir*",current_dir)
		if "*item_id*" in launcher_options: launcher_options = launcher_options.replace("*item_id*",item_id)
		if "*item_txt*" in launcher_options: launcher_options = launcher_options.replace("*item_txt*",item_txt)
		
		old_display_caption = pygame.display.get_caption()[0]
		pygame.display.set_caption(item_txt)
		
		if plMENU.CFG["debug_mode"]:
			# En modo debug ejecuto a través de un .CMD
			batch_file = open("cfg\\pyLAUNCH.cmd","w")

			# en modo depuración no se ocultan los comandos
			batch_file.write("echo CURRENT DIR "+current_dir+"\n")
			batch_file.write("echo LOADING "+item_txt+"\n")
			
			# Me cambio al directorio del lanzador
			batch_file.write(current_dir[:2]+"\n")
			batch_file.write("cd "+launcher_path+"\n")
			
			# Ejecuto el comando "mágico"
			batch_file.write("echo "+old_launcher_options+"\n")
			batch_file.write(launcher_options+"\n")
			batch_file.write("pause\n")
			batch_file.write("\n")
			
			batch_file.close()
		
		plfiles._LOG("OK.Launching ("+idLST+"."+item_id+" / "+item_txt+")")

		if plMENU.CFG["debug_mode"]:
			plfiles._LOG("DBUG pyLAUNCH.DIR ("+os.getcwd()+")")
			plfiles._LOG("DBUG appDIR.DIR ("+launcher_path+")")
			plfiles._LOG("DBUG launch.CMD ("+launcher_options+")")
			# Esto solo funcionaría en Windows
			#exeCMD = '"'+os.getcwd()+'\cfg\\pyLAUNCH.cmd"'
			#subprocess.Popen(exeCMD).wait()

		os.chdir(launcher_path+"\\")
		# Si shell=True puede causar problemas en LINUX?
		# PAUSA MUSICA y El efecto de sonido correspondiente
		# Escribo los valores de posición y melodía
		appOBJ = subprocess.Popen(launcher_options,shell=False)
		time.sleep(1)
		pygame.display.quit() 
		plMENU.LIST.write()
		plMENU.MUSIC.write()
		
		appOBJ.wait()
		os.chdir(current_dir)		
		plfiles._LOG("OK.Returning ("+idLST+"."+item_id+" / "+item_txt+")")
				
		try:
			plvideo.videoINIT(plMENU)
		except:
			time.sleep(1)
			plvideo.videoINIT(plMENU)
			
		plMENU.keypress = "no_event"
		plMENU.MUSIC.next()
		
		plMENU.vDISP.show_list = True
		plMENU.vDISP.anim_image = False
		plMENU.vDISP.show_image = True
		plMENU.vDISP.anim_list = False
		
		plMENU.vDISP.show_title = True
		plMENU.vDISP.show_stats = True
		plMENU.vDISP.show_wall = True
		plMENU.vDISP.anim_wall = False
			
		plMENU.vDISP.refresh()
