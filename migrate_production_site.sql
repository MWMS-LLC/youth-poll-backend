-- Migration to add site column to production database
-- Run this on the production database

-- Add site column to categories table
ALTER TABLE categories ADD COLUMN IF NOT EXISTS site TEXT NOT NULL DEFAULT 'youth';

-- Update existing categories to separate youth vs teen
-- Youth gets 1 category, Teen gets 12 categories
UPDATE categories SET site = 'youth' WHERE id = 1;  -- Youth category
UPDATE categories SET site = 'teen' WHERE id IN (7, 8, 9, 10, 11, 12);  -- Teen categories

-- Add site column to other tables if they don't have it
ALTER TABLE questions ADD COLUMN IF NOT EXISTS site TEXT NOT NULL DEFAULT 'youth';
ALTER TABLE options ADD COLUMN IF NOT EXISTS site TEXT NOT NULL DEFAULT 'youth';
ALTER TABLE blocks ADD COLUMN IF NOT EXISTS site TEXT NOT NULL DEFAULT 'youth';

-- Update questions, options, and blocks to match their category's site
UPDATE questions SET site = c.site 
FROM categories c 
WHERE questions.category_id = c.id;

UPDATE options SET site = q.site 
FROM questions q 
WHERE options.question_code = q.question_code;

UPDATE blocks SET site = c.site 
FROM categories c 
WHERE blocks.category_id = c.id;

-- Remove default constraint from site columns
ALTER TABLE categories ALTER COLUMN site DROP DEFAULT;
ALTER TABLE questions ALTER COLUMN site DROP DEFAULT;
ALTER TABLE options ALTER COLUMN site DROP DEFAULT;
ALTER TABLE blocks ALTER COLUMN site DROP DEFAULT;
