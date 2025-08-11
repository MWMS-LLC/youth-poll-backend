-- Migration script to add site column to all tables
-- Run this BEFORE creating the schemas

-- Add site column to categories table
ALTER TABLE categories ADD COLUMN site VARCHAR(20) DEFAULT 'youth';

-- Add site column to blocks table  
ALTER TABLE blocks ADD COLUMN site VARCHAR(20) DEFAULT 'youth';

-- Add site column to questions table
ALTER TABLE questions ADD COLUMN site VARCHAR(20) DEFAULT 'youth';

-- Add site column to options table
ALTER TABLE options ADD COLUMN site VARCHAR(20) DEFAULT 'youth';

-- Add site column to responses table
ALTER TABLE responses ADD COLUMN site VARCHAR(20) DEFAULT 'youth';

-- Add site column to other_responses table
ALTER TABLE other_responses ADD COLUMN site VARCHAR(20) DEFAULT 'youth';

-- Add site column to checkbox_responses table
ALTER TABLE checkbox_responses ADD COLUMN site VARCHAR(20) DEFAULT 'youth';

-- Add site column to users table
ALTER TABLE users ADD COLUMN site VARCHAR(20) DEFAULT 'youth';

-- Add site column to user_block_progress table
ALTER TABLE user_block_progress ADD COLUMN site VARCHAR(20) DEFAULT 'youth';

-- Create indexes for better performance
CREATE INDEX idx_categories_site ON categories(site);
CREATE INDEX idx_blocks_site ON blocks(site);
CREATE INDEX idx_questions_site ON questions(site);
CREATE INDEX idx_options_site ON options(site);
CREATE INDEX idx_responses_site ON responses(site);
CREATE INDEX idx_other_responses_site ON other_responses(site);
CREATE INDEX idx_checkbox_responses_site ON checkbox_responses(site);
CREATE INDEX idx_users_site ON users(site);
CREATE INDEX idx_user_block_progress_site ON user_block_progress(site);

