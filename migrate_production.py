#!/usr/bin/env python3
"""
Standalone script to migrate production database to add site columns
Run this locally to connect to production database
"""

import os
import psycopg2
from psycopg2.extras import RealDictCursor

# Production database URL from Render
PRODUCTION_DATABASE_URL = "postgresql://mwms_polls_db_rbj5_user:jhNQweOFPAm9jm3GwQgqIduXBvWsrlbe@dpg-d2aes03e5dus73cpe30g-a.oregon-postgres.render.com/mwms_polls_db_rbj5"

def migrate_production_database():
    """Migrate production database to add site columns"""
    
    if PRODUCTION_DATABASE_URL == "postgresql://...":
        print("❌ Please update PRODUCTION_DATABASE_URL with your actual Railway database URL")
        print("   You can find this in your Railway dashboard under the backend service")
        return
    
    try:
        # Connect to production database
        print("🔌 Connecting to production database...")
        conn = psycopg2.connect(PRODUCTION_DATABASE_URL)
        cursor = conn.cursor()
        
        print("✅ Connected successfully!")
        
        # Add site column to categories table
        print("📝 Adding site column to categories table...")
        cursor.execute("ALTER TABLE categories ADD COLUMN IF NOT EXISTS site TEXT NOT NULL DEFAULT 'youth'")
        
        # Update existing categories to separate youth vs teen
        print("🔄 Updating category sites...")
        cursor.execute("UPDATE categories SET site = 'youth' WHERE id = 1")
        cursor.execute("UPDATE categories SET site = 'teen' WHERE id IN (7, 8, 9, 10, 11, 12)")
        
        # Add site column to other tables
        print("📝 Adding site columns to other tables...")
        cursor.execute("ALTER TABLE questions ADD COLUMN IF NOT EXISTS site TEXT NOT NULL DEFAULT 'youth'")
        cursor.execute("ALTER TABLE options ADD COLUMN IF NOT EXISTS site TEXT NOT NULL DEFAULT 'youth'")
        cursor.execute("ALTER TABLE blocks ADD COLUMN IF NOT EXISTS site TEXT NOT NULL DEFAULT 'youth'")
        
        # Update related tables to match category site
        print("🔄 Updating related table sites...")
        cursor.execute("""
            UPDATE questions SET site = c.site 
            FROM categories c 
            WHERE questions.category_id = c.id
        """)
        
        cursor.execute("""
            UPDATE options SET site = q.site 
            FROM questions q 
            WHERE options.question_code = q.question_code
        """)
        
        cursor.execute("""
            UPDATE blocks SET site = c.site 
            FROM categories c 
            WHERE blocks.category_id = c.id
        """)
        
        # Remove defaults
        print("🧹 Removing default constraints...")
        cursor.execute("ALTER TABLE categories ALTER COLUMN site DROP DEFAULT")
        cursor.execute("ALTER TABLE questions ALTER COLUMN site DROP DEFAULT")
        cursor.execute("ALTER TABLE options ALTER COLUMN site DROP DEFAULT")
        cursor.execute("ALTER TABLE blocks ALTER COLUMN site DROP DEFAULT")
        
        # Commit changes
        conn.commit()
        print("✅ Migration completed successfully!")
        
        # Verify the changes
        print("🔍 Verifying changes...")
        cursor.execute("SELECT id, category_name, site FROM categories ORDER BY id")
        categories = cursor.fetchall()
        
        print("Categories with sites:")
        for cat in categories:
            print(f"  ID {cat[0]}: {cat[1]} -> {cat[2]}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Migration failed: {str(e)}")
        if 'conn' in locals():
            conn.rollback()
            conn.close()

if __name__ == "__main__":
    print("🚀 Production Database Migration Script")
    print("=" * 40)
    migrate_production_database()
