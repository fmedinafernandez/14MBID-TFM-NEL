'''
Created on 27 dec. 2022

@author: fmedinafernandez
'''
import os
import subprocess
from pathlib import Path
import com.fmedinafernandez.ClinicalNELEngine.general.logs as logs
import json
from json import JSONEncoder
import numpy

class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)

def serialiceNumpyArray(numpyArrayOne):
	# Serialization
	numpyData = {"array": numpyArrayOne}
	encodedNumpyData = json.dumps(numpyData, cls=NumpyArrayEncoder)  # use dump() to write array into file
	#print("Printing JSON serialized NumPy array")
	#print(encodedNumpyData)
	return encodedNumpyData

def deserialiceNumpyArray(encodedNumpyData):
	# Deserialization
	#print("Decode JSON serialized NumPy array")
	decodedArrays = json.loads(encodedNumpyData)
	return numpy.asarray(decodedArrays["array"])


def execute_os_command(comando):
    logs.log('utils.execute_os_command("'+comando+'")')
    return subprocess.Popen(comando, shell=True, stdout=subprocess.PIPE).stdout

def str2fecha(fecha_cadena):
    return fecha_cadena[6:8] + '/' + fecha_cadena[4:6] + '/' + fecha_cadena[0:4]

def delete_directory(directory):
    logs.log("utils.delete_directory('" + directory + "')")
    if Path(directory).exists():
        ficheros=os.listdir(directory)
        for fichero in ficheros:
            os.remove(directory+'\\'+fichero)
        os.rmdir(directory)
    else:
        pass

def delete_bak_files(directory):
    logs.log("utils.delete_bak_files('" + directory + "')")
    if Path(directory).exists():
        ficheros=os.listdir(directory)
        for fichero in ficheros:
            if (fichero[-3:]=='bak' or fichero[-3:]=='BAK'):
                os.remove(directory+'\\'+fichero)
    else:
        pass

def create_directory(directory):
    logs.log("utils.create_directory('" + directory + "')")
    #Comprobar que si ya existe no lo vuelva a crear
    if not Path(directory).exists():
        os.makedirs(directory)
    else:
        pass
