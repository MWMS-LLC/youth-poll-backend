-- Fix questions table site values to match their categories
-- This will resolve the 500 errors on /api/start-question/{category_id}

-- First, let's see what we're working with
SELECT 'Before fix - Questions with NULL or mismatched site values:' as info;
SELECT q.id, q.question_code, q.category_id, q.site as question_site, c.site as category_site
FROM questions q 
JOIN categories c ON q.category_id = c.id 
WHERE q.site IS NULL OR q.site != c.site
LIMIT 10;

-- Now fix the questions table site values
UPDATE questions 
SET site = c.site 
FROM categories c 
WHERE questions.category_id = c.id 
  AND (questions.site IS NULL OR questions.site != c.site);

-- Verify the fix worked
SELECT 'After fix - Questions with correct site values:' as info;
SELECT q.id, q.question_code, q.category_id, q.site as question_site, c.site as category_site
FROM questions q 
JOIN categories c ON q.category_id = c.id 
WHERE q.site = c.site
LIMIT 10;

-- Final verification - should return 0 rows if everything is fixed
SELECT 'Final check - Any remaining mismatches (should be 0):' as info;
SELECT COUNT(*) as mismatched_count
FROM questions q 
JOIN categories c ON q.category_id = c.id 
WHERE q.site != c.site OR q.site IS NULL;

