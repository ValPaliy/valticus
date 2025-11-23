#!/usr/bin/env python3
"""
Script to check for pages with multiple H1 tags
"""

import os
import json
from pathlib import Path
from bs4 import BeautifulSoup

def count_h1_tags(html_content):
    """Count the number of H1 tags in HTML content"""
    soup = BeautifulSoup(html_content, 'html.parser')
    h1_tags = soup.find_all('h1')
    return len(h1_tags), [h1.get_text(strip=True) for h1 in h1_tags]

def scan_html_files(public_dir):
    """Scan all HTML files and find pages with multiple H1 tags"""
    results = {
        'total_pages': 0,
        'pages_with_zero_h1': [],
        'pages_with_one_h1': [],
        'pages_with_multiple_h1': [],
        'summary': {}
    }

    # Walk through all HTML files
    for root, dirs, files in os.walk(public_dir):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, public_dir)

                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    h1_count, h1_texts = count_h1_tags(content)
                    results['total_pages'] += 1

                    page_info = {
                        'path': rel_path,
                        'h1_count': h1_count,
                        'h1_texts': h1_texts
                    }

                    if h1_count == 0:
                        results['pages_with_zero_h1'].append(page_info)
                    elif h1_count == 1:
                        results['pages_with_one_h1'].append(page_info)
                    else:
                        results['pages_with_multiple_h1'].append(page_info)

                except Exception as e:
                    print(f"Error processing {rel_path}: {str(e)}")

    # Create summary
    results['summary'] = {
        'total_pages': results['total_pages'],
        'zero_h1': len(results['pages_with_zero_h1']),
        'one_h1': len(results['pages_with_one_h1']),
        'multiple_h1': len(results['pages_with_multiple_h1'])
    }

    return results

def main():
    public_dir = 'public'

    if not os.path.exists(public_dir):
        print(f"Error: {public_dir} directory not found!")
        return

    print("Scanning HTML files for H1 tags...")
    results = scan_html_files(public_dir)

    # Save detailed results to JSON
    with open('h1_multiple_report.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    # Print summary
    print("\n" + "="*60)
    print("H1 TAG ANALYSIS SUMMARY")
    print("="*60)
    print(f"\nTotal pages scanned: {results['summary']['total_pages']}")
    print(f"Pages with 0 H1 tags: {results['summary']['zero_h1']}")
    print(f"Pages with 1 H1 tag: {results['summary']['one_h1']} ✓")
    print(f"Pages with multiple H1 tags: {results['summary']['multiple_h1']}")

    if results['pages_with_multiple_h1']:
        print("\n" + "="*60)
        print("PAGES WITH MULTIPLE H1 TAGS (NEEDS FIXING)")
        print("="*60)
        for page in results['pages_with_multiple_h1'][:10]:  # Show first 10
            print(f"\n📄 {page['path']}")
            print(f"   H1 count: {page['h1_count']}")
            print(f"   H1 texts:")
            for i, text in enumerate(page['h1_texts'], 1):
                print(f"     {i}. {text}")

        if len(results['pages_with_multiple_h1']) > 10:
            print(f"\n... and {len(results['pages_with_multiple_h1']) - 10} more pages")
    else:
        print("\n✅ EXCELLENT! No pages found with multiple H1 tags!")

    if results['pages_with_zero_h1']:
        print("\n" + "="*60)
        print("PAGES WITH NO H1 TAGS (NEEDS FIXING)")
        print("="*60)
        for page in results['pages_with_zero_h1'][:10]:
            print(f"  - {page['path']}")

        if len(results['pages_with_zero_h1']) > 10:
            print(f"... and {len(results['pages_with_zero_h1']) - 10} more pages")

    print("\n" + "="*60)
    print(f"Detailed report saved to: h1_multiple_report.json")
    print("="*60)

if __name__ == "__main__":
    main()
