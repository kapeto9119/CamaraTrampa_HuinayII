# Programa para ejecutar copia de seguridad. Elimina fotos duplicadas, mueve estos archivos y ejecuta script para reconocimiento de imagenes con tesorflow lite.

# print("--------------------------------------------------------------------")

# print("\nEjecutando copia de seguridad.\n")

#Importar librerias
import os, glob, shutil, time, hashlib, datetime
from pathlib import Path

# Directorios
#source = "/media/smartdots/HP-ESXI-5_5/DCIM/PHOTO"            #Carpeta que contiene incialmente las imagenes
#source = "/home/smartdots/Documents/source"
#recognize = "/home/smartdots/Documents/recognize"      #Carpeta donde se reconocen las imagenes con tensorflow lite
# destination = "/home/pi/Downloads/destination"  #Carpeta de respaldo con las imagenes iniciales
# destination = "/mnt/storage/destination"


class Transferencia:
    def __init__(self, source, destination):
        self.source = source
        self.destination = destination

    def find_duplicates(self):
        hashes = {}
        duplicates = []
        ubicacion = self.source

        filePath = Path(ubicacion)
        if filePath.is_dir():
            files = list(x for x in filePath.iterdir() if x.is_file())

        for file in files:
            file_name = Path(os.path.join(ubicacion, file))
            
            if file_name.is_file():
                temp_hash = hashlib.md5(open(file_name, 'rb').read()).hexdigest()
                
                if temp_hash in hashes:
                    print("Archivo '{}' duplicado de '{}' en '{}'.".format(os.path.basename(file),os.path.basename(hashes[temp_hash]), os.path.basename(ubicacion)))
                    duplicates.append(file)
                else:
                    hashes[temp_hash] = file
                
        if len(duplicates) != 0:
            space_saved = 0
            
            for duplicate in duplicates:
                space_saved += os.path.getsize(os.path.join(self.source,duplicate))
                    
                os.remove(os.path.join(self.source,duplicate))
                print("Eliminando '{}'.".format(os.path.basename(duplicate)))
            
            print("Se han recuperado {} KB de espacio de almacenamiento en '{}'.\n".format(round(space_saved/1000), os.path.basename(self.source)))
            
        else:
            print("No se han encontrado fotos duplicadas en '{}'.".format(os.path.basename(self.source)))


    def transfer_files(self):
        os.mkdir(self.destination)
        print("\n-Moviendo archivos desde '{}' a '{}'.".format(os.path.basename(self.source), os.path.basename(self.destination)))
        flag = 0
        ubicacion = self.source
        filePath = Path(ubicacion)
        if filePath.is_dir():
            files = list(x for x in filePath.iterdir() if x.is_file())

            for picture in files:
                flag=1
                shutil.copy(os.path.join(self.source, picture), self.destination) # Copia los archivos desde una carpeta a la otra.
                os.remove(os.path.join(self.source, picture)) # Remueve fotos tras transferirlas.
                name = os.path.basename(picture)
                            
        if flag==0:
            print("No se han encontrado archivos para trasladar.")
    
    def copy_files(self):
        os.mkdir(self.destination)
        print("\n-Copiando archivos desde '{}' a '{}'.".format(os.path.basename(self.source), os.path.basename(self.destination)))
        flag = 0
        ubicacion = self.source
        filePath = Path(ubicacion)
        if filePath.is_dir():
            files = list(x for x in filePath.iterdir() if x.is_file())

            for picture in files:
                flag=1
                shutil.copy(os.path.join(self.source, picture), self.destination) # Copia los archivos desde una carpeta a la otra.
                # os.remove(os.path.join(self.source, picture)) # Remueve fotos tras transferirlas.
                name = os.path.basename(picture)
                            
        if flag==0:
            print("No se han encontrado archivos para copiar.")