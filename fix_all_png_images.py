#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour convertir TOUS les PNG en WEBP et standardiser les noms
pour tous les produits qui ont des images PNG
"""
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

print("🔍 Recherche de tous les produits avec des images PNG...\n")

# 1. Trouver tous les produits avec des PNG
products_with_png = {}
for product_dir in images_base.iterdir():
    if not product_dir.is_dir():
        continue
    
    product_id = product_dir.name
    png_files = sorted([f for f in product_dir.iterdir() if f.is_file() and f.suffix.lower() == '.png'])
    
    if png_files:
        # Limiter à 6 images max
        products_with_png[product_id] = min(len(png_files), 6)
        print(f"✅ {product_id}: {len(png_files)} PNG trouvées")

print(f"\n📊 Total: {len(products_with_png)} produits avec des PNG à convertir\n")

if not products_with_png:
    print("✅ Aucun produit avec PNG trouvé!")
    exit(0)

print("🔄 Conversion et renommage des images en WEBP...\n")

# 2. Convertir et renommer les images
for product_id, max_images in products_with_png.items():
    product_dir = images_base / product_id
    
    # Lister les fichiers PNG triés
    png_files = sorted([f for f in product_dir.iterdir() if f.is_file() and f.suffix.lower() == '.png'])
    
    # Convertir et renommer (limiter à max_images)
    converted = 0
    for i, img_file in enumerate(png_files[:max_images], 1):
        new_name = f"image_{i}.webp"
        new_path = product_dir / new_name
        
        # Vérifier si le fichier WEBP existe déjà
        if new_path.exists():
            print(f"  ⚠️  {product_id}: {new_name} existe déjà, on passe")
            continue
        
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
            
            converted += 1
            print(f"  ✅ {product_id}: {img_file.name} → {new_name}")
        except Exception as e:
            print(f"  ❌ {product_id}: Erreur pour {img_file.name}: {e}")
    
    if converted > 0:
        print(f"✅ {product_id}: {converted} images converties\n")

# 3. Mettre à jour le CSV
print("📝 Mise à jour du CSV...\n")
rows = []
with open(csv_path, 'r', encoding='utf-8') as f:
    # Détecter le délimiteur
    first_line = f.readline()
    f.seek(0)
    delimiter = ';' if ';' in first_line and first_line.count(';') > first_line.count(',') else ','
    reader = csv.reader(f, delimiter=delimiter)
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
        
        if product_id in products_with_png:
            max_images = products_with_png[product_id]
            # Construire les nouveaux chemins standardisés en WEBP
            new_paths = [f"images/products/{product_id}/image_{i}.webp" for i in range(1, max_images + 1)]
            row[image_paths_idx] = '|'.join(new_paths)
            updated += 1
            print(f"✅ {product_id}: {len(new_paths)} chemins mis à jour")
        
        rows.append(row)

# Écrire le CSV
if updated > 0:
    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, delimiter=delimiter)
        writer.writerows(rows)
    print(f"\n✅ {updated} produits mis à jour dans le CSV!")
    print("\n🎉 Terminé! Toutes les images PNG sont maintenant en WEBP et standardisées.")
    print("\n💡 Maintenant, régénérez les pages:")
    print("   python3 generate_all_languages_with_domain_update.py")
else:
    print("⚠️  Aucun produit mis à jour dans le CSV")
