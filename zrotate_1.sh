# Petit script pour faire une rotation d'images d'une structure de dossiers
# zf250809.1454

#!/bin/bash

# Vérifier si ImageMagick est installé
if ! command -v convert &> /dev/null; then
    echo "ImageMagick n'est pas installé. Installation en cours..."
    sudo apt update
    sudo apt install imagemagick -y
fi

# Parcourir récursivement tous les fichiers dans le répertoire courant
find .. -type f \( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" -o -iname "*.gif" -o -iname "*.bmp" \) | while read file; do
    echo "Rotation de l'image : $file"
    # Utiliser convert pour faire pivoter l'image de 180 degrés
    convert "$file" -rotate 180 "$file"
done

echo "Toutes les images ont été pivotées de 180 degrés."



