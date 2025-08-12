-- Youth Poll Setup Schema
-- Contains poll structure (categories, questions, options, blocks)
-- Can be safely dropped and reimported without affecting response data
-- =========================================================================

-- Drop setup tables in correct order
DROP TABLE IF EXISTS options CASCADE;
DROP TABLE IF EXISTS questions CASCADE;
DROP TABLE IF EXISTS categories CASCADE;
DROP TABLE IF EXISTS blocks CASCADE;

-- ======================
-- SETUP TABLES 
-- ======================

-- Categories table
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL,
    description TEXT,
    category_text TEXT NOT NULL,
    category_text_long TEXT,
    version VARCHAR(20),
    uuid VARCHAR(36),
    site VARCHAR(20) DEFAULT 'youth',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Questions table  
CREATE TABLE questions (
    id SERIAL PRIMARY KEY,
    question_code VARCHAR(50) NOT NULL UNIQUE,
    question_number INTEGER NOT NULL,
    question_text TEXT NOT NULL,
    category_id INTEGER REFERENCES categories(id),
    is_start_question BOOLEAN DEFAULT FALSE,
    check_box BOOLEAN DEFAULT FALSE,
    block INTEGER,
    color_code TEXT,
    color TEXT,
    color_list_code TEXT,
    color_list TEXT,
    site VARCHAR(20) DEFAULT 'youth',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(category_id, question_number)
);

-- Options table
CREATE TABLE options (
    id SERIAL PRIMARY KEY,
    question_code VARCHAR(50) NOT NULL REFERENCES questions(question_code) ON DELETE CASCADE,
    option_text TEXT NOT NULL,
    option_code VARCHAR(10) NOT NULL CHECK(option_code IN ('A','B','C','D','E','F','G','H','OTHER')),
    next_question_code VARCHAR(50) REFERENCES questions(question_code),
    response_message TEXT,
    companion_advice TEXT,
    tone_tag TEXT,
    site VARCHAR(20) DEFAULT 'youth',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(question_code, option_code)
);

-- Blocks table
CREATE TABLE blocks (
    id SERIAL PRIMARY KEY,
    category_id INTEGER REFERENCES categories(id),
    block_number INTEGER NOT NULL,
    block_text TEXT,
    version VARCHAR(20),
    uuid VARCHAR(36),
    category_name VARCHAR(100),
    site VARCHAR(20) DEFAULT 'youth',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ======================
-- INDEXES FOR SETUP TABLES
-- ======================

CREATE INDEX idx_questions_category ON questions(category_id);
CREATE INDEX idx_questions_question_code ON questions(question_code);
CREATE INDEX idx_questions_block ON questions(block);
CREATE INDEX idx_options_question ON options(question_code);
CREATE INDEX idx_options_code ON options(option_code);
CREATE INDEX idx_blocks_category ON blocks(category_id);

-- Site indexes for multi-site support
CREATE INDEX idx_categories_site ON categories(site);
CREATE INDEX idx_questions_site ON questions(site);
CREATE INDEX idx_options_site ON options(site);
CREATE INDEX idx_blocks_site ON blocks(site);

-- ======================
-- COMMENTS
-- ======================

COMMENT ON TABLE categories IS 'Poll categories - can be safely reimported';
COMMENT ON TABLE questions IS 'Poll questions - can be safely reimported';  
COMMENT ON TABLE options IS 'Question options - can be safely reimported';
COMMENT ON TABLE blocks IS 'Question blocks - can be safely reimported';

COMMENT ON SCHEMA public IS 'Youth Poll Setup Schema - Structure can be updated without affecting response data';