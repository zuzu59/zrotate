# Petit script pour faire une rotation 180° ou 270° d'images d'une structure de dossiers en fonction de sa location et de son format portrait ou paysage
# zf250821.1224

#!/bin/bash




echo "Nom du script : $0"
echo "Répertoire du script : $(dirname $0)"
echo "Répertoire de l'appel : $(pwd)"




# Vérification du nombre d'arguments
if [ "$#" -ne 1 ]; then
    echo "Usage : $0 <chemin_de_racine>"
    exit 1
fi

ROOT_DIR="$1"

# Vérification que le chemin existe
if [ ! -d "$ROOT_DIR" ]; then
    echo "Le dossier $ROOT_DIR n'existe pas."
    exit 1
fi


execute_script() {
    local dir="$1"
    local script_name="$2"
        zSCRIPT=$(pwd)/$script_name
	echo "Exécution de $zSCRIPT dans $dir"
        $zSCRIPT "$dir"
}

# Dossiers pour toto.sh
echo "Lancement de toto.sh dans :"
for dir in "$ROOT_DIR"/01A "$ROOT_DIR"/02 "$ROOT_DIR"/03 "$ROOT_DIR"/04 "$ROOT_DIR"/05A "$ROOT_DIR"/06; do
    if [ -d "$dir" ]; then
        execute_script "$dir" "zrotate_01_06.sh"
    fi
done

# Dossiers pour tutu.sh
echo "Lancement de tutu.sh dans :"
for dir in "$ROOT_DIR"/07B/impaires "$ROOT_DIR"/08B/impaires "$ROOT_DIR"/09B/impaires; do
    if [ -d "$dir" ]; then
        execute_script "$dir" "zrotate_impaire.sh"
    fi
done

# Dossiers pour titi.sh
echo "Lancement de titi.sh dans :"
for dir in "$ROOT_DIR"/07B/paires "$ROOT_DIR"/08B/paires "$ROOT_DIR"/09B/paires; do
    if [ -d "$dir" ]; then
        execute_script "$dir" "zrotate_paire.sh"
    fi
done



