import numpy as np
import csv, time, datetime, os, system

import detectObjects, EnvioDatos, csvToJson

IMAGES_DIR = 'recognize'

nameOfDevice = sys.argv

d = datetime.datetime.now()
timestamp = "%04d%02d%02d%02d%02d" % (d.year, d.month, d.day, d.hour, d.minute)
timestamp = str(timestamp)

csv_name = 'objects_detection_on_{0}.csv'.format(timestamp)

csv_file = open(csv_name, 'w')
writer = csv.writer(csv_file)

index = ['Date', 'File', 'Animal', 'Confidence']
writer.writerow(index)

directory = IMAGES_DIR

for filename in os.listdir(directory):
    f = str(os.path.join(directory, filename))
    detectObjects.detectObjectOfImage(f, filename, writer, timestamp)

file_name = '{0}'.format(csv_name)

content = csvToJson.read(file_name)

finalJson = {
    "deviceName": str(nameOfDevice)
    "values": [
        content
    ]
}

send = Envio(file_name, finalJson)
send.sendByEmail()
send.sendByHTTP()

print("Proceso terminado, se apaga RPI")
os.system('sudo rm -r recognize/')
os.system('sudo shutdown now')
# print(file_name)