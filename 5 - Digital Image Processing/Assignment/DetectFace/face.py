import random

import cv2
from mtcnn import MTCNN

detector = MTCNN()


def detect_faces(image):
    """
    Detects faces in an image using MTCNN.
    :param image: Input image in BGR format.
    :return:
    """
    detections = detector.detect_faces(image)
    if not detections:
        return None

    boxes = []
    for detection in detections:
        boxes.append(detection['box'])

    return boxes


def crop_face(image):
    """
    Detects and tightly crops the face from an image.
    """
    detections = detect_faces(image)

    if detections:
        x, y, w, h = detections[0]
        face = image[y:y + h, x:x + w]

        # Ensure tight cropping with no extra borders
        face = remove_black_background(face)

        return face
    return None


def remove_black_background(image):
    """
    Removes black background and trims edges.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    _, mask = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)

    # Find contours and bounding box of the non-black area
    coords = cv2.findNonZero(mask)
    x, y, w, h = cv2.boundingRect(coords)

    # Crop to bounding box
    cropped = image[y:y + h, x:x + w]
    return cropped


def apply_transformations(image, num_variations=10):
    """
    Generates multiple variations of the face image.
    """
    processed_images = []
    h, w = image.shape[:2]

    for _ in range(num_variations):
        transformed = image.copy()

        # Random rotation (-30 to +30 degrees)
        angle = random.randint(-30, 30)
        matrix = cv2.getRotationMatrix2D((w // 2, h // 2), angle, 1)
        transformed = cv2.warpAffine(transformed, matrix, (w, h))

        # Random flip
        if random.choice([True, False]):
            transformed = cv2.flip(transformed, 1)

        # Random brightness/contrast
        alpha = random.uniform(0.7, 1.3)
        beta = random.randint(-40, 40)
        transformed = cv2.convertScaleAbs(transformed, alpha=alpha, beta=beta)

        # Gaussian blur
        if random.choice([True, False]):
            kernel_size = random.choice([(3, 3), (5, 5)])
            transformed = cv2.GaussianBlur(transformed, kernel_size, 0)

        # Remove any remaining black borders
        transformed = remove_black_background(transformed)

        processed_images.append(transformed)

    return processed_images
