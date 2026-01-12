#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import csv
from pathlib import Path

# Chemin du CSV
csv_path = Path('/Users/terrybauer/Documents/site affiliation/itinero/CSV/all_products.csv')
images_base = Path('/Users/terrybauer/Documents/site affiliation/itinero/images/products')

# Produits à mettre à jour avec leurs images
products_images = {
    '1005008896031548': [
        "Capture d'écran 2026-01-10 à 17.19.42.png",
        "Capture d'écran 2026-01-10 à 17.19.50.png",
        "Capture d'écran 2026-01-10 à 17.19.57.png",
        "Capture d'écran 2026-01-10 à 17.20.04.png"
    ],
    '1005010146019524': [
        "Capture d'écran 2026-01-10 à 17.21.23.png",
        "Capture d'écran 2026-01-10 à 17.21.29.png",
        "Capture d'écran 2026-01-10 à 17.21.35.png",
        "Capture d'écran 2026-01-10 à 17.21.40.png",
        "Capture d'écran 2026-01-10 à 17.21.46.png",
        "Capture d'écran 2026-01-10 à 17.21.51.png"
    ],
    '1005009173429003': [
        "Capture d'écran 2026-01-10 à 17.23.18.png",
        "Capture d'écran 2026-01-10 à 17.23.22.png",
        "Capture d'écran 2026-01-10 à 17.23.28.png",
        "Capture d'écran 2026-01-10 à 17.23.32.png",
        "Capture d'écran 2026-01-10 à 17.23.38.png",
        "Capture d'écran 2026-01-10 à 17.23.43.png"
    ]
}

# Lire le CSV
rows = []
with open(csv_path, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)
    rows.append(header)
    
    # Trouver l'index de la colonne image_paths
    image_paths_idx = None
    for i, col in enumerate(header):
        if 'image' in col.lower() and 'path' in col.lower():
            image_paths_idx = i
            break
    
    if image_paths_idx is None:
        print("❌ Colonne image_paths non trouvée!")
        exit(1)
    
    # Traiter chaque ligne
    updated = 0
    for row in reader:
        product_id = row[0] if row else None
        
        if product_id in products_images:
            # Construire les nouveaux chemins
            new_paths = [f"images/products/{product_id}/{img}" for img in products_images[product_id]]
            row[image_paths_idx] = '|'.join(new_paths)
            updated += 1
            print(f"✅ {product_id}: {len(new_paths)} images")
        
        rows.append(row)

# Écrire le CSV
if updated > 0:
    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)
    print(f"\n✅ {updated} produits mis à jour!")
else:
    print("❌ Aucun produit mis à jour")
