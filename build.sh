#!/bin/bash
set -e

echo "=== Building Valticus ==="
echo "Step 1: Building with Hugo..."
hugo --ignoreCache

echo "Step 2: Generating sitemap (overwrite)..."
python3 generate_sitemap.py

# Post-build verification: print the first lines of the generated sitemap for build logs
if [ -f public/sitemap.xml ]; then
	echo "--- public/sitemap.xml (first 30 lines) ---"
	head -n 30 public/sitemap.xml
else
	echo "Warning: public/sitemap.xml not found after build"
fi

echo "=== Build complete ==="
