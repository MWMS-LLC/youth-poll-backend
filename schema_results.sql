-- Results Schema for Youth Poll
-- These tables store user responses and voting data

-- Users table to track unique users
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    user_uuid VARCHAR(255) UNIQUE NOT NULL,
    site VARCHAR(20) DEFAULT 'youth',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Responses table for standard voting
CREATE TABLE IF NOT EXISTS responses (
    id SERIAL PRIMARY KEY,
    user_uuid VARCHAR(255) NOT NULL,
    question_code VARCHAR(50) NOT NULL,
    option_code VARCHAR(10) NOT NULL,
    site VARCHAR(20) DEFAULT 'youth',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_uuid) REFERENCES users(user_uuid) ON DELETE CASCADE,
    FOREIGN KEY (question_code) REFERENCES questions(question_code) ON DELETE CASCADE
);

-- Other responses table for text-based answers
CREATE TABLE IF NOT EXISTS other_responses (
    id SERIAL PRIMARY KEY,
    user_uuid VARCHAR(255) NOT NULL,
    question_code VARCHAR(50) NOT NULL,
    other_text TEXT NOT NULL,
    site VARCHAR(20) DEFAULT 'youth',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_uuid) REFERENCES users(user_uuid) ON DELETE CASCADE,
    FOREIGN KEY (question_code) REFERENCES questions(question_code) ON DELETE CASCADE
);

-- Checkbox responses table for multi-select questions
CREATE TABLE IF NOT EXISTS checkbox_responses (
    id SERIAL PRIMARY KEY,
    user_uuid VARCHAR(255) NOT NULL,
    question_code VARCHAR(50) NOT NULL,
    option_code VARCHAR(10) NOT NULL,
    site VARCHAR(20) DEFAULT 'youth',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_uuid) REFERENCES users(user_uuid) ON DELETE CASCADE,
    FOREIGN KEY (question_code) REFERENCES questions(question_code) ON DELETE CASCADE
);

-- User block progress tracking
CREATE TABLE IF NOT EXISTS user_block_progress (
    id SERIAL PRIMARY KEY,
    user_uuid VARCHAR(255) NOT NULL,
    category_id INTEGER NOT NULL,
    block_number INTEGER NOT NULL,
    completed BOOLEAN DEFAULT FALSE,
    site VARCHAR(20) DEFAULT 'youth',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_uuid) REFERENCES users(user_uuid) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_responses_question ON responses(question_code, site);
CREATE INDEX IF NOT EXISTS idx_responses_user ON responses(user_uuid);
CREATE INDEX IF NOT EXISTS idx_other_responses_question ON other_responses(question_code, site);
CREATE INDEX IF NOT EXISTS idx_checkbox_responses_question ON checkbox_responses(question_code, site);
CREATE INDEX IF NOT EXISTS idx_users_site ON users(site);
CREATE INDEX IF NOT EXISTS idx_user_block_progress_user ON user_block_progress(user_uuid, category_id);

