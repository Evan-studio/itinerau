#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import csv
import shutil
from pathlib import Path

# Chemins
csv_path = Path('/Users/terrybauer/Documents/site affiliation/itinero/CSV/all_products.csv')
images_base = Path('/Users/terrybauer/Documents/site affiliation/itinero/images/products')

# Produits à traiter
products = {
    '1005008896031548': 4,
    '1005010146019524': 6,
    '1005009173429003': 6,
}

print("🔄 Renommage des images et mise à jour du CSV...\n")

# 1. Renommer les images dans les dossiers
for product_id, max_images in products.items():
    product_dir = images_base / product_id
    if not product_dir.exists():
        print(f"❌ Dossier non trouvé: {product_dir}")
        continue
    
    # Lister les fichiers PNG triés
    png_files = sorted([f for f in product_dir.iterdir() if f.is_file() and f.suffix.lower() == '.png'])
    
    if not png_files:
        print(f"❌ Aucune image PNG trouvée pour {product_id}")
        continue
    
    # Renommer les images (limiter à max_images)
    for i, img_file in enumerate(png_files[:max_images], 1):
        new_name = f"image_{i}.png"
        new_path = product_dir / new_name
        if img_file != new_path:
            shutil.move(str(img_file), str(new_path))
            print(f"✅ {product_id}: {img_file.name} → {new_name}")
    
    print(f"✅ {product_id}: {len(png_files[:max_images])} images renommées\n")

# 2. Mettre à jour le CSV
print("📝 Mise à jour du CSV...\n")
rows = []
with open(csv_path, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)
    rows.append(header)
    
    # Trouver l'index de image_paths
    image_paths_idx = None
    for i, col in enumerate(header):
        if 'image' in col.lower() and 'path' in col.lower():
            image_paths_idx = i
            break
    
    if image_paths_idx is None:
        print("❌ Colonne image_paths non trouvée!")
        exit(1)
    
    updated = 0
    for row in reader:
        product_id = row[0] if row else None
        
        if product_id in products:
            max_images = products[product_id]
            # Construire les nouveaux chemins standardisés
            new_paths = [f"images/products/{product_id}/image_{i}.png" for i in range(1, max_images + 1)]
            row[image_paths_idx] = '|'.join(new_paths)
            updated += 1
            print(f"✅ {product_id}: {len(new_paths)} chemins mis à jour")
        
        rows.append(row)

# Écrire le CSV
if updated > 0:
    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)
    print(f"\n✅ {updated} produits mis à jour dans le CSV!")
    print("\n🎉 Terminé! Les images sont maintenant standardisées.")
else:
    print("❌ Aucun produit mis à jour")
