# Youth Poll Backend - Clean Architecture

This backend is designed for the new Youth Poll system with separated setup and response data to prevent data loss during content updates.

## Architecture Overview

### 🔄 Problem Solved
- **Old System**: Setup and response data were linked via foreign keys, causing data loss when reimporting content
- **New System**: Response data is denormalized and self-contained, surviving setup table changes

### 📊 Database Schema

#### Setup Tables (can be safely reimported)
- `categories` - Poll categories  
- `questions` - Poll questions (uses `question_code` as unique identifier)
- `options` - Question options
- `blocks` - Question blocks

#### Results Tables (persistent across setup changes)
- `users` - User accounts
- `responses` - Standard responses with denormalized text data
- `checkbox_responses` - Multi-select responses with denormalized text data  
- `other_responses` - Free-text responses with denormalized text data
- `user_block_progress` - User progress tracking

## Setup Instructions

### 1. Local Database Setup
```bash
# Create PostgreSQL database
./create_local_db.sh

# Or manually:
createdb youth_poll_dev
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Import Data
```bash
# Complete setup (recommended for first time)
python3 setup_database.py

# Or import specific data types
python3 import_setup.py --categories
python3 import_setup.py --questions  
python3 import_setup.py --options
python3 import_setup.py --blocks
```

### 4. Verify Setup
```bash
# Test CSV parsing
python3 csv_parser.py

# Expected output:
# Categories: 12 rows
# Blocks: 45 rows  
# Questions: 226 rows
# Options: 1115 rows
```

## Key Features

### ✅ BOM and Multi-line CSV Handling
- Robust CSV parser handles UTF-8 BOM
- Proper multi-line quoted field support
- Handles complex text with embedded quotes and newlines

### ✅ Data Preservation
- Response data survives setup table reimports
- Denormalized storage includes actual text values
- Optional references to setup tables (can break safely)

### ✅ Consistent Naming
- Uses `question_code` instead of `question_id` to avoid confusion with primary keys
- All tables have single `id` primary key
- Clear separation between setup and response schemas

## File Structure

```
backend/
├── schema_setup.sql      # Setup tables schema
├── schema_results.sql    # Response tables schema  
├── import_setup.py       # Setup data import script
├── setup_database.py     # Complete database setup
├── csv_parser.py         # Robust CSV parsing utilities
├── create_local_db.sh    # Local database creation script
└── main.py              # FastAPI application (to be created)
```

## Environment Variables

```bash
# Local development (default)
DATABASE_URL=postgresql://localhost:5432/youth_poll_dev

# Production (set in Render)
DATABASE_URL=postgresql://user:pass@host:port/dbname
```

## Next Steps

1. ✅ Create database schemas
2. ✅ Build import system  
3. ✅ Test CSV parsing
4. 🔄 Create FastAPI endpoints
5. 🔄 Deploy to LLC Render account
6. 🔄 Set up frontend for youth.myworldmysay.com

## Deployment Strategy

1. **youth.myworldmysay.com** - Test/pilot site (current workspace)
2. **teen.myworldmysay.com** - Future main site (duplicate when ready)
3. **parents.myworldmysay.com** - Parent-focused version
4. **schools.myworldmysay.com** - School-focused version

**Important**: Never touch the existing `myworldmysay.com` - it stays untouched!