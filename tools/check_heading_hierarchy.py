#!/usr/bin/env python3
"""
Check for heading hierarchy issues in HTML files.
SEO/Accessibility best practice: Headings should be in sequentially-descending order.
"""

import os
import re
from pathlib import Path
from bs4 import BeautifulSoup
import json

def check_heading_hierarchy(public_dir):
    """Check all HTML files for heading hierarchy issues."""
    results = {
        'hierarchy_issues': [],
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

            # Find all heading tags
            headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])

            if not headings:
                continue

            # Extract heading levels
            heading_levels = []
            for heading in headings:
                level = int(heading.name[1])
                text = heading.get_text(strip=True)[:50]  # First 50 chars
                heading_levels.append({
                    'level': level,
                    'text': text,
                    'tag': heading.name
                })

            # Check for hierarchy issues
            issues = []
            for i in range(1, len(heading_levels)):
                prev_level = heading_levels[i-1]['level']
                curr_level = heading_levels[i]['level']

                # Check if heading skips levels (e.g., H1 -> H3)
                if curr_level > prev_level + 1:
                    issues.append({
                        'type': 'skipped_level',
                        'from': heading_levels[i-1],
                        'to': heading_levels[i],
                        'message': f"Heading skips from H{prev_level} to H{curr_level}"
                    })

            entry = {
                'file': str(rel_path),
                'headings': heading_levels,
                'issues': issues
            }

            if issues:
                results['hierarchy_issues'].append(entry)
            else:
                results['valid'].append(entry)

        except Exception as e:
            print(f"Error processing {html_file}: {str(e)}")

    return results

def main():
    public_dir = 'public'

    print("Checking heading hierarchy in HTML files...")
    print(f"Scanning directory: {public_dir}\n")
    print("SEO/Accessibility Best Practice: Headings should be in sequentially-descending order")
    print("=" * 80)

    results = check_heading_hierarchy(public_dir)

    total = len(results['hierarchy_issues']) + len(results['valid'])

    print(f"\nTotal HTML files with headings: {total}")
    print(f"  Files with hierarchy issues: {len(results['hierarchy_issues'])}")
    print(f"  Valid files: {len(results['valid'])}\n")

    if results['hierarchy_issues']:
        print("=" * 80)
        print("HEADING HIERARCHY ISSUES:")
        print("=" * 80)

        for entry in results['hierarchy_issues'][:20]:  # Show first 20
            print(f"\nFile: {entry['file']}")
            print(f"Heading sequence: {' -> '.join([f\"{h['tag'].upper()}\" for h in entry['headings']])}")

            for issue in entry['issues']:
                print(f"  ⚠ {issue['message']}")
                print(f"    From: {issue['from']['tag'].upper()}: \"{issue['from']['text']}\"")
                print(f"    To:   {issue['to']['tag'].upper()}: \"{issue['to']['text']}\"")

            print("-" * 80)

        if len(results['hierarchy_issues']) > 20:
            print(f"\n... and {len(results['hierarchy_issues']) - 20} more files with issues")

    if not results['hierarchy_issues']:
        print("✓ All pages have proper heading hierarchy!")

    # Save detailed report
    report = {
        'summary': {
            'total': total,
            'hierarchy_issues': len(results['hierarchy_issues']),
            'valid': len(results['valid'])
        },
        'hierarchy_issues': results['hierarchy_issues'][:50],
        'sample_valid': results['valid'][:10]
    }

    with open('heading_hierarchy_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)

    print(f"\nDetailed report saved to: heading_hierarchy_report.json")

if __name__ == '__main__':
    main()
