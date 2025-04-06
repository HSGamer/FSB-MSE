import os

import cv2
import numpy as np
from deepface import DeepFace

from face import crop_face, apply_transformations

DIR = "faces"
if not os.path.exists(DIR):
    os.makedirs(DIR)

KNOWN_FACES = {}


def save_face(name, image_name, image):
    """
    Save a face image to the dataset.
    """
    image_path = f"{DIR}/{name}/{image_name}"
    if not os.path.exists(f"{DIR}/{name}"):
        os.makedirs(f"{DIR}/{name}")
    image.save(image_path)
    return image_path


def encode_face(image):
    """
    Encode a face image into a vector.
    """
    encodings = DeepFace.represent(image, model_name="Dlib", detector_backend="skip", max_faces=1)
    if len(encodings) == 0:
        return None
    return encodings[0]['embedding']


def add_new_face(name, image):
    """
    Add a new face to the dataset.
    """
    face_image = crop_face(image)
    if face_image is None:
        return False

    face_variations = apply_transformations(face_image)
    face_variations.append(face_image)

    if not os.path.exists(f"{DIR}/{name}"):
        os.makedirs(f"{DIR}/{name}")

    for i, img in enumerate(face_variations):
        image_name = f"{name}_{i}.jpg"
        cv2.imwrite(f"{DIR}/{name}/{image_name}", img)

    face_encodings = [encode_face(face) for face in face_variations]
    KNOWN_FACES[name] = face_encodings
    return True


def face_distance(image):
    """
    Calculate the Euclidean distance between the given face image and known faces.
    """
    encoding = encode_face(image)
    if encoding is None:
        return None

    distances = {}
    for name, encodings in KNOWN_FACES.items():
        min_distance = float('inf')
        for known_encoding in encodings:
            distance = np.linalg.norm(np.array(encoding) - np.array(known_encoding))
            if distance < min_distance:
                min_distance = distance
        distances[name] = min_distance

    return distances


def guess_face(image):
    """
    Guess the name of the person in the image.
    """
    distances = face_distance(image)
    if distances is None or len(distances) == 0:
        return None

    closest_name = min(distances, key=distances.get)
    closest_name_distance = distances[closest_name]
    return closest_name, closest_name_distance


def load_dataset():
    """
    Load the dataset from the directory.
    """
    for name in os.listdir(DIR):
        if os.path.isdir(f"{DIR}/{name}"):
            encodings = []
            for image_name in os.listdir(f"{DIR}/{name}"):
                image_path = f"{DIR}/{name}/{image_name}"
                image = cv2.imread(image_path, cv2.IMREAD_COLOR)
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                encoding = encode_face(image)
                if encoding is not None:
                    print(f"Loaded {image_path}")
                    encodings.append(encoding)

            KNOWN_FACES[name] = encodings
