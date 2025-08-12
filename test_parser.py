#!/usr/bin/env python3
"""Test script to debug CSV parsing"""

from csv_parser import parse_questions_csv
from pathlib import Path

# Test the questions parser
csv_file = Path(__file__).parent.parent / 'data' / 'questions.csv'
rows = parse_questions_csv(csv_file)

print(f"Total rows parsed: {len(rows)}")
print("\nFirst 5 rows:")
for i, row in enumerate(rows[:5]):
    print(f"Row {i+1}: {row}")

print("\nChecking for site values:")
teen_count = 0
youth_count = 0
null_count = 0

for row in rows:
    site = row.get('site')
    if site == 'teen':
        teen_count += 1
    elif site == 'youth':
        youth_count += 1
    else:
        null_count += 1

print(f"Teen questions: {teen_count}")
print(f"Youth questions: {youth_count}")
print(f"Null site: {null_count}")

# Check category distribution
print("\nCategory distribution:")
category_sites = {}
for row in rows:
    cat_id = row.get('category_id')
    site = row.get('site')
    if cat_id not in category_sites:
        category_sites[cat_id] = {'teen': 0, 'youth': 0}
    if site == 'teen':
        category_sites[cat_id]['teen'] += 1
    elif site == 'youth':
        category_sites[cat_id]['youth'] += 1

for cat_id in sorted(category_sites.keys()):
    print(f"Category {cat_id}: Teen={category_sites[cat_id]['teen']}, Youth={category_sites[cat_id]['youth']}")
