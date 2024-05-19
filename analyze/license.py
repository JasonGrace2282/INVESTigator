import string
import time
from collections.abc import Iterable
from pathlib import Path

import cv2
import easyocr
from ultralytics import YOLO

dict_char_to_int = {'O': '0', 'I': '1', 'J': '3', 'A': '4', 'G': '6', 'S': '5'}
dict_int_to_char = {v: k for k, v in dict_char_to_int.items()}

def license_complies_format(text):
    """
    Check if the license plate text complies with the required format.
    """

    if len(text) != 7:
        return False

    return (
        (text[0] in string.ascii_uppercase or text[0] in dict_int_to_char)
        and (text[1] in string.ascii_uppercase or text[1] in dict_int_to_char)
        and (
            text[2].isdigit()
            or text[2] in dict_char_to_int
        )
        and (
            text[3].isdigit()
            or text[3] in dict_char_to_int
        )
        and (text[4] in string.ascii_uppercase or text[4] in dict_int_to_char)
        and (text[5] in string.ascii_uppercase or text[5] in dict_int_to_char)
        and (text[6] in string.ascii_uppercase or text[6] in dict_int_to_char)
    )

def format_license(text):

    license_plate_ = ''
    mapping = {0: dict_int_to_char, 1: dict_int_to_char, 4: dict_int_to_char, 5: dict_int_to_char, 6: dict_int_to_char,
               2: dict_char_to_int, 3: dict_char_to_int}
    for j in range(7):
        if text[j] in mapping[j]:
            license_plate_ += mapping[j][text[j]]
        else:
            license_plate_ += text[j]
    return license_plate_

def read_license_plate(reader: easyocr.Reader, license_plate_crop):

    detections = reader.readtext(license_plate_crop)

    for detection in detections:
        bbox, text, score = detection

        text = text.upper().replace(' ', '')

        if license_complies_format(text):
            return format_license(text), score

    return None, None


def read_frame(video: str) -> Iterable[tuple[str, float, float]]:
    # Initialize the OCR reader
    reader = easyocr.Reader(['en'], gpu=False)

    # Load models
    license_plate_detector = YOLO(
        Path(__file__).resolve().parent.parent / "ml" / 'license_plate_detector.pt',
        verbose=False,
    )

    # Load video
    cap = cv2.VideoCapture(video)

    ret = True
    t0 = time.perf_counter()
    while ret:
        ret, frame = cap.read()
        if ret:
            license_plates = license_plate_detector(frame)[0]
            for license_plate in license_plates.boxes.data.tolist():
                x1, y1, x2, y2, score, class_id = license_plate

                license_plate_crop = frame[int(y1):int(y2), int(x1):int(x2), :]

                license_plate_crop_gray = cv2.cvtColor(license_plate_crop, cv2.COLOR_BGR2GRAY)
                _, license_plate_crop_thresh = cv2.threshold(license_plate_crop_gray, 64, 255, cv2.THRESH_BINARY_INV)

                license_plate_text, license_plate_text_score = read_license_plate(reader, license_plate_crop_thresh)

                if license_plate_text is not None:
                    print(license_plate_text)
                    yield license_plate_text, time.perf_counter()-t0, license_plate_text_score

    cap.release()
