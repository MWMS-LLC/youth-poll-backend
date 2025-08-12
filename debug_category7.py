#!/usr/bin/env python3
"""Debug script to check category 7 questions"""

from csv_parser import parse_questions_csv
from pathlib import Path

# Parse the CSV
csv_file = Path('..') / 'data' / 'questions.csv'
rows = parse_questions_csv(csv_file)

print(f"Total questions parsed: {len(rows)}")

# Check for category 7
category7_questions = [row for row in rows if row.get('category_id') == 7]
print(f"Questions for category 7: {len(category7_questions)}")

if category7_questions:
    print("\nFirst few category 7 questions:")
    for i, row in enumerate(category7_questions[:5]):
        print(f"  {i+1}. ID: {row.get('id')}, Question ID: {row.get('question_id')}, Site: {row.get('site')}")
        print(f"     Text: {row.get('question_text')[:100]}...")
        print()

# Check all category IDs
category_ids = set(row.get('category_id') for row in rows if row.get('category_id'))
print(f"All category IDs found: {sorted(category_ids)}")
