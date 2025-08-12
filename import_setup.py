#!/usr/bin/env python3
"""
Setup Data Import Script for Youth Poll
========================================
Imports only setup data (categories, questions, options, blocks)
Can be run safely without affecting response data

Usage:
    python import_setup.py              # Import all setup data
    python import_setup.py --categories  # Import only categories
    python import_setup.py --questions   # Import only questions
    python import_setup.py --options     # Import only options
    python import_setup.py --blocks      # Import only blocks
"""

import os
import sys
import argparse
from sqlalchemy import create_engine, text
from pathlib import Path
import logging
from csv_parser import parse_simple_csv, parse_questions_csv, parse_options_csv

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_database_url():
    """Get database URL - use PostgreSQL for production"""
    return os.getenv('DATABASE_URL', 'postgresql://localhost/youth_poll_pg')

def create_setup_schema(engine):
    """Create setup schema tables"""
    logger.info("🔧 Creating setup schema...")
    
    try:
        schema_file = Path(__file__).parent / 'schema_setup.sql'
        with open(schema_file, 'r') as f:
            schema_sql = f.read()
        
        # Split by semicolons but handle multi-line statements
        statements = []
        current_statement = ""
        
        for line in schema_sql.split('\n'):
            line = line.strip()
            if line.startswith('--'):
                continue  # Skip comment lines
            if line:
                current_statement += line + " "
            elif current_statement.strip():
                # Empty line and we have content - check if statement ends with semicolon
                if current_statement.strip().endswith(';'):
                    statements.append(current_statement.strip())
                    current_statement = ""
        
        # Add the last statement if it exists
        if current_statement.strip():
            statements.append(current_statement.strip())
        
        logger.info(f"Parsed {len(statements)} SQL statements")
        
        with engine.connect() as conn:
            # Execute each statement in its own transaction
            for i, statement in enumerate(statements):
                if statement and not statement.startswith('--'):
                    try:
                        logger.info(f"Executing statement {i+1}: {statement[:50]}...")
                        conn.execute(text(statement))
                        conn.commit()  # Commit after each statement
                    except Exception as e:
                        logger.warning(f"Statement {i+1} failed (continuing): {statement[:50]}... - {e}")
                        conn.rollback()  # Rollback on error
                        continue
        
        logger.info("✅ Setup schema created successfully")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error creating setup schema: {e}")
        return False

def import_categories(engine):
    """Import categories from CSV"""
    logger.info("📁 Importing categories...")
    
    csv_file = Path(__file__).parent.parent / 'data' / 'categories.csv'
    rows = parse_simple_csv(csv_file)
    
    if not rows:
        logger.error("No categories data found")
        return False
    
    try:
        insert_sql = """
            INSERT INTO categories (id, category_name, description, category_text, category_text_long, version, uuid, site)
            VALUES (:id, :category_name, :description, :category_text, :category_text_long, :version, :uuid, :site)
            ON CONFLICT (id) DO UPDATE SET
                category_name = EXCLUDED.category_name,
                description = EXCLUDED.description,
                category_text = EXCLUDED.category_text,
                category_text_long = EXCLUDED.category_text_long,
                version = EXCLUDED.version,
                uuid = EXCLUDED.uuid,
                site = EXCLUDED.site
        """
        
        count = 0
        with engine.connect() as conn:
            for row in rows:
                try:
                    conn.execute(text(insert_sql), {
                        'id': int(row.get('id', 0)),
                        'category_name': row.get('category_name'),
                        'description': row.get('description'),
                        'category_text': row.get('category_text'),
                        'category_text_long': row.get('category_text_long'),
                        'version': row.get('version'),
                        'uuid': row.get('uuid'),
                        'site': row.get('site', 'youth')  # Default to 'youth' if not specified
                    })
                    count += 1
                except Exception as e:
                    logger.warning(f"Error importing category {row.get('id')}: {e}")
                    continue
            conn.commit()
        
        logger.info(f"✅ Successfully imported {count} categories")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error importing categories: {e}")
        return False

def import_blocks(engine):
    """Import blocks from CSV"""
    logger.info("🧩 Importing blocks...")
    
    csv_file = Path(__file__).parent.parent / 'data' / 'blocks.csv'
    rows = parse_simple_csv(csv_file)
    
    if not rows:
        logger.error("No blocks data found")
        return False
    
    try:
        insert_sql = """
            INSERT INTO blocks (id, category_id, block_number, block_text, version, uuid, category_name, site)
            VALUES (:id, :category_id, :block_number, :block_text, :version, :uuid, :category_name, :site)
            ON CONFLICT (id) DO UPDATE SET
                category_id = EXCLUDED.category_id,
                block_number = EXCLUDED.block_number,
                block_text = EXCLUDED.block_text,
                version = EXCLUDED.version,
                uuid = EXCLUDED.uuid,
                category_name = EXCLUDED.category_name,
                site = EXCLUDED.site
        """
        
        count = 0
        with engine.connect() as conn:
            for row in rows:
                try:
                    conn.execute(text(insert_sql), {
                        'id': int(row.get('id', 0)),
                        'category_id': int(row.get('category_id', 0)) if row.get('category_id') else None,
                        'block_number': int(row.get('block_number', 0)) if row.get('block_number') else None,
                        'block_text': row.get('block_text'),
                        'version': row.get('version'),
                        'uuid': row.get('uuid'),
                        'category_name': row.get('category_name'),
                        'site': row.get('site', 'youth')  # Default to 'youth' if not specified
                    })
                    count += 1
                except Exception as e:
                    logger.warning(f"Error importing block {row.get('id')}: {e}")
                    continue
            conn.commit()
        
        logger.info(f"✅ Successfully imported {count} blocks")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error importing blocks: {e}")
        return False

def import_questions(engine):
    """Import questions from CSV"""
    logger.info("❓ Importing questions...")
    
    csv_file = Path(__file__).parent.parent / 'data' / 'questions.csv'
    rows = parse_questions_csv(csv_file)
    
    if not rows:
        logger.error("No questions data found")
        return False
    
    try:
        insert_sql = """
            INSERT INTO questions (question_code, question_number, question_text, category_id, 
                                 is_start_question, check_box, block, color_code, color, 
                                 color_list_code, color_list, site)
            VALUES (:question_code, :question_number, :question_text, :category_id, 
                    :is_start_question, :check_box, :block, :color_code, :color, 
                    :color_list_code, :color_list, :site)
            ON CONFLICT (question_code) DO UPDATE SET
                question_number = EXCLUDED.question_number,
                question_text = EXCLUDED.question_text,
                category_id = EXCLUDED.category_id,
                is_start_question = EXCLUDED.is_start_question,
                check_box = EXCLUDED.check_box,
                block = EXCLUDED.block,
                color_code = EXCLUDED.color_code,
                color = EXCLUDED.color,
                color_list_code = EXCLUDED.color_list_code,
                color_list = EXCLUDED.color_list,
                site = EXCLUDED.site
        """
        
        count = 0
        batch_size = 100
        batch = []
        
        with engine.connect() as conn:
            for row in rows:
                try:
                    # Handle boolean values (could be string or already boolean)
                    is_start_question_val = row.get('is_start_question', False)
                    check_box_val = row.get('check_box', False)
                    
                    # Convert to boolean if it's a string
                    if isinstance(is_start_question_val, str):
                        is_start_question_bool = is_start_question_val.upper() == 'TRUE'
                    else:
                        is_start_question_bool = bool(is_start_question_val)
                        
                    if isinstance(check_box_val, str):
                        check_box_bool = check_box_val.upper() == 'TRUE'
                    else:
                        check_box_bool = bool(check_box_val)
                    
                    data = {
                        'question_code': row.get('question_id'),  # CSV has question_id mapped to question_code
                        'question_number': row.get('question_number'),
                        'question_text': row.get('question_text'),
                        'category_id': row.get('category_id'),
                        'is_start_question': is_start_question_bool,
                        'check_box': check_box_bool,
                        'block': row.get('block'),
                        'color_code': row.get('color_code'),
                        'color': row.get('color'),
                        'color_list_code': row.get('color_list_code'),
                        'color_list': row.get('color_list'),
                        'site': row.get('site', 'youth')  # Default to 'youth' if not specified
                    }
                    
                    if data['question_code']:  # Only process valid questions
                        batch.append(data)
                        count += 1
                        
                        # Process in batches
                        if len(batch) >= batch_size:
                            for item in batch:
                                conn.execute(text(insert_sql), item)
                            conn.commit()
                            logger.info(f"Processed {count} questions...")
                            batch = []
                
                except Exception as e:
                    logger.warning(f"Error processing question {row.get('question_id')}: {e}")
                    continue
            
            # Process remaining batch
            if batch:
                for item in batch:
                    conn.execute(text(insert_sql), item)
                conn.commit()
        
        logger.info(f"✅ Successfully imported {count} questions")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error importing questions: {e}")
        return False

def import_options(engine):
    """Import options from CSV"""
    logger.info("🔘 Importing options...")
    
    csv_file = Path(__file__).parent.parent / 'data' / 'options.csv'
    rows = parse_options_csv(csv_file)
    
    if not rows:
        logger.error("No options data found")
        return False
    
    try:
        insert_sql = """
            INSERT INTO options (question_code, option_text, option_code, next_question_code, 
                               response_message, companion_advice, site)
            VALUES (:question_code, :option_text, :option_code, :next_question_code,
                    :response_message, :companion_advice, :site)
            ON CONFLICT(question_code, option_code) DO NOTHING
        """
        
        count = 0
        processed = 0
        
        for row in rows:
            try:
                data = {
                    'question_code': row.get('question_id'),  # CSV has question_id mapped to question_code
                    'option_text': row.get('option_text'),
                    'option_code': row.get('option_code'),
                    'next_question_code': row.get('next_question_id'),  # CSV has next_question_id mapped to next_question_code
                    'response_message': row.get('response_message'),
                    'companion_advice': row.get('companion_advice'),
                    'site': row.get('site', 'youth')  # Default to 'youth' if not specified
                }
                
                if data['question_code'] and data['option_code']:
                    # Use individual transaction for each insert
                    with engine.connect() as conn:
                        conn.execute(text(insert_sql), data)
                        conn.commit()
                    
                    count += 1
                    
                    # Log progress
                    if count % 100 == 0:
                        logger.info(f"Processed {count} options...")
            
            except Exception as e:
                logger.warning(f"Error processing option {row.get('id')}: {e}")
                continue
        
        logger.info(f"✅ Successfully imported {count} options")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error importing options: {e}")
        return False

def main():
    """Main import function"""
    parser = argparse.ArgumentParser(description='Import Youth Poll setup data')
    parser.add_argument('--categories', action='store_true', help='Import only categories')
    parser.add_argument('--blocks', action='store_true', help='Import only blocks')
    parser.add_argument('--questions', action='store_true', help='Import only questions')
    parser.add_argument('--options', action='store_true', help='Import only options')
    parser.add_argument('--schema', action='store_true', help='Create schema only')
    
    args = parser.parse_args()
    
    logger.info("🚀 Starting Youth Poll setup data import...")
    
    # Get database connection
    try:
        database_url = get_database_url()
        logger.info(f"Connecting to database: {database_url.split('@')[0] if '@' in database_url else database_url}")
        engine = create_engine(database_url)
        
        # Test connection
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        
        logger.info("✅ Database connection successful")
        
    except Exception as e:
        logger.error(f"❌ Database connection failed: {e}")
        logger.error("Make sure PostgreSQL is running and the database exists")
        return False
    
    success = True
    
    # Create schema if requested or if no specific import requested
    if args.schema or not any([args.categories, args.blocks, args.questions, args.options]):
        success &= create_setup_schema(engine)
    
    # Import specific data or all if no specific flags
    if args.categories or not any([args.categories, args.blocks, args.questions, args.options]):
        success &= import_categories(engine)
    
    if args.blocks or not any([args.categories, args.blocks, args.questions, args.options]):
        success &= import_blocks(engine)
    
    if args.questions or not any([args.categories, args.blocks, args.questions, args.options]):
        success &= import_questions(engine)
    
    if args.options or not any([args.categories, args.blocks, args.questions, args.options]):
        success &= import_options(engine)
    
    if success:
        logger.info("🎉 Setup data import completed successfully!")
        logger.info("✅ Response data remains untouched and preserved")
        logger.info("")
        logger.info("Next steps:")
        logger.info("1. Create results schema: python -c \"from import_setup import *; create_results_schema()\"")
        logger.info("2. Start the API server: python main.py")
    else:
        logger.error("❌ Some imports failed - check logs above")
    
    return success

def create_results_schema(database_url=None):
    """Helper function to create results schema"""
    if not database_url:
        database_url = get_database_url()
    
    try:
        engine = create_engine(database_url)
        
        schema_file = Path(__file__).parent / 'schema_results.sql'
        with open(schema_file, 'r') as f:
            schema_sql = f.read()
        
        statements = [stmt.strip() for stmt in schema_sql.split(';') if stmt.strip()]
        
        with engine.connect() as conn:
            for statement in statements:
                if statement and not statement.startswith('--'):
                    try:
                        conn.execute(text(statement))
                    except Exception as e:
                        logger.warning(f"Statement failed (continuing): {statement[:50]}... - {e}")
                        continue
            conn.commit()
        
        logger.info("✅ Results schema created successfully")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error creating results schema: {e}")
        return False

if __name__ == "__main__":
    main()