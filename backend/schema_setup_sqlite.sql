-- Youth Poll Setup Schema (SQLite Version)
-- This schema can be safely reimported without affecting results

-- Drop existing tables (SQLite doesn't support CASCADE)
DROP TABLE IF EXISTS options;
DROP TABLE IF EXISTS questions;
DROP TABLE IF EXISTS categories;
DROP TABLE IF EXISTS blocks;

-- Create categories table
CREATE TABLE categories (
    id INTEGER PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL,
    description TEXT,
    category_text TEXT,
    category_text_long TEXT,
    version VARCHAR(20),
    uuid VARCHAR(36),
    site VARCHAR(20) DEFAULT 'youth'
);

-- Create blocks table
CREATE TABLE blocks (
    id INTEGER PRIMARY KEY,
    category_id INTEGER NOT NULL,
    block_number INTEGER NOT NULL,
    block_text TEXT NOT NULL,
    description TEXT,
    version VARCHAR(20),
    uuid VARCHAR(36),
    site VARCHAR(20) DEFAULT 'youth',
    FOREIGN KEY (category_id) REFERENCES categories(id)
);

-- Create questions table
CREATE TABLE questions (
    id INTEGER PRIMARY KEY,
    question_code VARCHAR(50) UNIQUE NOT NULL,
    block_id INTEGER NOT NULL,
    question_text TEXT NOT NULL,
    question_type VARCHAR(20) DEFAULT 'single_choice',
    is_start_question BOOLEAN DEFAULT FALSE,
    version VARCHAR(20),
    uuid VARCHAR(36),
    site VARCHAR(20) DEFAULT 'youth',
    FOREIGN KEY (block_id) REFERENCES blocks(id)
);

-- Create options table
CREATE TABLE options (
    id INTEGER PRIMARY KEY,
    question_code VARCHAR(50) NOT NULL,
    option_code VARCHAR(50) NOT NULL,
    option_text TEXT NOT NULL,
    option_order INTEGER DEFAULT 0,
    check_box BOOLEAN DEFAULT FALSE,
    version VARCHAR(20),
    uuid VARCHAR(36),
    site VARCHAR(20) DEFAULT 'youth',
    FOREIGN KEY (question_code) REFERENCES questions(question_code),
    UNIQUE(question_code, option_code)
);

-- Create indexes for performance
CREATE INDEX idx_categories_site ON categories(site);
CREATE INDEX idx_questions_site ON questions(site);
CREATE INDEX idx_options_site ON options(site);
CREATE INDEX idx_blocks_site ON blocks(site);
CREATE INDEX idx_questions_block_id ON questions(block_id);
CREATE INDEX idx_options_question_code ON options(question_code);

