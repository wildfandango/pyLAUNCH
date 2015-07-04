# -*- coding: iso-8859-15 -*-

import os
from xml.dom.minidom import parse,parseString

# De una cadena del estilo val = <tag>VALOR</tag> y tag = tag devuelve VALOR
# ej: getVAL("<info>ejemplo</info>","info") -> ejemplo
def getVAL(val,tag):
	txt = val[len(tag)+2:len(val)-(len(tag)+3)]
	return txt
	
# Limpia una descripción haciendo lo siguiente
# Elimina los caracters [ , ]
# Elimina los caracteres a partir de / o (
def cleanDES(txt):
	# Elimino caracteres indeseados
	txt = txt.replace("[","")
	txt = txt.replace("]","")
	
	# Elimino todo el texto que siga al caracter /
	txt = txt.split("/")[0]
	
	# Elimino todo el texto que siga al caracter (
	txt = txt.split("(")[0]
	
	return txt.strip()
	
def renderTXT(file):
	dom = parse("info.xml")
	names = {}	# Inicializo el diccionario de nombres

	for node in dom.getElementsByTagName('game'):
		# Obtengo el nombre de la ROM
		for value in node.toxml().split():
			if value[:5] == ("name="): 
				txtROM = value
				# Elimino caracteres indeseados
				txtROM = txtROM[6:len(value)-1]
				break
		
		# Descripción
		xmlTAG = 'description'
		txtDES = node.getElementsByTagName(xmlTAG)[0].toxml()
		txtDES = cleanDES(getVAL(txtDES,xmlTAG))
		if len(txtDES) == 0: txtDES = txtROM
		
		# Año
		xmlTAG = 'year'
		try:
			txtYEA = node.getElementsByTagName(xmlTAG)[0].toxml()
			txtYEA = getVAL(txtYEA,xmlTAG)
		except:
			txtYEA = "19??"
		
		# Fabricante
		xmlTAG = 'manufacturer'
		txtMAN = node.getElementsByTagName(xmlTAG)[0].toxml()
		txtMAN = cleanDES(getVAL(txtMAN,xmlTAG))
		
		# Nombre (Fabricante.Año)
		#names[txtROM] = txtDES+" ("+txtMAN+"."+txtYEA+")"

		# Nombre (Año)
		#names[txtROM] = txtDES+" ("+txtYEA+")"

		# Nombre (solo)
		#names[txtROM] = txtDES
		
		# Año. Nombre (Fabricante)
		names[txtROM] = txtYEA + "  " + txtDES+" ("+txtMAN+")"

	# Al terminar ordeno la lista a generar y vuelvo en un fichero de texto
	index = names.keys()
	index.sort()

	for item in index:
		file.write(item+" "*(16-len(item))+names[item]+"\n")
	
	
if __name__ == '__main__':
	
	pref = ("0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z")
	
	# Preparo el fichero de texto
	file = open("info.txt","w")

	for let in pref:
		# Genero un XML diferente por cada letra, de lo contrario el XML seria demasido grande
		print let,"..."
		os.system("M:\mame\MAMEUI32.exe -listxml "+let+"* > info.xml")
		renderTXT(file)

	file.close()