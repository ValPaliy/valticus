#!/usr/bin/env python3
"""
Check for missing alt attributes in images across the Hugo site.
"""

import os
import re
from pathlib import Path
from bs4 import BeautifulSoup
import json

def check_alt_attributes(public_dir):
    """Check all HTML files for images with missing alt attributes."""
    issues = []
    valid_images = []

    public_path = Path(public_dir)
    if not public_path.exists():
        print(f"Error: Directory {public_dir} does not exist")
        return issues, valid_images

    # Find all HTML files
    html_files = list(public_path.rglob('*.html'))

    for html_file in html_files:
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Parse HTML
            soup = BeautifulSoup(content, 'html.parser')

            # Get relative path for reporting
            rel_path = html_file.relative_to(public_path)

            # Find all img tags
            images = soup.find_all('img')

            for img in images:
                src = img.get('src', '')
                alt = img.get('alt', '')
                img_class = img.get('class', [])

                # Check if alt attribute is missing or empty
                if not alt or alt.strip() == '':
                    issues.append({
                        'file': str(rel_path),
                        'src': src,
                        'class': ' '.join(img_class) if isinstance(img_class, list) else img_class,
                        'issue': 'Missing or empty alt attribute',
                        'html': str(img)[:200]  # First 200 chars of the img tag
                    })
                else:
                    valid_images.append({
                        'file': str(rel_path),
                        'src': src,
                        'alt': alt
                    })

        except Exception as e:
            print(f"Error processing {html_file}: {str(e)}")

    return issues, valid_images

def main():
    public_dir = 'public'

    print("Checking for missing alt attributes in images...")
    print(f"Scanning directory: {public_dir}\n")

    issues, valid_images = check_alt_attributes(public_dir)

    # Report results
    total_images = len(issues) + len(valid_images)
    print(f"Total images found: {total_images}")
    print(f"Images with valid alt attributes: {len(valid_images)}")
    print(f"Images with missing/empty alt attributes: {len(issues)}\n")

    if issues:
        print("=" * 80)
        print("IMAGES WITH MISSING ALT ATTRIBUTES:")
        print("=" * 80)

        # Group by file
        files_with_issues = {}
        for issue in issues:
            file = issue['file']
            if file not in files_with_issues:
                files_with_issues[file] = []
            files_with_issues[file].append(issue)

        for file, file_issues in sorted(files_with_issues.items()):
            print(f"\nFile: {file}")
            print(f"  Issues: {len(file_issues)}")
            for issue in file_issues[:3]:  # Show first 3 per file
                print(f"  - Source: {issue['src']}")
                if issue['class']:
                    print(f"    Class: {issue['class']}")
            if len(file_issues) > 3:
                print(f"  ... and {len(file_issues) - 3} more")
            print("-" * 80)
    else:
        print("✓ No images with missing alt attributes found!")

    # Save detailed report
    report = {
        'summary': {
            'total_images': total_images,
            'valid': len(valid_images),
            'issues': len(issues)
        },
        'issues': issues[:50],  # Limit to first 50 issues
        'sample_valid': valid_images[:10]  # Sample of valid images
    }

    with open('alt_attribute_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)

    print(f"\nDetailed report saved to: alt_attribute_report.json")

if __name__ == '__main__':
    main()
