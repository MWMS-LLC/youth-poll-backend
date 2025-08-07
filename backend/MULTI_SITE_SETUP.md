# Multi-Site Setup Guide

## What We've Done

✅ **Updated Database Schema**
- Added `site` column to all tables (categories, questions, options, blocks, responses, etc.)
- Added site indexes for better performance
- Default site value is 'youth'

✅ **Updated Import Scripts**
- `import_setup.py` now handles site column from CSV files
- Automatically adds site='youth' if not specified in CSV

✅ **Updated API Endpoints**
- All endpoints now filter by site
- Uses `X-Site` header or defaults to 'youth'
- Categories, blocks, questions all filtered by site

✅ **Created Helper Script**
- `add_site_to_csv.py` to add site column to your CSV files

## Next Steps

### 1. Add Site Column to Your CSV Files

Run this command to add the site column:
```bash
cd backend
python add_site_to_csv.py youth
```

### 2. Edit Your CSV Files in Excel

Now you can edit your CSV files to add different content for different sites:

**Example `categories.csv`:**
```csv
id,category_name,category_text,site
1,Love,What do you think about love?,teen
2,Friends,What do you think about friends?,teen
3,Love,What do you think about love?,youth
4,Politics,What do you think about politics?,youth
5,Marriage,What do you think about marriage?,youth
```

**Example `questions.csv`:**
```csv
question_id,question_text,category_id,site
Q1,Do you believe in love at first sight?,1,teen
Q2,How important are friends to you?,2,teen
Q3,What's your view on political engagement?,3,youth
Q4,Do you think marriage is still relevant?,4,youth
```

### 3. Import Updated Data

```bash
python import_setup.py
```

### 4. Test Different Sites

You can test different sites by setting the `X-Site` header:

```bash
# Test youth site (default)
curl http://localhost:8000/api/categories

# Test teen site
curl -H "X-Site: teen" http://localhost:8000/api/categories
```

## Future Multi-Site Deployment

When you deploy multiple sites, each site will:
- Use the same database
- Filter by its own site value
- Have completely separate content and responses

**Site Values:**
- `youth.myworldmysay.com` → `site = 'youth'`
- `teen.myworldmysay.com` → `site = 'teen'`
- `parents.myworldmysay.com` → `site = 'parents'`
- `schools.myworldmysay.com` → `site = 'schools'`

## Benefits

✅ **One Database**: All sites share the same database
✅ **Separate Content**: Each site has its own categories, questions, etc.
✅ **Separate Responses**: User responses are filtered by site
✅ **Easy Management**: One set of CSV files for all sites
✅ **Scalable**: Easy to add new sites

## Files Modified

- `backend/schema_setup.sql` - Added site column
- `backend/schema_results.sql` - Added site column  
- `backend/import_setup.py` - Updated to handle site column
- `backend/main.py` - Updated API endpoints to filter by site
- `backend/add_site_to_csv.py` - Helper script (new)
- `backend/add_site_column.sql` - Migration script (new)
