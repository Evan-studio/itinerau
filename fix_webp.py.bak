#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import csv
import shutil
from pathlib import Path
try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False
    import subprocess

# Chemins
csv_path = Path('/Users/terrybauer/Documents/site affiliation/itinero/CSV/all_products.csv')
images_base = Path('/Users/terrybauer/Documents/site affiliation/itinero/images/products')

# Produits à traiter
products = {
    '1005008896031548': 4,
    '1005010146019524': 6,
    '1005009173429003': 6,
    '1005007556585645': 6,  # Ajout du produit qui n'affiche pas les 6 images
}

print("🔄 Conversion et renommage des images en WEBP...\n")

# 1. Convertir et renommer les images
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
    
    # Convertir et renommer (limiter à max_images)
    for i, img_file in enumerate(png_files[:max_images], 1):
        new_name = f"image_{i}.webp"
        new_path = product_dir / new_name
        
        try:
            if HAS_PIL:
                # Ouvrir l'image PNG avec PIL
                img = Image.open(img_file)
                # Convertir en RGB si nécessaire (pour RGBA)
                if img.mode in ('RGBA', 'LA', 'P'):
                    rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    rgb_img.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
                    img = rgb_img
                # Sauvegarder en WEBP
                img.save(new_path, 'WEBP', quality=85)
            else:
                # Utiliser sips (macOS) pour convertir
                result = subprocess.run(['sips', '-s', 'format', 'webp', '-s', 'formatOptions', '85', str(img_file), '--out', str(new_path)], 
                                      capture_output=True, text=True)
                if result.returncode != 0:
                    raise Exception(f"sips conversion failed: {result.stderr}")
            
            # Supprimer l'ancien fichier PNG
            if img_file != new_path:
                img_file.unlink()
            
            print(f"✅ {product_id}: {img_file.name} → {new_name}")
        except Exception as e:
            print(f"❌ Erreur pour {img_file.name}: {e}")
    
    print(f"✅ {product_id}: {len(png_files[:max_images])} images converties\n")

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
            # Construire les nouveaux chemins standardisés en WEBP
            new_paths = [f"images/products/{product_id}/image_{i}.webp" for i in range(1, max_images + 1)]
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
    print("\n🎉 Terminé! Les images sont maintenant en WEBP et standardisées.")
else:
    print("❌ Aucun produit mis à jour")
