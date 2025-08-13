-- Results Tables Schema
-- These tables store user responses and are self-sufficient (denormalized)

-- Regular responses table
CREATE TABLE IF NOT EXISTS responses (
    id SERIAL PRIMARY KEY,
    user_uuid TEXT NOT NULL,
    question_code TEXT NOT NULL,
    question_text TEXT NOT NULL,
    option_code TEXT NOT NULL,
    option_text TEXT NOT NULL,
    category_name TEXT NOT NULL,
    version TEXT NOT NULL DEFAULT '1',
    site TEXT NOT NULL,
    year_of_birth INTEGER,
    block_text TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_uuid, question_code)
);

-- Checkbox responses table (multiple options per question)
CREATE TABLE IF NOT EXISTS checkbox_responses (
    id SERIAL PRIMARY KEY,
    user_uuid TEXT NOT NULL,
    question_code TEXT NOT NULL,
    question_text TEXT NOT NULL,
    option_code TEXT NOT NULL,
    option_text TEXT NOT NULL,
    category_name TEXT NOT NULL,
    version TEXT NOT NULL DEFAULT '1',
    site TEXT NOT NULL,
    year_of_birth INTEGER,
    block_text TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Other/free-text responses table
CREATE TABLE IF NOT EXISTS other_responses (
    id SERIAL PRIMARY KEY,
    user_uuid TEXT NOT NULL,
    question_code TEXT NOT NULL,
    question_text TEXT NOT NULL,
    other_text TEXT NOT NULL,
    category_name TEXT NOT NULL,
    version TEXT NOT NULL DEFAULT '1',
    site TEXT NOT NULL,
    year_of_birth INTEGER,
    block_text TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_uuid, question_code)
);

-- Users table (minimal, mainly for reference)
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    user_uuid TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_responses_user_uuid ON responses(user_uuid);
CREATE INDEX IF NOT EXISTS idx_responses_question_code ON responses(question_code);
CREATE INDEX IF NOT EXISTS idx_responses_site ON responses(site);

CREATE INDEX IF NOT EXISTS idx_checkbox_responses_user_uuid ON checkbox_responses(user_uuid);
CREATE INDEX IF NOT EXISTS idx_checkbox_responses_question_code ON checkbox_responses(question_code);
CREATE INDEX IF NOT EXISTS idx_checkbox_responses_site ON checkbox_responses(site);

CREATE INDEX IF NOT EXISTS idx_other_responses_user_uuid ON other_responses(user_uuid);
CREATE INDEX IF NOT EXISTS idx_other_responses_question_code ON other_responses(question_code);
CREATE INDEX IF NOT EXISTS idx_other_responses_site ON other_responses(site);
