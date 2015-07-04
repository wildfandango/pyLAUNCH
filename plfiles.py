# -*- coding: iso-8859-15 -*-

import inspect,os,datetime

# La finalidad de este m�dulo es gestionar las anotaciones en ficheros LOG y XML

# Inicializa y vac�a el fichero de LOG
def _clearLOG(logFILE=os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + "\\pyLAUNCH.LOG"):
	# Reseteo el fichero y lo inicializo (en blanco)
	_LOG = open(logFILE,"w")
	_LOG.write(str(datetime.datetime.now()).split()[0]+ " > " +logFILE+"\n\n")
	_LOG.close()
	
# A�ade una nueva l�nea al LOG
def _LOG(txt="",dbug = True,logFILE=os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + "\\pyLAUNCH.LOG"):
	if (dbug or txt[:3] == "ERR"):
		_LOG = open(logFILE,"a")
		_LOG.write(str(datetime.datetime.now()).split()[1] +" > "+ txt+"\n")
		_LOG.close()

# A�ade una nueva l�nea un fichero de texto cualquiera
def _writeTXT(txt="",logFILE=""):
	logFILE = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + "\\" + logFILE
	_LOG = open(logFILE,"a")
	_LOG.write(txt+"\n")
	_LOG.close()

	
	
	
		

