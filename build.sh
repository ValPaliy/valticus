#!/bin/bash
set -e

echo "=== Building Valticus ==="
echo "Step 1: Generating sitemap..."
python3 generate_sitemap.py

echo "Step 2: Building with Hugo..."
hugo

echo "=== Build complete ==="
