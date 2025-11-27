#!/bin/bash
set -e

echo "=== Building Valticus ==="
echo "Step 1: Building with Hugo..."
hugo

echo "Step 2: Generating sitemap (overwrite)..."
python3 generate_sitemap.py

echo "=== Build complete ==="
