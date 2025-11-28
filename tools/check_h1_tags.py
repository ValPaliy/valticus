#!/usr/bin/env python3
"""
Check for missing H1 tags in HTML files.
SEO best practice: Every page should have exactly one H1 tag.
"""

import os
import re
from pathlib import Path
from bs4 import BeautifulSoup
import json

def check_h1_tags(public_dir):
    """Check all HTML files for H1 tags."""
    results = {
        'missing_h1': [],
        'multiple_h1': [],
        'valid': []
    }

    public_path = Path(public_dir)
    if not public_path.exists():
        print(f"Error: Directory {public_dir} does not exist")
        return results

    # Find all HTML files
    html_files = list(public_path.rglob('*.html'))

    for html_file in html_files:
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Parse HTML
            soup = BeautifulSoup(content, 'html.parser')

            # Get relative path
            rel_path = html_file.relative_to(public_path)

            # Find all H1 tags
            h1_tags = soup.find_all('h1')
            h1_count = len(h1_tags)

            entry = {
                'file': str(rel_path),
                'h1_count': h1_count
            }

            if h1_count == 0:
                # Extract title for context
                title_tag = soup.find('title')
                entry['title'] = title_tag.string if title_tag else 'No title'
                results['missing_h1'].append(entry)
            elif h1_count > 1:
                entry['h1_texts'] = [h1.get_text(strip=True) for h1 in h1_tags]
                results['multiple_h1'].append(entry)
            else:
                entry['h1_text'] = h1_tags[0].get_text(strip=True)
                results['valid'].append(entry)

        except Exception as e:
            print(f"Error processing {html_file}: {str(e)}")

    return results

def main():
    public_dir = 'public'

    print("Checking for H1 tags in HTML files...")
    print(f"Scanning directory: {public_dir}\n")
    print("SEO Best Practice: Every page should have exactly one H1 tag")
    print("=" * 80)

    results = check_h1_tags(public_dir)

    total = len(results['missing_h1']) + len(results['multiple_h1']) + len(results['valid'])

    print(f"\nTotal HTML files scanned: {total}")
    print(f"  Missing H1: {len(results['missing_h1'])}")
    print(f"  Multiple H1: {len(results['multiple_h1'])}")
    print(f"  Valid (exactly 1 H1): {len(results['valid'])}\n")

    if results['missing_h1']:
        print("=" * 80)
        print("PAGES MISSING H1 TAG:")
        print("=" * 80)

        for entry in results['missing_h1'][:20]:  # Show first 20
            print(f"\nFile: {entry['file']}")
            print(f"Page title: {entry['title']}")
            print("-" * 80)

        if len(results['missing_h1']) > 20:
            print(f"\n... and {len(results['missing_h1']) - 20} more pages")

    if results['multiple_h1']:
        print("\n" + "=" * 80)
        print("PAGES WITH MULTIPLE H1 TAGS:")
        print("=" * 80)

        for entry in results['multiple_h1'][:10]:
            print(f"\nFile: {entry['file']}")
            print(f"H1 count: {entry['h1_count']}")
            print(f"H1 texts: {', '.join(entry['h1_texts'][:3])}")
            print("-" * 80)

    if not results['missing_h1'] and not results['multiple_h1']:
        print("✓ All pages have exactly one H1 tag!")

    # Save detailed report
    report = {
        'summary': {
            'total': total,
            'missing_h1': len(results['missing_h1']),
            'multiple_h1': len(results['multiple_h1']),
            'valid': len(results['valid'])
        },
        'missing_h1': results['missing_h1'][:50],
        'multiple_h1': results['multiple_h1'],
        'sample_valid': results['valid'][:10]
    }

    with open('h1_tag_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)

    print(f"\nDetailed report saved to: h1_tag_report.json")

if __name__ == '__main__':
    main()
