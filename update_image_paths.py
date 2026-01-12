#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import os
from pathlib import Path

# Définir les chemins
script_dir = Path(__file__).parent
csv_path = script_dir / 'CSV' / 'all_products.csv'
images_base = script_dir / 'images' / 'products'

# Produits à mettre à jour
products_to_update = {
    '1005008896031548': None,  # Sera rempli avec les fichiers trouvés
    '1005010146019524': None,
    '1005009173429003': None,
}

# Récupérer les fichiers images pour chaque produit
for product_id in products_to_update.keys():
    product_dir = images_base / product_id
    if product_dir.exists() and product_dir.is_dir():
        # Lister les fichiers images (png, jpg, jpeg, webp)
        image_files = sorted([
            f.name for f in product_dir.iterdir()
            if f.is_file() and f.suffix.lower() in ['.png', '.jpg', '.jpeg', '.webp']
        ])
        if image_files:
            # Limiter à 6 images et inverser l'ordre pour avoir les plus récentes en premier (si triées par date)
            # Les fichiers sont déjà triés par ordre alphabétique (du plus ancien au plus récent)
            # On les inverse pour avoir les plus récentes en premier
            image_files_reversed = list(reversed(image_files))
            products_to_update[product_id] = image_files_reversed[:6]
            print(f"✅ {product_id}: {len(image_files)} images trouvées, {len(products_to_update[product_id])} utilisées")
            for i, img in enumerate(products_to_update[product_id], 1):
                print(f"   {i}. {img}")
        else:
            print(f"⚠️  {product_id}: Dossier vide ou aucune image")
    else:
        print(f"❌ {product_id}: Dossier non trouvé")

# Lire le CSV
print(f"\n📖 Lecture du CSV: {csv_path}")
rows = []
updated_count = 0

with open(csv_path, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)
    rows.append(header)
    
    # Trouver l'index de la colonne image_paths (normalement index 7)
    image_paths_idx = None
    for i, col in enumerate(header):
        if 'image' in col.lower() and 'path' in col.lower():
            image_paths_idx = i
            break
    
    if image_paths_idx is None:
        print("❌ Colonne image_paths non trouvée dans le CSV!")
        exit(1)
    
    print(f"📋 Colonne image_paths à l'index: {image_paths_idx}")
    
    # Traiter chaque ligne
    for row in reader:
        product_id = row[0] if row else None
        
        if product_id in products_to_update and products_to_update[product_id]:
            # Construire les nouveaux chemins relatifs
            new_paths = []
            for img_file in products_to_update[product_id]:
                # Chemin relatif depuis la racine du projet
                rel_path = f"images/products/{product_id}/{img_file}"
                new_paths.append(rel_path)
            
            # Mettre à jour la colonne image_paths (séparée par |)
            row[image_paths_idx] = '|'.join(new_paths)
            updated_count += 1
            print(f"✅ Mis à jour: {product_id} avec {len(new_paths)} images")
            print(f"   Chemins: {new_paths[0]} ... {new_paths[-1] if len(new_paths) > 1 else ''}")
        
        rows.append(row)

# Écrire le CSV mis à jour
if updated_count > 0:
    print(f"\n💾 Écriture du CSV mis à jour...")
    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)
    print(f"✅ {updated_count} produits mis à jour dans le CSV!")
else:
    print("⚠️  Aucun produit mis à jour")
