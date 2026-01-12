#!/bin/bash

# Script pour lancer le serveur HTTP sur le projet itinero

cd "$(dirname "$0")"

echo "🚀 Démarrage du serveur HTTP..."
echo "📍 Répertoire: $(pwd)"
echo ""
echo "🌐 Le serveur sera accessible sur:"
echo "   http://localhost:8000"
echo ""
echo "⚠️  Pour arrêter le serveur, appuyez sur Ctrl+C"
echo ""

# Vérifier si le port 8000 est déjà utilisé
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo "⚠️  Le port 8000 est déjà utilisé."
    echo "   Arrêt du processus existant..."
    kill $(lsof -ti:8000) 2>/dev/null
    sleep 1
fi

# Lancer le serveur Python HTTP
python3 -m http.server 8000
