import glob

import cv2
import numpy as np
from keras.utils import to_categorical
import kagglehub

MODEL_NAME = "model.keras"
NUMBER_OF_CLASSES = 6
BATCH_SIZE = 32
EPOCHS = 50
INDICE_TO_LABEL = {0: "0", 1: "1", 2: "2", 3: "3", 4: "4", 5: "5"}
LABEL_TO_INDICE = {v: k for k, v in INDICE_TO_LABEL.items()}


def process_image(img):
    img = img / 255
    return img


def img_to_sample(img, kernel=None):
    img = img.astype(np.uint8)
    img = np.reshape(img, (128, 128))

    img = process_image(img)

    img = np.reshape(img, (128, 128, 1))
    return img


def download_dataset():
    path = kagglehub.dataset_download("koryakinp/fingers")
    print("Dataset downloaded to", path)

    return path


def load_dataset():
    path = download_dataset()

    train_set = [(file[-6], img_to_sample(cv2.imread(file, 0))) for file in glob.glob(path + "/train/*.png")]
    test_set = [(file[-6], img_to_sample(cv2.imread(file, 0))) for file in glob.glob(path + "/test/*.png")]

    X_train = [t[1] for t in train_set]
    X_train = X_train + X_train[0:6000]
    Y_train = [LABEL_TO_INDICE[t[0]] for t in train_set]
    Y_train = Y_train + Y_train[0:6000]

    X_test = [t[1] for t in test_set]
    X_test = X_test
    Y_test = [LABEL_TO_INDICE[t[0]] for t in test_set]
    Y_test = Y_test

    X_train = np.array(X_train)
    Y_train = to_categorical(Y_train, num_classes=NUMBER_OF_CLASSES)
    X_test = np.array(X_test)
    Y_test = to_categorical(Y_test, num_classes=NUMBER_OF_CLASSES)

    return X_train, Y_train, X_test, Y_test
