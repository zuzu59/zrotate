# Petit script pour faire une rotation 'intelligente' d'images d'une structure de dossiers
# zf250809.1556

import cv2
import numpy as np
import os
import argparse

def is_landscape(image):
    h, w = image.shape[:2]
    return w > h

def detect_orientation(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Check if the image is landscape
    if is_landscape(image):
        # For landscape images, check if it needs a 180-degree rotation
        # This is a simple heuristic and might need adjustments
        # Here, we check the intensity distribution
        top_half_intensity = np.mean(gray[:gray.shape[0]//2, :])
        bottom_half_intensity = np.mean(gray[gray.shape[0]//2:, :])
        if bottom_half_intensity > top_half_intensity:
            return 180

    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Use Canny edge detection
    edges = cv2.Canny(blurred, 50, 150, apertureSize=3)

    # Detect lines using Hough Line Transform
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=100, minLineLength=100, maxLineGap=10)

    if lines is not None:
        angles = []
        for line in lines:
            x1, y1, x2, y2 = line[0]
            angle = np.degrees(np.arctan2(y2 - y1, x2 - x1))
            angles.append(angle)

        if angles:
            average_angle = np.mean(angles)
            if average_angle < -45:
                return 270
            elif -45 <= average_angle <= 45:
                return 0
            else:
                return 90
    return 0

def rotate_image(image_path, angle):
    image = cv2.imread(image_path)
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)

    # Calculate the new bounding dimensions of the image
    abs_cos = abs(np.cos(np.radians(angle)))
    abs_sin = abs(np.sin(np.radians(angle)))
    new_w = int(h * abs_sin + w * abs_cos)
    new_h = int(h * abs_cos + w * abs_sin)

    # Adjust the rotation matrix to take into account translation
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    M[0, 2] += (new_w - w) / 2
    M[1, 2] += (new_h - h) / 2

    # Perform the rotation
    rotated = cv2.warpAffine(image, M, (new_w, new_h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
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
