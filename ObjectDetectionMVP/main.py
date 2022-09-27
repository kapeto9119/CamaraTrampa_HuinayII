import numpy as np
import csv, time, datetime, os

import detectObjects

IMAGES_DIR = 'recognize'

d = datetime.datetime.now()
timestamp = "%04d%02d%02d%02d%02d" % (d.year, d.month, d.day, d.hour, d.minute)
timestamp = str(timestamp)

csv_name = 'objects_detection_on_{0}.csv'.format(timestamp)

csv_file = open(csv_name, 'w')
writer = csv.writer(csv_file)

index = ['File', 'Animal', 'Confidence']
writer.writerow(index)

directory = IMAGES_DIR

for filename in os.listdir(directory):
    f = str(os.path.join(directory, filename))
    detectObjects.detectObjectOfImage(f, writer, timestamp)

file_name = '{0}'.format(csv_name)

print("Proceso terminado, se apaga RPI")
os.system('sudo rm -r recognize/')
os.system('sudo shutdown now')
# print(file_name)