-- Youth Poll Results Schema (SQLite Version)
-- This schema stores user responses with denormalized data for safety

-- Drop existing tables (SQLite doesn't support CASCADE)
DROP TABLE IF EXISTS checkbox_responses;
DROP TABLE IF EXISTS other_responses;
DROP TABLE IF EXISTS responses;
DROP TABLE IF EXISTS user_block_progress;
DROP TABLE IF EXISTS users;

-- Create users table
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    user_uuid VARCHAR(36) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    site VARCHAR(20) DEFAULT 'youth'
);

-- Create user_block_progress table
CREATE TABLE user_block_progress (
    id INTEGER PRIMARY KEY,
    user_uuid VARCHAR(36) NOT NULL,
    category_id INTEGER NOT NULL,
    block_id INTEGER NOT NULL,
    completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    site VARCHAR(20) DEFAULT 'youth',
    FOREIGN KEY (user_uuid) REFERENCES users(user_uuid),
    FOREIGN KEY (category_id) REFERENCES categories(id),
    FOREIGN KEY (block_id) REFERENCES blocks(id)
);

-- Create responses table (single choice)
CREATE TABLE responses (
    id INTEGER PRIMARY KEY,
    user_uuid VARCHAR(36) NOT NULL,
    question_code VARCHAR(50) NOT NULL,
    option_code VARCHAR(50) NOT NULL,
    question_text TEXT NOT NULL,
    option_text TEXT NOT NULL,
    category_name VARCHAR(100) NOT NULL,
    block_text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    site VARCHAR(20) DEFAULT 'youth',
    FOREIGN KEY (user_uuid) REFERENCES users(user_uuid)
);

-- Create checkbox_responses table (multi-select)
CREATE TABLE checkbox_responses (
    id INTEGER PRIMARY KEY,
    user_uuid VARCHAR(36) NOT NULL,
    question_code VARCHAR(50) NOT NULL,
    option_code VARCHAR(50) NOT NULL,
    question_text TEXT NOT NULL,
    option_text TEXT NOT NULL,
    category_name VARCHAR(100) NOT NULL,
    block_text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    site VARCHAR(20) DEFAULT 'youth',
    FOREIGN KEY (user_uuid) REFERENCES users(user_uuid)
);

-- Create other_responses table (text input)
CREATE TABLE other_responses (
    id INTEGER PRIMARY KEY,
    user_uuid VARCHAR(36) NOT NULL,
    setup_question_code VARCHAR(50) NOT NULL,
    question_text TEXT NOT NULL,
    response_text TEXT NOT NULL,
    category_name VARCHAR(100) NOT NULL,
    block_text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    site VARCHAR(20) DEFAULT 'youth',
    FOREIGN KEY (user_uuid) REFERENCES users(user_uuid)
);

-- Create indexes for performance
CREATE INDEX idx_users_site ON users(site);
CREATE INDEX idx_user_block_progress_site ON user_block_progress(site);
CREATE INDEX idx_responses_site ON responses(site);
CREATE INDEX idx_checkbox_responses_site ON checkbox_responses(site);
CREATE INDEX idx_other_responses_site ON other_responses(site);
CREATE INDEX idx_responses_question_code ON responses(question_code);
CREATE INDEX idx_checkbox_responses_question_code ON checkbox_responses(question_code);
CREATE INDEX idx_other_responses_question_code ON other_responses(setup_question_code);

