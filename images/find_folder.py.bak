#!/usr/bin/env python3
"""
Script pour trouver et ouvrir un dossier produit par son product_id
"""

import os
import subprocess
import sys
from pathlib import Path

def find_and_open_folder(product_id):
    """Trouve et ouvre un dossier produit par son product_id."""
    
    try:
        # Obtenir le chemin du script actuel (qui est dans images/)
        script_file = Path(__file__).resolve()
        # Le script est dans images/, donc le dossier parent est itinero/
        itinero_dir = script_file.parent.parent
        # Le bon chemin est : images/products/{product_id}
        images_dir = itinero_dir / 'images' / 'products'
        images_dir = images_dir.resolve()
        
        # Chemin du dossier produit
        product_dir = images_dir / str(product_id)
        
        if product_dir.exists():
            print(f"✅ Dossier trouvé : {product_dir}")
            
            # Ouvrir le dossier dans Finder
            try:
                subprocess.run(['open', str(product_dir)], check=True)
                print(f"✅ Dossier ouvert dans Finder")
            except Exception as e:
                print(f"⚠️  Impossible d'ouvrir automatiquement : {str(e)}")
                print(f"💡 Ouvrez manuellement : {product_dir}")
            
            return str(product_dir)
        else:
            print(f"❌ Dossier non trouvé pour le product_id : {product_id}")
            print(f"📁 Chemin recherché : {product_dir}")
            
            # Chercher dans d'autres emplacements possibles
            print(f"\n🔍 Recherche dans d'autres emplacements...")
            
            # Chercher dans le dossier itinero et ses sous-dossiers
            parent_dir = itinero_dir
            found = False
            
            for root, dirs, files in os.walk(parent_dir):
                # Ignorer certains dossiers pour accélérer la recherche
                dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__', 'node_modules', 'dist']]
                
                if str(product_id) in dirs:
                    found_path = Path(root) / str(product_id)
                    print(f"✅ Trouvé : {found_path}")
                    
                    try:
                        subprocess.run(['open', str(found_path)], check=True)
                        print(f"✅ Dossier ouvert dans Finder")
                        found = True
                        return str(found_path)
                    except Exception as e:
                        print(f"💡 Ouvrez manuellement : {found_path}")
                        found = True
                        return str(found_path)
            
            if not found:
                print(f"❌ Dossier introuvable dans : {parent_dir}")
            
            return None
            
    except Exception as e:
        print(f"❌ Erreur : {str(e)}")
        import traceback
        traceback.print_exc()
        return None

def main():
    """Fonction principale."""
    print("🔍 RECHERCHE DE DOSSIER PRODUIT")
    print("=" * 60)
    
    # Si un argument est fourni en ligne de commande
    if len(sys.argv) > 1:
        product_id = sys.argv[1].strip()
        print(f"📁 Recherche du dossier : {product_id}\n")
        find_and_open_folder(product_id)
    else:
        # Mode interactif
        while True:
            print("\n" + "=" * 60)
            product_id = input("📝 Entrez le product_id (ou 'q' pour quitter) : ").strip()
            
            if product_id.lower() in ['q', 'quit', 'exit']:
                print("👋 Au revoir!")
                break
            
            if not product_id:
                print("⚠️  Veuillez entrer un product_id")
                continue
            
            print()
            find_and_open_folder(product_id)

if __name__ == "__main__":
    main()
