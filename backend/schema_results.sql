-- Youth Poll Results Schema
-- Contains user responses with denormalized data
-- NEVER DROP - This preserves all historical response data
-- =========================================================================

-- ======================
-- USER TABLES
-- ======================

-- Users table (persistent across setup changes)
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    uuid VARCHAR(36) NOT NULL UNIQUE,
    year_of_birth INTEGER,
    referred_by VARCHAR(36),
    site VARCHAR(20) DEFAULT 'youth',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User block progress (persistent across setup changes)
CREATE TABLE IF NOT EXISTS user_block_progress (
    id SERIAL PRIMARY KEY,
    user_uuid VARCHAR(36) NOT NULL REFERENCES users(uuid),
    category_id INTEGER,
    block_number INTEGER,
    completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    -- Denormalized for safety
    category_name VARCHAR(100),
    site VARCHAR(20) DEFAULT 'youth',
    UNIQUE(user_uuid, category_id, block_number)
);

-- ======================
-- RESPONSE TABLES (DENORMALIZED)
-- ======================
-- These tables store actual text values to survive setup table changes

-- Standard responses (denormalized with text values)
CREATE TABLE IF NOT EXISTS responses (
    id SERIAL PRIMARY KEY,
    -- Response data
    user_uuid VARCHAR(36),
    
    -- Question data (denormalized)
    question_code VARCHAR(50) NOT NULL,
    question_text TEXT NOT NULL,
    question_number INTEGER,
    
    -- Category data (denormalized) 
    category_id INTEGER,
    category_name VARCHAR(100) NOT NULL,
    category_text TEXT,
    
    -- Option data (denormalized)
    option_id INTEGER,
    option_code VARCHAR(10) NOT NULL,
    option_text TEXT NOT NULL,
    
    -- Block data (denormalized)
    block_number INTEGER,
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    site VARCHAR(20) DEFAULT 'youth',
    
    -- Optional reference to setup tables (can break without data loss)
    setup_question_code VARCHAR(50),
    setup_option_id INTEGER
);

-- Checkbox responses (denormalized with text values)
CREATE TABLE IF NOT EXISTS checkbox_responses (
    id SERIAL PRIMARY KEY,
    -- Response data
    user_uuid VARCHAR(36),
    
    -- Question data (denormalized)
    question_code VARCHAR(50) NOT NULL,
    question_text TEXT NOT NULL,
    question_number INTEGER,
    
    -- Category data (denormalized)
    category_id INTEGER,
    category_name VARCHAR(100) NOT NULL,
    category_text TEXT,
    
    -- Option data (denormalized)
    option_id INTEGER,
    option_code VARCHAR(10) NOT NULL,
    option_text TEXT NOT NULL,
    
    -- Block data (denormalized)
    block_number INTEGER,
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    site VARCHAR(20) DEFAULT 'youth',
    
    -- Optional reference to setup tables (can break without data loss)
    setup_question_code VARCHAR(50),
    setup_option_id INTEGER,
    
    -- Prevent duplicate responses
    UNIQUE(user_uuid, question_code, option_code, created_at)
);

-- Other/free-text responses (denormalized with text values)
CREATE TABLE IF NOT EXISTS other_responses (
    id SERIAL PRIMARY KEY,
    -- Response data
    user_uuid VARCHAR(36),
    other_text TEXT NOT NULL,
    
    -- Question data (denormalized)
    question_code VARCHAR(50) NOT NULL,
    question_text TEXT NOT NULL,
    question_number INTEGER,
    
    -- Category data (denormalized)
    category_id INTEGER,
    category_name VARCHAR(100) NOT NULL,
    category_text TEXT,
    
    -- Block data (denormalized)
    block_number INTEGER,
    
    -- Metadata
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    site VARCHAR(20) DEFAULT 'youth',
    
    -- Optional reference to setup tables (can break without data loss)
    setup_question_code VARCHAR(50)
);

-- ======================
-- INDEXES FOR RESPONSE TABLES
-- ======================

-- User indexes
CREATE INDEX IF NOT EXISTS idx_users_uuid ON users(uuid);
CREATE INDEX IF NOT EXISTS idx_user_block_progress_user ON user_block_progress(user_uuid);
CREATE INDEX IF NOT EXISTS idx_user_block_progress_category ON user_block_progress(category_id);

-- Site indexes for multi-site support
CREATE INDEX IF NOT EXISTS idx_users_site ON users(site);
CREATE INDEX IF NOT EXISTS idx_user_block_progress_site ON user_block_progress(site);

-- Response table indexes
CREATE INDEX IF NOT EXISTS idx_responses_user ON responses(user_uuid);
CREATE INDEX IF NOT EXISTS idx_responses_question ON responses(question_code);
CREATE INDEX IF NOT EXISTS idx_responses_category ON responses(category_name);
CREATE INDEX IF NOT EXISTS idx_responses_created ON responses(created_at);
CREATE INDEX IF NOT EXISTS idx_responses_site ON responses(site);

CREATE INDEX IF NOT EXISTS idx_checkbox_responses_user ON checkbox_responses(user_uuid);
CREATE INDEX IF NOT EXISTS idx_checkbox_responses_question ON checkbox_responses(question_code);
CREATE INDEX IF NOT EXISTS idx_checkbox_responses_category ON checkbox_responses(category_name);
CREATE INDEX IF NOT EXISTS idx_checkbox_responses_created ON checkbox_responses(created_at);
CREATE INDEX IF NOT EXISTS idx_checkbox_responses_site ON checkbox_responses(site);

CREATE INDEX IF NOT EXISTS idx_other_responses_user ON other_responses(user_uuid);
CREATE INDEX IF NOT EXISTS idx_other_responses_question ON other_responses(question_code);
CREATE INDEX IF NOT EXISTS idx_other_responses_category ON other_responses(category_name);
CREATE INDEX IF NOT EXISTS idx_other_responses_submitted ON other_responses(submitted_at);
CREATE INDEX IF NOT EXISTS idx_other_responses_site ON other_responses(site);

-- ======================
-- COMMENTS
-- ======================

COMMENT ON TABLE users IS 'User accounts - persistent across setup changes';
COMMENT ON TABLE user_block_progress IS 'User progress tracking - persistent across setup changes';

COMMENT ON TABLE responses IS 'Standard responses with denormalized data - survives setup table changes';
COMMENT ON TABLE checkbox_responses IS 'Checkbox responses with denormalized data - survives setup table changes';
COMMENT ON TABLE other_responses IS 'Free-text responses with denormalized data - survives setup table changes';

COMMENT ON COLUMN responses.setup_question_code IS 'Optional reference to current setup tables - can be NULL if setup changed';
COMMENT ON COLUMN responses.setup_option_id IS 'Optional reference to current setup tables - can be NULL if setup changed';