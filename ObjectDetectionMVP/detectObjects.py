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

def detectObjectOfImage(path, writer, timestamp):
    
    class_names = ['conejo', 'gato', 'pajaro', 'perro', 'raton', 'zorro']

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

    predictions_lite = classify_lite(sequential_1_input=img_array)['outputs']

    score_lite = tf.nn.softmax(predictions_lite)

    db.collection(str(timestamp)).add({'File': str(os.path.normpath(path)), 'Animal':str(class_names[np.argmax(score_lite)]), 'Confidence':str(100 * np.max(score_lite))})

    row = [os.path.basename(os.path.normpath(path)), class_names[np.argmax(score_lite)], 100 * np.max(score_lite)]

    if (100 * np.max(score_lite) > THRESHOLD):
        writer.writerow(row)

    # print(
    #     "Se predice que esta imagen pertenece a {} con un {:.2f} porciento de confianza."
    #     .format(class_names[np.argmax(score_lite)], 100 * np.max(score_lite))
    # )
    return 0