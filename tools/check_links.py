import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import concurrent.futures
import sys

# Configuration
PUBLIC_DIR = os.path.join(os.getcwd(), 'public')
IGNORE_DOMAINS = ['linkedin.com', 'twitter.com', 'facebook.com', 'instagram.com', 'localhost']
IGNORE_PREFIXES = ['mailto:', 'tel:', '#']

def is_external(url):
    return bool(urlparse(url).netloc)

def check_external_link(url):
    if any(domain in url for domain in IGNORE_DOMAINS):
        return url, "Ignored", None

    try:
        response = requests.head(url, allow_redirects=True, timeout=5)
        if response.status_code >= 400:
            # Retry with GET as some servers deny HEAD
            response = requests.get(url, allow_redirects=True, timeout=5)

        if response.status_code >= 400:
            return url, "Broken", response.status_code
        return url, "OK", response.status_code
    except requests.RequestException as e:
        return url, "Error", str(e)

def check_internal_link(filepath, link):
    # Remove anchor for file check
    link_path = link.split('#')[0]
    anchor = link.split('#')[1] if '#' in link else None

    if not link_path:
        # Just an anchor on the same page
        return True # TODO: validate anchor existence in the same file

    # Absolute path relative to site root
    if link_path.startswith('/'):
        target_path = os.path.join(PUBLIC_DIR, link_path.lstrip('/'))
    else:
        # Relative path
        target_path = os.path.join(os.path.dirname(filepath), link_path)

    # If it's a directory, look for index.html
    if os.path.isdir(target_path):
        target_path = os.path.join(target_path, 'index.html')
    elif not os.path.exists(target_path) and os.path.exists(target_path + '/index.html'):
         target_path = target_path + '/index.html'

    if not os.path.exists(target_path):
        return False

    return True

def process_file(filepath):
    broken_links = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')

        for a in soup.find_all('a', href=True):
            href = a['href']

            if any(href.startswith(p) for p in IGNORE_PREFIXES):
                continue

            if is_external(href):
                # We will collect external links to check them in batch or parallel later?
                # For now let's just return them to be checked
                pass
            else:
                if not check_internal_link(filepath, href):
                    broken_links.append((href, "Internal Link Not Found"))

    except Exception as e:
        print(f"Error processing {filepath}: {e}")

    return broken_links, soup

def main():
    print(f"Scanning {PUBLIC_DIR}...")
    html_files = []
    for root, dirs, files in os.walk(PUBLIC_DIR):
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))

    print(f"Found {len(html_files)} HTML files.")

    all_external_links = set()
    internal_broken = []

    for filepath in html_files:
        broken, soup = process_file(filepath)
        for b in broken:
            internal_broken.append((filepath, b[0], b[1]))

        # Collect external links
        for a in soup.find_all('a', href=True):
            href = a['href']
            if is_external(href) and not any(href.startswith(p) for p in IGNORE_PREFIXES):
                all_external_links.add(href)

    print(f"Found {len(all_external_links)} unique external links.")

    external_broken = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_url = {executor.submit(check_external_link, url): url for url in all_external_links}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                url, status, code = future.result()
                if status != "OK" and status != "Ignored":
                    external_broken.append((url, status, code))
            except Exception as exc:
                external_broken.append((url, "Exception", str(exc)))

    print("\n--- Report ---")
    if internal_broken:
        print("\nBroken Internal Links:")
        for item in internal_broken:
            print(f"File: {os.path.relpath(item[0], PUBLIC_DIR)}\n  Link: {item[1]} ({item[2]})")
    else:
        print("\nNo broken internal links found.")

    if external_broken:
        print("\nBroken External Links:")
        for item in external_broken:
            print(f"Link: {item[0]} - {item[1]} ({item[2]})")
    else:
        print("\nNo broken external links found.")

if __name__ == "__main__":
    main()
