#!/usr/bin/env python3
"""
Special CSV parser for Youth Poll data
Handles complex multi-line quoted fields and BOM issues
"""

import csv
import codecs
import logging
from io import StringIO
from pathlib import Path

logger = logging.getLogger(__name__)

def remove_bom(content):
    """Remove BOM from content if present"""
    if isinstance(content, bytes):
        if content.startswith(codecs.BOM_UTF8):
            content = content[len(codecs.BOM_UTF8):]
        content = content.decode('utf-8')
    elif isinstance(content, str):
        if content.startswith('\ufeff'):
            content = content[1:]
    return content

def parse_options_csv(file_path):
    """
    Special parser for options.csv which has complex multi-line structure
    """
    logger.info(f"Parsing complex options CSV: {file_path}")
    
    if not Path(file_path).exists():
        logger.error(f"File not found: {file_path}")
        return []
    
    # Read raw content
    with open(file_path, 'rb') as f:
        raw_content = f.read()
    
    content = remove_bom(raw_content)
    
    try:
        # Use csv.DictReader with proper multi-line handling
        csv_file = StringIO(content)
        reader = csv.DictReader(csv_file, quoting=csv.QUOTE_MINIMAL)
        
        rows = []
        for row_num, row in enumerate(reader, start=2):
            try:
                # Clean and validate the row
                cleaned_row = {}
                
                # Required fields
                if not row.get('id') or not row.get('question_id'):
                    logger.warning(f"Row {row_num}: Missing required fields (id or question_id)")
                    continue
                
                # Process each field
                cleaned_row['id'] = int(row['id']) if row.get('id') else None
                cleaned_row['category_id'] = int(row['category_id']) if row.get('category_id') else None
                cleaned_row['question_id'] = clean_field(row.get('question_id'))
                cleaned_row['question_number'] = int(row['question_number']) if row.get('question_number') else None
                cleaned_row['question_text'] = clean_field(row.get('question_text'))
                cleaned_row['check_box'] = parse_boolean(row.get('check_box'))
                cleaned_row['block_number'] = int(row['block_number']) if row.get('block_number') else None
                cleaned_row['block_text'] = clean_field(row.get('block_text'))
                cleaned_row['option_code'] = clean_field(row.get('option_code'))
                cleaned_row['option_text'] = clean_field(row.get('option_text'))
                cleaned_row['response_message'] = clean_field(row.get('response_message'))
                cleaned_row['companion_advice'] = clean_field(row.get('companion_advice'))
                cleaned_row['tone_tag'] = clean_field(row.get('tone_tag'))
                cleaned_row['next_question_id'] = clean_field(row.get('next_question_id'))
                
                if cleaned_row['id'] and cleaned_row['question_id']:
                    rows.append(cleaned_row)
                    
            except Exception as e:
                logger.warning(f"Row {row_num}: Error processing row - {e}")
                continue
        
        logger.info(f"Successfully parsed {len(rows)} options from CSV")
        return rows
        
    except Exception as e:
        logger.error(f"Error parsing options CSV: {e}")
        return []

def parse_questions_csv(file_path):
    """
    Parser for questions.csv (large file)
    """
    logger.info(f"Parsing questions CSV: {file_path}")
    
    if not Path(file_path).exists():
        logger.error(f"File not found: {file_path}")
        return []
    
    try:
        rows = []
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            
            for row_num, row in enumerate(reader, start=2):
                try:
                    # Clean and validate
                    if not (row.get('question_id') or row.get('question_code')):
                        continue
                    
                    cleaned_row = {
                        'id': int(row['id']) if row.get('id') else None,
                        'question_id': clean_field(row.get('question_code') or row.get('question_id')),  # Always return as question_id for consistency
                        'question_number': int(row['question_number']) if row.get('question_number') else None,
                        'question_text': clean_field(row.get('question_text')),
                        'category_id': int(row['category_id']) if row.get('category_id') else None,
                        'is_start_question': parse_boolean(row.get('is_start_question')),
                        'check_box': parse_boolean(row.get('check_box')),
                        'block': int(row.get('block_number') or row.get('block', 0)) if row.get('block_number') or row.get('block') else None,
                        'color_code': clean_field(row.get('color_code')),
                        'color': clean_field(row.get('color')),
                        'color_list_code': clean_field(row.get('color_list_code')),
                        'color_list': clean_field(row.get('color_list'))
                    }
                    
                    if cleaned_row['question_id']:
                        rows.append(cleaned_row)
                        
                except Exception as e:
                    logger.warning(f"Row {row_num}: Error processing question - {e}")
                    continue
        
        logger.info(f"Successfully parsed {len(rows)} questions from CSV")
        return rows
        
    except Exception as e:
        logger.error(f"Error parsing questions CSV: {e}")
        return []

def parse_simple_csv(file_path):
    """
    Parser for simple CSV files (categories, blocks)
    """
    logger.info(f"Parsing simple CSV: {file_path}")
    
    if not Path(file_path).exists():
        logger.error(f"File not found: {file_path}")
        return []
    
    try:
        # Read with BOM handling
        with open(file_path, 'rb') as f:
            raw_content = f.read()
        
        content = remove_bom(raw_content)
        csv_file = StringIO(content)
        reader = csv.DictReader(csv_file)
        
        rows = []
        for row in reader:
            # Clean all fields
            cleaned_row = {}
            for key, value in row.items():
                if key:
                    clean_key = key.strip().strip('"')
                    cleaned_row[clean_key] = clean_field(value)
            
            if cleaned_row:
                rows.append(cleaned_row)
        
        logger.info(f"Successfully parsed {len(rows)} rows from CSV")
        return rows
        
    except Exception as e:
        logger.error(f"Error parsing simple CSV: {e}")
        return []

def clean_field(value):
    """Clean individual field values"""
    if value is None:
        return None
    
    value = str(value).strip()
    
    # Handle empty values
    if not value or value.lower() in ['null', 'none', '']:
        return None
    
    # Remove surrounding quotes if present
    if value.startswith('"') and value.endswith('"'):
        value = value[1:-1]
    
    # Handle escaped quotes
    value = value.replace('""', '"')
    
    # Normalize line endings
    value = value.replace('\r\n', '\n').replace('\r', '\n')
    
    return value

def parse_boolean(value):
    """Parse boolean values from CSV"""
    if value is None:
        return False
    
    value = str(value).strip().lower()
    return value in ['true', '1', 'yes', 'on']

def test_parsers():
    """Test the parsers with actual data"""
    base_path = Path(__file__).parent.parent / 'data'
    
    print("Testing CSV parsers...")
    
    # Test categories
    categories = parse_simple_csv(base_path / 'categories.csv')
    print(f"Categories: {len(categories)} rows")
    if categories:
        print(f"Sample category: {categories[0]}")
    
    # Test blocks  
    blocks = parse_simple_csv(base_path / 'blocks.csv')
    print(f"Blocks: {len(blocks)} rows")
    if blocks:
        print(f"Sample block: {blocks[0]}")
    
    # Test questions
    questions = parse_questions_csv(base_path / 'questions.csv')
    print(f"Questions: {len(questions)} rows")
    if questions:
        print(f"Sample question: {questions[0]}")
    
    # Test options
    options = parse_options_csv(base_path / 'options.csv')
    print(f"Options: {len(options)} rows")
    if options:
        print(f"Sample option: {options[0]}")

if __name__ == "__main__":
    test_parsers()