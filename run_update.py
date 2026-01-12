#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import subprocess
import sys

# Exécuter le script update_image_paths.py
result = subprocess.run([sys.executable, 'update_image_paths.py'], 
                       cwd='/Users/terrybauer/Documents/site affiliation/itinero',
                       capture_output=True, text=True, encoding='utf-8')

print(result.stdout)
if result.stderr:
    print(result.stderr, file=sys.stderr)
sys.exit(result.returncode)
