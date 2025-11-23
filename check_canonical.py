#!/usr/bin/env python3
"""
Check for broken canonical URLs in Hugo-generated HTML files.
"""

import os
import re
from pathlib import Path
from urllib.parse import urlparse
import json

def extract_canonical_url(html_content):
    """Extract canonical URL from HTML content."""
    # Look for <link rel="canonical" href="...">
    pattern = r'<link\s+rel=["\']canonical["\']\s+href=["\'](.*?)["\']'
    match = re.search(pattern, html_content, re.IGNORECASE)
    if match:
        return match.group(1)
    return None

def check_canonical_urls(public_dir):
    """Check all HTML files for canonical URL issues."""
    issues = []
    valid_pages = []

    public_path = Path(public_dir)
    if not public_path.exists():
        print(f"Error: Directory {public_dir} does not exist")
        return issues, valid_pages

    # Find all HTML files
    html_files = list(public_path.rglob('*.html'))

    for html_file in html_files:
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()

            canonical_url = extract_canonical_url(content)

            # Get relative path for reporting
            rel_path = html_file.relative_to(public_path)

            if canonical_url is None:
                issues.append({
                    'file': str(rel_path),
                    'issue': 'Missing canonical URL',
                    'canonical': None
                })
            else:
                # Check for common issues
                parsed = urlparse(canonical_url)

                # Check if URL is malformed
                if not parsed.scheme or not parsed.netloc:
                    issues.append({
                        'file': str(rel_path),
                        'issue': 'Malformed canonical URL (missing scheme or domain)',
                        'canonical': canonical_url
                    })
                # Check for localhost or development URLs
                elif 'localhost' in parsed.netloc or '127.0.0.1' in parsed.netloc:
                    issues.append({
                        'file': str(rel_path),
                        'issue': 'Development URL in canonical (localhost)',
                        'canonical': canonical_url
                    })
                # Check for HTTP instead of HTTPS
                elif parsed.scheme == 'http':
                    issues.append({
                        'file': str(rel_path),
                        'issue': 'HTTP instead of HTTPS in canonical URL',
                        'canonical': canonical_url
                    })
                # Check for trailing slash consistency
                elif canonical_url.endswith('/') and str(rel_path) != 'index.html':
                    # This is actually OK for directories
                    valid_pages.append({
                        'file': str(rel_path),
                        'canonical': canonical_url
                    })
                else:
                    valid_pages.append({
                        'file': str(rel_path),
                        'canonical': canonical_url
                    })

        except Exception as e:
            issues.append({
                'file': str(rel_path),
                'issue': f'Error reading file: {str(e)}',
                'canonical': None
            })

    return issues, valid_pages

def main():
    public_dir = 'public'

    print("Checking canonical URLs in Hugo site...")
    print(f"Scanning directory: {public_dir}\n")

    issues, valid_pages = check_canonical_urls(public_dir)

    # Report results
    print(f"Total HTML files scanned: {len(issues) + len(valid_pages)}")
    print(f"Pages with valid canonical URLs: {len(valid_pages)}")
    print(f"Pages with issues: {len(issues)}\n")

    if issues:
        print("=" * 80)
        print("PAGES WITH CANONICAL URL ISSUES:")
        print("=" * 80)

        for issue in issues:
            print(f"\nFile: {issue['file']}")
            print(f"Issue: {issue['issue']}")
            if issue['canonical']:
                print(f"Canonical URL: {issue['canonical']}")
            print("-" * 80)
    else:
        print("✓ No canonical URL issues found!")

    # Save detailed report
    report = {
        'summary': {
            'total_files': len(issues) + len(valid_pages),
            'valid': len(valid_pages),
            'issues': len(issues)
        },
        'issues': issues,
        'valid_pages': valid_pages[:10]  # Sample of valid pages
    }

    with open('canonical_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)

    print(f"\nDetailed report saved to: canonical_report.json")

if __name__ == '__main__':
    main()
