# Petit script pour faire une rotation 'intelligente' d'images d'une structure de dossiers
# zf250809.1641

import cv2
import numpy as np
import os
import argparse
import imutils
from imutils.object_detection import non_max_suppression

def round_to_nearest_90(angle):
    return round(angle / 90) * 90

def detect_orientation(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (17, 7))
    sqKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 21))

    gray = cv2.GaussianBlur(gray, (3, 3), 0)
    blackhat = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, rectKernel)
    grad = cv2.Sobel(blackhat, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=-1)
    grad = np.absolute(grad)
    (minVal, maxVal) = (np.min(grad), np.max(grad))
    grad = (grad - minVal) / (maxVal - minVal)
    grad = (grad * 255).astype("uint8")

    grad = cv2.morphologyEx(grad, cv2.MORPH_CLOSE, rectKernel)
    thresh = cv2.threshold(grad, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, sqKernel)
    thresh = cv2.erode(thresh, None, iterations=2)

    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    angles = []
    for c in cnts:
        rect = cv2.minAreaRect(c)
        angle = rect[-1]
        if angle < -45:
            angle = -(90 + angle)
        else:
            angle = -angle
        angles.append(angle)

    if angles:
        average_angle = np.mean(angles)
        return round_to_nearest_90(average_angle)
    else:
        return 0

def rotate_image(image_path, angle):
    image = cv2.imread(image_path)
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h))
    cv2.imwrite(image_path, rotated)

def process_images(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                image_path = os.path.join(root, file)
                angle = detect_orientation(image_path)
                if angle != 0:
                    print(f"Rotation de {image_path} de {angle} degrés")
                    rotate_image(image_path, angle)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Faire pivoter les images en fonction de l\'orientation du texte.')
    parser.add_argument('path', type=str, help='Chemin du répertoire contenant les images à traiter')
    args = parser.parse_args()

    if os.path.isdir(args.path):
        process_images(args.path)
    else:
        print(f"Le chemin spécifié n'est pas un répertoire valide : {args.path}")
