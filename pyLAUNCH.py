# -*- coding: iso-8859-15 -*-

# Librer�as y variables utilizadas
import plmenu,plvideo,plfiles

# C�digo principal
def main():
	# Inicializo el LOG
	plfiles._clearLOG()
	
	# el MENU que lo controla todo
	mainMENU = plmenu.MENU()

	# Bucle principal de acci�n
	while not mainMENU.exitMENU:  mainMENU.loop()
	
	# Al abandonar el bucle operaciones finales antes de cerrar
	mainMENU.MUSIC.write()
	mainMENU.LIST.write()

	plvideo.shutdownEFFECT(mainMENU)
	
	plfiles._LOG("END.frames: "+str(mainMENU.frames) + " / loops: "+str(mainMENU.loops))

if __name__ == '__main__':
	main()	