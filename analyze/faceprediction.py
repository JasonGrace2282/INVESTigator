import time
from pathlib import Path

import cv2
import numpy as np
from tensorflow.keras.models import load_model


def get_face(inputs):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(inputs)
    frame_count = 0
    last_screenshot_time = time.time()
    predicted = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        frame_count += 1
        current_time = time.time()
        elapsed_time = current_time - last_screenshot_time
        if elapsed_time > 1:
            if len(faces) > 0:
                for (x, y, w, h) in faces:
                    y1 = max(0, y - 120)
                    y2 = min(frame.shape[0], y + h + 120)
                    x1 = max(0, x - 120)
                    x2 = min(frame.shape[1], x + w + 120)
                    roi = frame[y1:y2, x1:x2]
                    path = f'face_ss{frame_count}.jpg'
                    cv2.imwrite(path, roi)
                    predicted.append(prediction(path))
                    last_screenshot_time = current_time
                    break

    cap.release()
    return predicted

def preprocess(image_path: str):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    image_resized = cv2.resize(image, (48, 48))
    image_normalized = image_resized / 255.0
    image_reshaped = image_normalized.reshape(-1, 48, 48, 1)
    return image_reshaped

def prediction(image_path: str):
    model = load_model(Path(__file__).resolve().parent / 'facial_expression_model.h5')
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
