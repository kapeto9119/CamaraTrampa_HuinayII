import tensorflow as tf
import numpy as np
from PIL import Image
import csv, time, datetime, os

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

#Python 3.7.13

TF_MODEL_FILE_PATH = 'model.tflite'
THRESHOLD = 20

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

def detectObjectOfImage(path, filename, writer, timestamp):
    
    # class_names = ['conejo', 'gato', 'pajaro', 'perro', 'raton', 'zorro']

    img_height = 180
    img_width = 180

    img_path = path

    img = Image.open(img_path)

    img = tf.keras.utils.load_img(img_path, target_size=(img_height, img_width))
    
    img_array = tf.keras.utils.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)

    interpreter = tf.lite.Interpreter(model_path=TF_MODEL_FILE_PATH)
    # interpreter.allocate_tensors()

    interpreter.get_signature_list()

    classify_lite = interpreter.get_signature_runner('serving_default')

    interpreter.get_input_details()

    img_array = img_array.astype("float32")

    encoded = encode(input_2=img_array)

    predictions = tf.nn.sigmoid(encoded["dense"])

    predictions = tf.where(predictions < 0.8, 0, 1) #esta linea hace que solo tire 1 si es sobre 80% de confianza

    # predictions_lite = classify_lite(sequential_1_input=img_array)['outputs']

    # score_lite = tf.nn.softmax(predictions_lite)

    # db.collection(str(timestamp)).add({'File': str(os.path.normpath(path)), 'Animal':str(class_names[np.argmax(score_lite)]), 'Confidence':str(100 * np.max(score_lite))})

    # db.collection(str(timestamp)).add({'File': str(os.path.normpath(path)), 'Animal':predictions.numpy(), 'Confidence':str(100 * np.max(score_lite))})

    i0 = "Ave"
    i1 = "Conejo"
    i2 = "Raton"
    i3 = "Zorro"

    lista = predictions.numpy()
    max_value = max(lista)
    max_index = lista.index(max_value)

    if max_index == 0:
        animal = i0
    elif max_index == 1:
        animal = i1
    elif max_index == 2:
        animal = i2
    elif max_index == 3:
        animal = i3

    print('Predictions:\n', (predictions.numpy())[])

    year_data = filename[4] + filename[5] + filename[6] + filename[7]
    month_data = filename[9] + filename[10]
    day_data = filename[11] + filename[12]
    hour_data = filename[14] + filename[15]
    minute_data = filename[16] + filename[17]

    time = year_data + "/" + month_data + "/" + day_data + " " + hour_data + ":" + minute_data
    # "2022/09/01 08:50"

    row = [time, os.path.basename(os.path.normpath(path)), animal, 100 * max_value]

    # row = [time, os.path.basename(os.path.normpath(path)), class_names[np.argmax(score_lite)], 100 * np.max(score_lite)]

    if (100 * np.max(score_lite) > THRESHOLD):
        writer.writerow(row)

    return 0