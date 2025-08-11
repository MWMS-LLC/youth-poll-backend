#!/usr/bin/env python3
import os
from sqlalchemy import create_engine, text

# Set database URL
DATABASE_URL = "postgresql://mwms_polls_db_rbj5_user:jhNQweOFPAm9jm3GwQgqIduXBvWsrlbe@dpg-d2aes03e5dus73cpe30g-a.oregon-postgres.render.com/mwms_polls_db_rbj5?sslmode=require"

# Create engine
engine = create_engine(DATABASE_URL)

# Check categories and blocks
with engine.connect() as conn:
    result = conn.execute(text("SELECT DISTINCT category_id, block FROM questions ORDER BY category_id, block"))
    print("Available Category/Block combinations:")
    for row in result:
        print(f"Category {row[0]}, Block {row[1]}")
    
    # Check categories
    result = conn.execute(text("SELECT id, category_name FROM categories ORDER BY id"))
    print("\nAvailable Categories:")
    for row in result:
        print(f"ID {row[0]}: {row[1]}")
