#!/usr/bin/env python3
"""
Sitemap generator for Valticus Hugo site.
Generates a sitemap.xml based on content files.
"""

import os
import re
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
from typing import List, Tuple
import sys


class SitemapGenerator:
    def __init__(self, base_url: str = "https://valticus.pro/", content_dir: str = "content"):
        self.base_url = base_url.rstrip("/")
        self.content_dir = content_dir
        self.urls: List[Tuple[str, str, float]] = []

    def get_file_mtime(self, filepath: str) -> str:
        """Get file modification time in ISO 8601 format."""
        mtime = os.path.getmtime(filepath)
        return datetime.fromtimestamp(mtime).isoformat() + "+00:00"

    def slugify(self, text: str) -> str:
        """Convert text to a URL-friendly slug."""
        # Convert to lowercase
        text = text.lower()
        # Replace spaces and underscores with dashes
        text = re.sub(r'[\s_]+', '-', text)
        # Remove special characters but keep dashes
        text = re.sub(r'[^a-z0-9-]', '', text)
        # DON'T remove consecutive dashes - Hugo preserves them
        # Strip dashes from start and end
        text = text.strip('-')
        return text

    def get_slug_from_path(self, filepath: str) -> str:
        """Convert file path to URL slug."""
        rel_path = Path(filepath).relative_to(self.content_dir)
        parts = list(rel_path.parts[:-1])  # Remove filename

        if rel_path.name == "index.md":
            # For index.md files, use the parent directory as the slug
            if parts:
                slugged_parts = [self.slugify(p) for p in parts]
                return "/" + "/".join(slugged_parts) + "/"
            else:
                return "/"
        else:
            # For other files, convert filename to slug
            filename = rel_path.stem
            slugged_filename = self.slugify(filename)
            if parts:
                slugged_parts = [self.slugify(p) for p in parts]
                return "/" + "/".join(slugged_parts) + "/" + slugged_filename + "/"
            else:
                return "/" + slugged_filename + "/"

    def scan_content(self):
        """Scan content directory and collect URLs."""
        # Add homepage
        self.urls.append((f"{self.base_url}/", datetime.now().isoformat() + "+00:00", 1.00))

        # Scan all markdown files in content directory
        for root, dirs, files in os.walk(self.content_dir):
            for file in files:
                if file.endswith(".md"):
                    filepath = os.path.join(root, file)
                    slug = self.get_slug_from_path(filepath)
                    url = f"{self.base_url}{slug}"
                    mtime = self.get_file_mtime(filepath)

                    # Determine priority based on location
                    if "posts" in root:
                        priority = 0.80
                    elif "about" in root or "portfolio" in root or "ide-settings" in root:
                        priority = 0.90
                    else:
                        priority = 0.70

                    self.urls.append((url, mtime, priority))

        # Add taxonomy pages (categories and tags) from public directory
        self._add_taxonomy_pages()

    def _add_taxonomy_pages(self):
        """Add taxonomy pages (categories, tags) from public directory."""
        public_dir = "public"
        if not os.path.exists(public_dir):
            return

        now = datetime.now().isoformat() + "+00:00"

        # Scan for category pages
        categories_dir = os.path.join(public_dir, "categories")
        if os.path.exists(categories_dir):
            for item in os.listdir(categories_dir):
                item_path = os.path.join(categories_dir, item)
                # Only add if it's a directory and has an index.html
                if os.path.isdir(item_path) and item != "page":
                    index_html = os.path.join(item_path, "index.html")
                    if os.path.exists(index_html):
                        cat_slug = self.slugify(item)
                        url = f"{self.base_url}/categories/{cat_slug}/"
                        mtime = datetime.fromtimestamp(os.path.getmtime(index_html)).isoformat() + "+00:00"
                        self.urls.append((url, mtime, 0.75))

            # Add main categories page
            categories_index = os.path.join(categories_dir, "index.html")
            if os.path.exists(categories_index):
                url = f"{self.base_url}/categories/"
                mtime = datetime.fromtimestamp(os.path.getmtime(categories_index)).isoformat() + "+00:00"
                self.urls.append((url, mtime, 0.75))

        # Scan for tag pages
        tags_dir = os.path.join(public_dir, "tags")
        if os.path.exists(tags_dir):
            for item in os.listdir(tags_dir):
                item_path = os.path.join(tags_dir, item)
                # Only add if it's a directory and has an index.html
                if os.path.isdir(item_path) and item != "page":
                    index_html = os.path.join(item_path, "index.html")
                    if os.path.exists(index_html):
                        tag_slug = self.slugify(item)
                        url = f"{self.base_url}/tags/{tag_slug}/"
                        mtime = datetime.fromtimestamp(os.path.getmtime(index_html)).isoformat() + "+00:00"
                        self.urls.append((url, mtime, 0.70))

            # Add main tags page
            tags_index = os.path.join(tags_dir, "index.html")
            if os.path.exists(tags_index):
                url = f"{self.base_url}/tags/"
                mtime = datetime.fromtimestamp(os.path.getmtime(tags_index)).isoformat() + "+00:00"
                self.urls.append((url, mtime, 0.70))

    def generate_xml(self) -> str:
        """Generate XML sitemap."""
        urlset = ET.Element("urlset")
        urlset.set("xmlns", "http://www.sitemaps.org/schemas/sitemap/0.9")
        urlset.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
        urlset.set("xsi:schemaLocation",
                   "http://www.sitemaps.org/schemas/sitemap/0.9 "
                   "http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd")

        for url, lastmod, priority in sorted(set(self.urls)):
            url_elem = ET.SubElement(urlset, "url")

            loc = ET.SubElement(url_elem, "loc")
            loc.text = url

            mod = ET.SubElement(url_elem, "lastmod")
            mod.text = lastmod

            prio = ET.SubElement(url_elem, "priority")
            prio.text = f"{priority:.2f}"

        # Pretty print XML
        xml_str = ET.tostring(urlset, encoding='unicode')

        # Format with proper indentation
        import xml.dom.minidom as minidom
        dom = minidom.parseString(xml_str)
        return dom.toprettyxml(indent="  ")

    def save_sitemap(self, output_path: str = "static/sitemap.xml"):
        """Generate and save sitemap to file."""
        self.scan_content()
        xml_content = self.generate_xml()

        # Remove the default XML declaration added by toprettyxml and add our own
        lines = xml_content.split('\n')
        lines = [line for line in lines if line.strip()]  # Remove empty lines
        xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n' + '\n'.join(lines[1:])

        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(xml_content)

        print(f"✓ Sitemap generated: {output_path}")
        print(f"  Total URLs: {len(self.urls)}")


def main():
    """Main entry point."""
    # Read base URL from config.toml
    base_url = "https://valticus.pro/"  # Default fallback

    if os.path.exists("config.toml"):
        try:
            with open("config.toml", "r") as f:
                for line in f:
                    if line.startswith("baseurl"):
                        # Parse: baseurl = "https://valticus.pro/"
                        base_url = line.split("=", 1)[1].strip().strip('"')
                        break
        except Exception as e:
            print(f"Warning: Could not read config.toml: {e}")

    generator = SitemapGenerator(base_url=base_url)
    generator.save_sitemap()
    print("✓ Sitemap generation complete!")


if __name__ == "__main__":
    main()
