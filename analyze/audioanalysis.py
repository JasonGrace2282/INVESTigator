import pickle
import re

import numpy as np
import pandas as pd
import speech_recognition as sr
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
from transformers import (AutoModelForSequenceClassification, AutoTokenizer,
                          pipeline)


def clean_text(text):
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    text = text.lower()
    text = text.strip()
    return text

def prediction(text):
    model = tf.keras.models.load_model('best_emotion_classification_model.h5')
    #load
    df = pd.read_csv('tweet_emotions.csv')

    # data cleansing
    df = df.drop(columns=['tweet_id'])
    df['content'] = df['content'].apply(clean_text)

    # tokenizer
    tokenizer = Tokenizer(num_words=10000, lower=True, oov_token='<OOV>')
    tokenizer.fit_on_texts(df['content'])
    with open('tokenizer.pickle', 'wb') as handle:
        pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

    # label encoder
    label_encoder = LabelEncoder()
    df['sentiment'] = label_encoder.fit_transform(df['sentiment'])
    num_classes = len(label_encoder.classes_)
    with open('label_encoder.pickle', 'wb') as handle:
        pickle.dump(label_encoder, handle, protocol=pickle.HIGHEST_PROTOCOL)

    with open('tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)

    with open('label_encoder.pickle', 'rb') as handle:
        label_encoder = pickle.load(handle)
        text = clean_text(text)
        sequence = tokenizer.texts_to_sequences([text])
        padded_sequence = pad_sequences(sequence, maxlen=150)
        prediction = model.predict(padded_sequence)
    return label_encoder.inverse_transform(np.argmax(prediction, axis=1))[0]

def speech_to_text_local(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.RequestError as e:
        return f"RequestError on Sentiment"
    except sr.UnknownValueError:
        return "Not recognizable"

def audioanalysis(file_path):
    transcribed_text = speech_to_text_local(file_path)
    #print(f"Transcribed Text: {transcribed_text}")
    cleaned_text = clean_text(transcribed_text)
    #print(f"Cleaned Text: {cleaned_text}")
    print(prediction(cleaned_text))
    return prediction(cleaned_text)
