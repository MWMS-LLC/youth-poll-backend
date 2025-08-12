#!/usr/bin/env python3
"""Detailed CSV debugging script"""

import csv
from pathlib import Path
from io import StringIO

def remove_bom(content):
    """Remove BOM from content if present"""
    if isinstance(content, bytes):
        if content.startswith(b'\xef\xbb\xbf'):
            content = content[3:]
        content = content.decode('utf-8')
    elif isinstance(content, str):
        if content.startswith('\ufeff'):
            content = content[1:]
    return content

def debug_csv():
    csv_file = Path('..') / 'data' / 'questions.csv'
    print(f"CSV file: {csv_file}")
    print(f"File exists: {csv_file.exists()}")
    print(f"File size: {csv_file.stat().st_size} bytes")
    
    print("\n" + "="*60)
    print("RAW BYTES READING:")
    print("="*60)
    
    with open(csv_file, 'rb') as f:
        raw_content = f.read()
    
    print(f"Raw content length: {len(raw_content)} bytes")
    print(f"First 100 bytes: {raw_content[:100]}")
    bom_bytes = b'\xef\xbb\xbf'
    print(f"BOM present: {raw_content.startswith(bom_bytes)}")
    
    print("\n" + "="*60)
    print("AFTER BOM REMOVAL:")
    print("="*60)
    
    content = remove_bom(raw_content)
    print(f"Content length after BOM removal: {len(content)}")
    print(f"First 200 chars: {content[:200]}")
    
    print("\n" + "="*60)
    print("CSV PARSING TEST:")
    print("="*60)
    
    csv_file_io = StringIO(content)
    reader = csv.DictReader(csv_file_io)
    
    rows = list(reader)
    print(f"Total rows parsed: {len(rows)}")
    
    if rows:
        print(f"Headers: {list(rows[0].keys())}")
        
        # Look for category 7
        cat7_rows = [row for row in rows if row.get('category_id') == '7']
        print(f"Rows with category_id = 7: {len(cat7_rows)}")
        
        if cat7_rows:
            print("\nFirst category 7 row:")
            row = cat7_rows[0]
            for key, value in row.items():
                print(f"  {key}: {str(value)[:100]}...")
        
        # Check all categories
        all_cats = set(row.get('category_id') for row in rows if row.get('category_id'))
        print(f"\nAll category IDs found: {sorted(all_cats)}")
        
        # Look at rows around where category 7 should be
        print(f"\nRows 135-145:")
        for i in range(134, min(145, len(rows))):
            if i < len(rows):
                row = rows[i]
                print(f"  Row {i+1}: ID={row.get('id')}, Category={row.get('category_id')}, Site={row.get('site')}")

if __name__ == "__main__":
    debug_csv()
