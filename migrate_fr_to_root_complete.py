#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script complet de migration: Déplacer le contenu français de /fr vers la racine,
supprimer le contenu anglais, et mettre à jour le sitemap.

ATTENTION: Cette opération est irréversible. Une sauvegarde sera créée.
"""
import shutil
import sys
import subprocess
from pathlib import Path
from datetime import datetime
import re

BASE_DIR = Path('/Users/terrybauer/Documents/site affiliation/itinero')
FR_DIR = BASE_DIR / 'fr'
BACKUP_DIR = BASE_DIR / 'sauv' / f'migration_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}'

# Fichiers/dossiers à déplacer de /fr vers la racine
ITEMS_TO_MOVE = [
    'CSV',
    'scripts',
    'page_html',
    'index.html',
    'translations.csv',
    'sitemap.xml',
    'robots.txt',
    'custom.css',
    'upload youtube',
]

# Fichiers/dossiers anglais à supprimer (si existent)
ITEMS_TO_REMOVE = [
    'CSV',
    'scripts',
    'page_html',
    'index.html',
    'translations.csv',
]

def create_backup():
    """Crée une sauvegarde complète."""
    print("📦 Création de la sauvegarde...")
    try:
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)
        
        # Sauvegarder les fichiers à la racine qui seront remplacés
        for item in ITEMS_TO_REMOVE:
            src = BASE_DIR / item
            if src.exists():
                dst = BACKUP_DIR / f'root_{item}'
                if src.is_dir():
                    shutil.copytree(src, dst, dirs_exist_ok=True)
                else:
                    shutil.copy2(src, dst)
                print(f"  ✅ Sauvegardé: {item}")
        
        # Sauvegarder le dossier /fr
        if FR_DIR.exists():
            dst = BACKUP_DIR / 'fr'
            shutil.copytree(FR_DIR, dst, dirs_exist_ok=True)
            print(f"  ✅ Sauvegardé: /fr")
        
        print(f"✅ Sauvegarde créée: {BACKUP_DIR}")
        return True
    except Exception as e:
        print(f"❌ Erreur lors de la sauvegarde: {e}")
        return False

def remove_english_content():
    """Supprime le contenu anglais à la racine."""
    print("🗑️  Suppression du contenu anglais...")
    errors = []
    for item in ITEMS_TO_REMOVE:
        src = BASE_DIR / item
        if src.exists():
            try:
                if src.is_dir():
                    shutil.rmtree(src)
                else:
                    src.unlink()
                print(f"  ✅ Supprimé: {item}")
            except Exception as e:
                error_msg = f"Erreur lors de la suppression de {item}: {e}"
                errors.append(error_msg)
                print(f"  ⚠️  {error_msg}")
    return len(errors) == 0

def move_french_content():
    """Déplace le contenu français de /fr vers la racine."""
    print("📦 Déplacement du contenu français vers la racine...")
    errors = []
    for item in ITEMS_TO_MOVE:
        src = FR_DIR / item
        if src.exists():
            dst = BASE_DIR / item
            try:
                if src.is_dir():
                    if dst.exists():
                        shutil.rmtree(dst)
                    shutil.copytree(src, dst)
                else:
                    if dst.exists():
                        dst.unlink()
                    shutil.copy2(src, dst)
                print(f"  ✅ Déplacé: {item}")
            except Exception as e:
                error_msg = f"Erreur lors du déplacement de {item}: {e}"
                errors.append(error_msg)
                print(f"  ❌ {error_msg}")
        else:
            print(f"  ⚠️  Non trouvé dans /fr: {item}")
    return len(errors) == 0

def update_sitemap_script():
    """Met à jour generate_sitemaps.py pour générer sitemap.xml au lieu de sitemap-en.xml."""
    print("📝 Mise à jour de generate_sitemaps.py...")
    sitemap_script = BASE_DIR / 'generate_sitemaps.py'
    
    if not sitemap_script.exists():
        print(f"  ⚠️  Script non trouvé: {sitemap_script}")
        return False
    
    try:
        content = sitemap_script.read_text(encoding='utf-8')
        original_content = content
        
        # Après la migration, la racine contient le français (pas l'anglais)
        # On veut générer sitemap.xml directement (pas sitemap-en.xml)
        # et le sitemap index doit référencer sitemap.xml (pas sitemap-en.xml et sitemap-fr.xml)
        
        # Changer sitemap-en.xml en sitemap.xml pour la racine
        content = re.sub(
            r"sitemap-en\.xml",
            r"sitemap.xml",
            content
        )
        
        # Le script génère déjà correctement les URLs pour la racine (sans /fr/)
        # Après la migration, find_language_directories() retournera une liste vide
        # donc le script générera seulement pour la racine
        
        # Modifier le sitemap index pour qu'il génère directement sitemap.xml
        # au lieu de référencer plusieurs langues
        
        if content != original_content:
            sitemap_script.write_text(content, encoding='utf-8')
            print("  ✅ Script mis à jour (sitemap-en.xml -> sitemap.xml)")
            return True
        else:
            print("  ℹ️  Aucune modification nécessaire")
            return True
    except Exception as e:
        print(f"  ❌ Erreur lors de la mise à jour: {e}")
        return False

def regenerate_sitemap():
    """Régénère le sitemap."""
    print("🗺️  Régénération du sitemap...")
    sitemap_script = BASE_DIR / 'generate_sitemaps.py'
    
    if not sitemap_script.exists():
        print(f"  ⚠️  Script non trouvé: {sitemap_script}")
        return False
    
    try:
        result = subprocess.run(
            [sys.executable, str(sitemap_script)],
            cwd=str(BASE_DIR),
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        
        if result.returncode == 0:
            print(result.stdout)
            print("  ✅ Sitemap régénéré")
            return True
        else:
            print("  ⚠️  Erreurs lors de la génération:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"  ❌ Erreur lors de l'exécution: {e}")
        return False

def main():
    """Fonction principale."""
    print("=" * 70)
    print("🚀 MIGRATION COMPLÈTE: FRANÇAIS VERS LA RACINE")
    print("=" * 70)
    print()
    print("⚠️  ATTENTION: Cette opération va:")
    print("   1. Créer une sauvegarde complète")
    print("   2. Supprimer le contenu anglais à la racine")
    print("   3. Déplacer le contenu de /fr vers la racine")
    print("   4. Mettre à jour generate_sitemaps.py")
    print("   5. Régénérer le sitemap")
    print()
    print("❌ Cette opération est IRRéVERSIBLE!")
    print()
    
    response = input("Voulez-vous continuer? (oui/non): ").strip().lower()
    if response not in ['oui', 'o', 'yes', 'y']:
        print("❌ Opération annulée.")
        sys.exit(0)
    
    print()
    print("🔧 Début de la migration...")
    print()
    
    # 1. Sauvegarde
    if not create_backup():
        print("❌ Erreur lors de la sauvegarde. Arrêt.")
        sys.exit(1)
    
    print()
    
    # 2. Supprimer le contenu anglais
    if not remove_english_content():
        print("⚠️  Des erreurs sont survenues lors de la suppression.")
        response = input("Voulez-vous continuer quand même? (oui/non): ").strip().lower()
        if response not in ['oui', 'o', 'yes', 'y']:
            print("❌ Opération annulée.")
            sys.exit(1)
    
    print()
    
    # 3. Déplacer le contenu français
    if not move_french_content():
        print("❌ Erreur lors du déplacement. Arrêt.")
        sys.exit(1)
    
    print()
    print("✅ Migration des fichiers terminée!")
    print()
    
    # 4. Mettre à jour le script sitemap
    if not update_sitemap_script():
        print("⚠️  Erreur lors de la mise à jour du script sitemap.")
    
    print()
    
    # 5. Régénérer le sitemap
    if not regenerate_sitemap():
        print("⚠️  Erreur lors de la régénération du sitemap.")
        print("   Vous pouvez le régénérer manuellement avec: python3 generate_sitemaps.py")
    
    print()
    print("=" * 70)
    print("✅ MIGRATION TERMINÉE!")
    print("=" * 70)
    print()
    print(f"💾 Sauvegarde disponible dans: {BACKUP_DIR}")
    print()
    print("📝 Prochaines étapes:")
    print("   1. Vérifier que tout fonctionne correctement")
    print("   2. Tester le site localement")
    print("   3. Régénérer les pages si nécessaire")
    print()

if __name__ == '__main__':
    main()
