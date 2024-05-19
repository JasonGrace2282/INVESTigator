import os
import pickle
import re
from pathlib import Path

import numpy as np
import pandas as pd
import speech_recognition as sr
import tensorflow as tf
from pydub import AudioSegment
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer


def clean_text(text):
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    text = text.lower()
    text = text.strip()
    return text

def prediction(text):
    model = tf.keras.models.load_model(
        Path(__file__).resolve().parent.parent / "ml" / 'best_emotion_classification_model.h5'
    )
    # Load the dataset
    df = pd.read_csv('tweet_emotions.csv')

    # Data cleansing
    df = df.drop(columns=['tweet_id'])
    df['content'] = df['content'].apply(clean_text)

    # Tokenizer
    tokenizer = Tokenizer(num_words=10000, lower=True, oov_token='<OOV>')
    tokenizer.fit_on_texts(df['content'])
    with open('tokenizer.pickle', 'wb') as handle:
        pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

    # Label encoder
    label_encoder = LabelEncoder()
    df['sentiment'] = label_encoder.fit_transform(df['sentiment'])
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
        return recognizer.recognize_google(audio)
    except sr.RequestError:
        return f"RequestError on Sentiment"
    except sr.UnknownValueError:
        return "Not recognizable"


def audioanalysis(file_path) -> str:
    transcribed_text = speech_to_text_local(file_path)
    cleaned_text = clean_text(transcribed_text)
    p = prediction(cleaned_text)
    return p


def split_audio(input_file):
    audio = AudioSegment.from_file(input_file)
    total_duration = len(audio)
    start = 0
    end = 60000
    arr = []
    while start < total_duration:
        if end > total_duration:
            end = total_duration
        segment = audio[start:end]
        output_dir = "output_segments"
        output_file = f"{output_dir}/{os.path.splitext(os.path.basename(input_file))[0]}_{start}_{end}.wav"
        segment.export(output_file, format="wav")
        start = end
        end += 60000
        arr.append(output_file)
    return arr


def runpredictions(input_file):
    os.makedirs("output_segments", exist_ok=True)
    arr = []
    for audio in split_audio(input_file):
        arr.append(audioanalysis(audio))
    return arr, audioanalysis(input_file)

