import RPi.GPIO as GPIO
import time, datetime, os

# BEGIN 2022-09-17 00:10:00
# END   2025-07-31 23:59:59
# ON    M5    WAIT
# OFF   M59

from TransferImages import Transferencia


GPIO.setmode(GPIO.BOARD)

GPIO.setup(38, GPIO.OUT) #Poder del HUB USB para activar cam
GPIO.setup(36, GPIO.IN) #Ver si la cam esta trabajando

GPIO.output(38, GPIO.LOW) #Apago HUB

d = datetime.datetime.now()
timestamp = "%04d%02d%02d%02d%02d" % (d.year, d.month, d.day, d.hour, d.minute)
folderWithDate = str(timestamp)

# Directorios
nameOfDevice = str((os.listdir("/media/smartdots/")[0])
source = "/media/smartdots/" + nameOfDevice + "/DCIM/PHOTO"
# source = "/media/smartdots/HP-ESXI-5_5/DCIM/PHOTO"            #Carpeta que contiene incialmente las imagenes
recognize = "/home/smartdots/Documents/ObjectDetectionMVP/recognize"      #Carpeta donde se reconocen las imagenes con tensorflow lite

folder = "/home/smartdots/Documents/CamaraTrampa_HuinayII/ObjectDetectionMVP/"

print("Espera de 5 seg.")
time.sleep(5)

while 1:
	value = GPIO.input(36)
	print(value)
	if (value == GPIO.LOW):
		print("Activando modo de almacenamiento masivo de la camara")
		GPIO.output(38, GPIO.HIGH)
		time.sleep(15)
		print("Moviendo imagenes desde la camara hacia la carpeta con la fecha de importación")
		path1 = Transferencia(source, folderWithDate)
		path1.transfer_files()
		#Metodo para verificar si no quedan fotos dentro de la camara pendiente
		if os.listdir(folderWithDate) == []:
			#No quedan archivos
			time.sleep(5)
			print("Copiando imagenes de la carpeta con las fotos importadas, hacia carpeta de reconocimiento de imagen")
			path2 = Transferencia(str(folder+folderWithDate), recognize)
			path2.copy_files()
			time.sleep(5)
			break
	time.sleep(30)
print("Se apaga modo de almacenamiento de la camara")
GPIO.output(38, GPIO.LOW)

print("Se espera 10 seg.")
time.sleep(10)

GPIO.output(38, GPIO.LOW) #Apago HUB

GPIO.cleanup()

print("Se ejecuta main.py")

cmd = "python main.py " + str(nameOfDevice)

os.system(cmd)

# os.system("python3 main.py")
