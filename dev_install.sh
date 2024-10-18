#!/bin/bash

# Fonction pour détecter la plateforme
install_requirements() {
    # Vérifie la plateforme et exécute la commande appropriée
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        sudo pip3 install -r requirements.txt
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        sudo pip3 install -r requirements.txt
    elif [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
        # Windows
        powershell -Command "Start-Process powershell -ArgumentList '-NoExit', '-Command', 'Set-Location -Path \"$PWD\"; pip install -r requirements.txt' -Verb RunAs"

    else
        echo "Système d'exploitation non pris en charge."
        exit 1
    fi
    pause
}

# Exécute l'installation
install_requirements


# Pause finale pour attendre l'interaction de l'utilisateur
read -p "Appuyez sur une touche pour fermer ce script..."