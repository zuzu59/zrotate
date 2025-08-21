# Petit script pour parcourir toute une structure de dossiers et indiquer l'orientation de chaque image
# zf250821.2336

#!/bin/bash

# Vérifier si ImageMagick est installé
if ! command -v convert &> /dev/null; then
    echo "ImageMagick n'est pas installé. Installation en cours..."
    sudo apt update
    sudo apt install imagemagick -y
fi

# Parcourir récursivement tous les fichiers dans le répertoire courant
find .. -type f \( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" -o -iname "*.gif" -o -iname "*.bmp" \) | while read file; do
#    echo "Orientation de l'image : $file"
    # Utiliser convert pour faire pivoter l'image de 180 degrés
#    convert "$file" -rotate 180 "$file"
    orientation=$(file "$file" |grep orient | awk -F'orientation=' '{print $2}' | awk -F',' '{print $1}')
    echo -e "$file: $orientation"
done

echo "Toutes les images ont été pivotées de 180 degrés."



