#!/usr/bin/env python3
"""
Analyze page titles for SEO length compliance.
Ideal title length: 50-60 characters
Maximum before truncation in search results: ~60 characters
"""

import os
import re
from pathlib import Path
import json

def extract_title_from_frontmatter(content):
    """Extract title from YAML frontmatter."""
    # Match YAML frontmatter
    frontmatter_pattern = r'^---\s*\n(.*?)\n---'
    match = re.search(frontmatter_pattern, content, re.DOTALL | re.MULTILINE)

    if match:
        frontmatter = match.group(1)
        # Extract title
        title_pattern = r'^title:\s*["\']?(.+?)["\']?\s*$'
        title_match = re.search(title_pattern, frontmatter, re.MULTILINE)
        if title_match:
            return title_match.group(1).strip('"\'')

    return None

def analyze_titles(content_dir):
    """Analyze all markdown files for title length."""
    results = {
        'too_long': [],
        'optimal': [],
        'short': []
    }

    content_path = Path(content_dir)
    if not content_path.exists():
        print(f"Error: Directory {content_dir} does not exist")
        return results

    # Find all markdown files
    md_files = list(content_path.rglob('*.md'))

    for md_file in md_files:
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()

            title = extract_title_from_frontmatter(content)

            if title:
                rel_path = md_file.relative_to(content_path)
                title_length = len(title)

                entry = {
                    'file': str(rel_path),
                    'title': title,
                    'length': title_length
                }

                if title_length > 60:
                    results['too_long'].append(entry)
                elif title_length >= 50:
                    results['optimal'].append(entry)
                else:
                    results['short'].append(entry)

        except Exception as e:
            print(f"Error processing {md_file}: {str(e)}")

    return results

def suggest_shortened_title(title, max_length=60):
    """Suggest a shortened version of the title."""
    if len(title) <= max_length:
        return title

    # Try to shorten intelligently
    # Remove common filler words
    fillers = [' - A ', ' And ', ' Or ', ' The ', ' Of ', ' In ', ' On ', ' To ', ' For ']
    shortened = title

    for filler in fillers:
        if filler in shortened and len(shortened) > max_length:
            shortened = shortened.replace(filler, ' ')

    # If still too long, truncate at word boundary
    if len(shortened) > max_length:
        words = shortened.split()
        result = []
        current_length = 0

        for word in words:
            if current_length + len(word) + 1 <= max_length - 3:  # Leave room for ...
                result.append(word)
                current_length += len(word) + 1
            else:
                break

        shortened = ' '.join(result)

    return shortened.strip()

def main():
    content_dir = 'content'

    print("Analyzing page titles for SEO compliance...")
    print(f"Scanning directory: {content_dir}\n")
    print("SEO Guidelines:")
    print("  - Optimal: 50-60 characters")
    print("  - Maximum: 60 characters (truncated in search results)")
    print("=" * 80)

    results = analyze_titles(content_dir)

    total = len(results['too_long']) + len(results['optimal']) + len(results['short'])

    print(f"\nTotal pages analyzed: {total}")
    print(f"  Too long (>60 chars): {len(results['too_long'])}")
    print(f"  Optimal (50-60 chars): {len(results['optimal'])}")
    print(f"  Short (<50 chars): {len(results['short'])}\n")

    if results['too_long']:
        print("=" * 80)
        print("TITLES TOO LONG (>60 characters):")
        print("=" * 80)

        for entry in sorted(results['too_long'], key=lambda x: x['length'], reverse=True):
            print(f"\nFile: {entry['file']}")
            print(f"Title: {entry['title']}")
            print(f"Length: {entry['length']} characters (exceeds by {entry['length'] - 60})")

            suggested = suggest_shortened_title(entry['title'])
            if suggested != entry['title']:
                print(f"Suggested: {suggested} ({len(suggested)} chars)")
            print("-" * 80)
    else:
        print("✓ All titles are within SEO guidelines!")

    # Save detailed report
    report = {
        'summary': {
            'total': total,
            'too_long': len(results['too_long']),
            'optimal': len(results['optimal']),
            'short': len(results['short'])
        },
        'too_long': results['too_long'],
        'optimal': results['optimal'][:10],  # Sample
        'short': results['short'][:10]  # Sample
    }

    with open('title_length_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)

    print(f"\nDetailed report saved to: title_length_report.json")

if __name__ == '__main__':
    main()
