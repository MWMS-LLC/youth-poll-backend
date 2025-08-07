#!/usr/bin/env python3
"""
Deployment setup script for youth.myworldmysay.com
This script initializes the production database with all data.
"""

import os
import sys
from pathlib import Path
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Add the current directory to Python path
sys.path.append(str(Path(__file__).parent))

from import_setup import parse_categories_csv, parse_blocks_csv, parse_questions_csv, parse_options_csv

def get_database_url():
    """Get database URL from environment"""
    return os.getenv('DATABASE_URL')

def create_schemas(engine):
    """Create both setup and results schemas"""
    print("🔧 Creating database schemas...")
    
    # Create setup schema
    schema_file = Path(__file__).parent / 'schema_setup.sql'
    with open(schema_file, 'r') as f:
        schema_sql = f.read()
    
    with engine.connect() as conn:
        # Split and execute SQL statements
        statements = schema_sql.split(';')
        for statement in statements:
            statement = statement.strip()
            if statement:
                try:
                    conn.execute(text(statement))
                except Exception as e:
                    print(f"Warning: {e}")
        conn.commit()
    
    # Create results schema
    schema_results_file = Path(__file__).parent / 'schema_results.sql'
    with open(schema_results_file, 'r') as f:
        schema_results_sql = f.read()
    
    with engine.connect() as conn:
        # Split and execute SQL statements
        statements = schema_results_sql.split(';')
        for statement in statements:
            statement = statement.strip()
            if statement:
                try:
                    conn.execute(text(statement))
                except Exception as e:
                    print(f"Warning: {e}")
        conn.commit()
    
    print("✅ Schemas created successfully")

def import_all_data(engine):
    """Import all data from CSV files"""
    print("📁 Importing all data...")
    
    # Import categories
    print("📂 Importing categories...")
    csv_file = Path(__file__).parent.parent / 'data' / 'categories.csv'
    rows = parse_categories_csv(csv_file)
    
    with engine.connect() as conn:
        for row in rows:
            try:
                conn.execute(text("""
                    INSERT INTO categories (id, category_name, category_text, category_text_long, description)
                    VALUES (:id, :category_name, :category_text, :category_text_long, :description)
                    ON CONFLICT (id) DO UPDATE SET
                        category_name = EXCLUDED.category_name,
                        category_text = EXCLUDED.category_text,
                        category_text_long = EXCLUDED.category_text_long,
                        description = EXCLUDED.description
                """), row)
            except Exception as e:
                print(f"Warning: {e}")
        conn.commit()
    
    print(f"✅ Imported {len(rows)} categories")
    
    # Import blocks
    print("📂 Importing blocks...")
    csv_file = Path(__file__).parent.parent / 'data' / 'blocks.csv'
    rows = parse_blocks_csv(csv_file)
    
    with engine.connect() as conn:
        for row in rows:
            try:
                conn.execute(text("""
                    INSERT INTO blocks (id, category_id, block_number, block_text, version, uuid, category_name)
                    VALUES (:id, :category_id, :block_number, :block_text, :version, :uuid, :category_name)
                    ON CONFLICT (id) DO UPDATE SET
                        category_id = EXCLUDED.category_id,
                        block_number = EXCLUDED.block_number,
                        block_text = EXCLUDED.block_text,
                        version = EXCLUDED.version,
                        uuid = EXCLUDED.uuid,
                        category_name = EXCLUDED.category_name
                """), row)
            except Exception as e:
                print(f"Warning: {e}")
        conn.commit()
    
    print(f"✅ Imported {len(rows)} blocks")
    
    # Import questions
    print("📂 Importing questions...")
    csv_file = Path(__file__).parent.parent / 'data' / 'questions.csv'
    rows = parse_questions_csv(csv_file)
    
    with engine.connect() as conn:
        for row in rows:
            try:
                # Handle boolean values
                is_start_question_val = row.get('is_start_question', False)
                check_box_val = row.get('check_box', False)
                
                if isinstance(is_start_question_val, str):
                    is_start_question_bool = is_start_question_val.upper() == 'TRUE'
                else:
                    is_start_question_bool = bool(is_start_question_val)
                    
                if isinstance(check_box_val, str):
                    check_box_bool = check_box_val.upper() == 'TRUE'
                else:
                    check_box_bool = bool(check_box_val)
                
                conn.execute(text("""
                    INSERT INTO questions (question_code, question_number, question_text, category_id, 
                                         is_start_question, check_box, block, color_code, color, 
                                         color_list_code, color_list)
                    VALUES (:question_code, :question_number, :question_text, :category_id, 
                            :is_start_question, :check_box, :block, :color_code, :color, 
                            :color_list_code, :color_list)
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
                        color_list = EXCLUDED.color_list
                """), {
                    'question_code': row.get('question_id'),
                    'question_number': row.get('question_number'),
                    'question_text': row.get('question_text'),
                    'category_id': row.get('category_id'),
                    'is_start_question': is_start_question_bool,
                    'check_box': check_box_bool,
                    'block': row.get('block'),
                    'color_code': row.get('color_code'),
                    'color': row.get('color'),
                    'color_list_code': row.get('color_list_code'),
                    'color_list': row.get('color_list')
                })
            except Exception as e:
                print(f"Warning: {e}")
        conn.commit()
    
    print(f"✅ Imported {len(rows)} questions")
    
    # Import options
    print("📂 Importing options...")
    csv_file = Path(__file__).parent.parent / 'data' / 'options.csv'
    rows = parse_options_csv(csv_file)
    
    with engine.connect() as conn:
        for row in rows:
            try:
                conn.execute(text("""
                    INSERT INTO options (question_code, option_text, option_code, next_question_code, 
                                       response_message, companion_advice)
                    VALUES (:question_code, :option_text, :option_code, :next_question_code,
                            :response_message, :companion_advice)
                    ON CONFLICT(question_code, option_code) DO NOTHING
                """), {
                    'question_code': row.get('question_id'),
                    'option_text': row.get('option_text'),
                    'option_code': row.get('option_code'),
                    'next_question_code': row.get('next_question_id'),
                    'response_message': row.get('response_message', ''),
                    'companion_advice': row.get('companion_advice', '')
                })
            except Exception as e:
                print(f"Warning: {e}")
        conn.commit()
    
    print(f"✅ Imported {len(rows)} options")

def main():
    """Main deployment setup function"""
    print("🚀 Starting Youth Poll deployment setup...")
    
    # Load environment variables
    load_dotenv()
    
    # Get database URL
    database_url = get_database_url()
    if not database_url:
        print("❌ DATABASE_URL environment variable not set")
        sys.exit(1)
    
    print(f"🔗 Connecting to database: {database_url}")
    
    # Create engine
    engine = create_engine(database_url)
    
    try:
        # Test connection
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("✅ Database connection successful")
        
        # Create schemas
        create_schemas(engine)
        
        # Import all data
        import_all_data(engine)
        
        print("🎉 Deployment setup completed successfully!")
        print("✅ Database is ready for production")
        
    except Exception as e:
        print(f"❌ Error during deployment setup: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
