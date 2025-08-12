-- Remove the unique constraint that's preventing multiple "Other" responses
-- This allows users to submit multiple "Other" responses for the same question

-- First, let's see what constraints exist
SELECT conname, contype, pg_get_constraintdef(oid) 
FROM pg_constraint 
WHERE conrelid = 'other_responses'::regclass;

-- Remove the specific unique constraint
ALTER TABLE other_responses DROP CONSTRAINT IF EXISTS other_responses_user_uuid_question_code_key;

-- Verify the constraint is removed
SELECT conname, contype, pg_get_constraintdef(oid) 
FROM pg_constraint 
WHERE conrelid = 'other_responses'::regclass;

