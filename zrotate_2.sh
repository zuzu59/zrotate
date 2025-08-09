# Petit script pour faire une rotation d'images d'une structure de dossiers en fonction de son format portrait (90°) ou paysage (180°)
# zf250809.1806

#!/bin/bash

# Vérifier si un chemin a été fourni
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <path_to_images>"
    exit 1
fi

# Chemin vers le dossier contenant les images
path_to_images="$1"

# Fonction pour faire tourner les images en fonction de leur orientation
rotate_images() {
    # Parcourir tous les fichiers dans le répertoire et ses sous-répertoires
    find "$path_to_images" -type f \( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" \) | while read img; do
        # Obtenir l'orientation de l'image
        orientation=$(identify -verbose "$img" 2>/dev/null | grep -i "Orientation:" | awk '{print $2}')

        # Faire tourner l'image en fonction de son orientation
        case "$orientation" in
            "RightTop") # Portrait
                echo "Rotation de $img de 90 degrés"
                convert "$img" -rotate 90 "$img"
                ;;
            "LeftTop") # Paysage
                echo "Rotation de $img de 180 degrés"
                convert "$img" -rotate 180 "$img"
                ;;
            *)
                echo "Aucune rotation nécessaire pour $img"
                ;;
        esac
    done
}

# Appeler la fonction pour faire tourner les images
rotate_images
