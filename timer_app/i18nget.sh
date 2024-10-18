#!/bin/bash

# Ce script recherche les chaînes dans _() et affiche uniquement le texte entre guillemets

# Dossier racine de votre projet
PROJECT_DIR="."

# Expression régulière pour détecter et capturer uniquement les chaînes
REGEX='(?<=_\(")[^"]+(?="\))'

# Recherche récursive dans tous les fichiers du projet, sans afficher les noms des fichiers
echo "Liste des traductions trouvées :"
grep -rh --include="*" -o -P "$REGEX" "$PROJECT_DIR" 2>/dev/null | sort | uniq