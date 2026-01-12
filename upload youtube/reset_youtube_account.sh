#!/bin/bash
# Script pour réinitialiser le compte YouTube et le tracking

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "🔄 Réinitialisation du compte YouTube..."
echo ""

# Supprimer le fichier de tracking
if [ -f "$SCRIPT_DIR/upload_tracking.json" ]; then
    rm "$SCRIPT_DIR/upload_tracking.json"
    echo "✅ upload_tracking.json supprimé"
else
    echo "ℹ️  upload_tracking.json n'existe pas"
fi

# Supprimer les credentials pour forcer une nouvelle authentification
if [ -f "$SCRIPT_DIR/credentials.json" ]; then
    rm "$SCRIPT_DIR/credentials.json"
    echo "✅ credentials.json supprimé"
    echo "   → Vous devrez vous ré-authentifier avec la nouvelle chaîne YouTube lors du prochain upload"
else
    echo "ℹ️  credentials.json n'existe pas"
fi

echo ""
echo "✅ Réinitialisation terminée!"
echo ""
echo "📝 Pour changer de chaîne YouTube :"
echo "   1. Assurez-vous d'avoir le fichier client_secret_*.json de la nouvelle chaîne dans ce dossier"
echo "   2. Lancez le script d'upload : python3 auto_upload_videos.py"
echo "   3. Le script vous demandera de vous authentifier avec le nouveau compte YouTube"
echo ""
