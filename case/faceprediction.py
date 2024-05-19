import cv2
import numpy as np
from tensorflow.keras.models import load_model

#load model

def preprocess(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    image_resized = cv2.resize(image, (48, 48))
    image_normalized = image_resized / 255.0
    image_reshaped = image_normalized.reshape(-1, 48, 48, 1)
    return image_reshaped

def prediction(image_path):
    model = load_model('facial_expression_model.h5')
    image = preprocess(image_path)
    prediction = model.predict(image)
    label = np.argmax(prediction)
    if label == 0:
        return "Angry"
    if label == 1:
        return "Angry"
    if label == 2:
        return "Fear"
    if label == 3:
        return "Sad"
    if label == 4:
        return "Fear"
    if label == 5:
        return "Surprise"
    if label == 6:
        return "Fear"
