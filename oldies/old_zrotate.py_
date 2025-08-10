# Petit script pour faire une rotation 'intelligente' d'images d'une structure de dossiers
# zf250809.1556

import cv2
import os
import argparse

def is_landscape(image_path):
    # Load the image
    image = cv2.imread(image_path)
    h, w = image.shape[:2]
    return w > h

def rotate_image(image_path, angle):
    image = cv2.imread(image_path)
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)

    # Calculate the new bounding dimensions of the image
    if angle == 90 or angle == 270:
        new_w, new_h = h, w
    else:
        new_w, new_h = w, h

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
                if is_landscape(image_path):
                    angle = 180
                else:
                    angle = 90
                print(f"Rotation de {image_path} de {angle} degrés")
                rotate_image(image_path, angle)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Faire pivoter les images en fonction de leur format.')
    parser.add_argument('path', type=str, help='Chemin du répertoire contenant les images à traiter')
    args = parser.parse_args()

    if os.path.isdir(args.path):
        process_images(args.path)
    else:
        print(f"Le chemin spécifié n'est pas un répertoire valide : {args.path}")
