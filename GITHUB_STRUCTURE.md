# GitHub Repository Structure for Multi-Site Poll

## **Repository Organization**

### **Backend Repositories (Shared API)**
```
youth-poll-backend/     # Main backend for all sites
├── main.py
├── requirements.txt
├── schema_setup.sql
├── schema_results.sql
├── import_setup.py
└── data/
    ├── categories.csv    # All sites data
    ├── questions.csv     # All sites data
    ├── options.csv       # All sites data
    └── blocks.csv        # All sites data
```

### **Frontend Repositories (Site-Specific)**
```
youth-poll-frontend/     # youth.myworldmysay.com
├── src/
│   ├── config.js        # API_BASE_URL = youth.myworldmysay.com/api
│   └── ...
└── package.json

teen-poll-frontend/      # teen.myworldmysay.com
├── src/
│   ├── config.js        # API_BASE_URL = teen.myworldmysay.com/api
│   └── ...
└── package.json

parents-poll-frontend/   # parents.myworldmysay.com
├── src/
│   ├── config.js        # API_BASE_URL = parents.myworldmysay.com/api
│   └── ...
└── package.json

schools-poll-frontend/   # schools.myworldmysay.com
├── src/
│   ├── config.js        # API_BASE_URL = schools.myworldmysay.com/api
│   └── ...
└── package.json
```

## **Repository Creation Commands**

### **1. Create Backend Repository**
```bash
# In your LLC GitHub account
# Create: youth-poll-backend
cd backend
git init
git add .
git commit -m "Initial youth poll backend with multi-site support"
git remote add origin https://github.com/your-llc-account/youth-poll-backend.git
git push -u origin main
```

### **2. Create Frontend Repositories**
```bash
# For each site (youth, teen, parents, schools)
# Create: youth-poll-frontend, teen-poll-frontend, parents-poll-frontend, schools-poll-frontend

# Example for youth:
cp -r frontend youth-poll-frontend
cd youth-poll-frontend
# Update config.js for youth site
git init
git add .
git commit -m "Initial youth poll frontend"
git remote add origin https://github.com/your-llc-account/youth-poll-frontend.git
git push -u origin main
```

## **Site-Specific Configurations**

### **Frontend Config Files**

**youth-poll-frontend/src/config.js:**
```javascript
const API_BASE_URL = import.meta.env.PROD 
  ? 'https://youth.myworldmysay.com/api'
  : 'http://localhost:8000';
```

**teen-poll-frontend/src/config.js:**
```javascript
const API_BASE_URL = import.meta.env.PROD 
  ? 'https://teen.myworldmysay.com/api'
  : 'http://localhost:8000';
```

**parents-poll-frontend/src/config.js:**
```javascript
const API_BASE_URL = import.meta.env.PROD 
  ? 'https://parents.myworldmysay.com/api'
  : 'http://localhost:8000';
```

**schools-poll-frontend/src/config.js:**
```javascript
const API_BASE_URL = import.meta.env.PROD 
  ? 'https://schools.myworldmysay.com/api'
  : 'http://localhost:8000';
```

## **Data Organization**

### **CSV Files Structure**
All CSV files contain data for all sites with `site` column:

**categories.csv:**
```csv
id,category_name,description,site
1,Love,What do you think about love?,teen
2,Friends,What do you think about friends?,teen
3,Healing,What helps you heal?,youth
4,Politics,What do you think about politics?,youth
5,Parenting,What's your view on parenting?,parents
6,Education,What do you think about education?,schools
```

## **Benefits of This Structure**

1. **Clear Separation**: Each site has its own frontend repository
2. **Shared Backend**: One backend serves all sites with site filtering
3. **Easy Management**: Each site can be updated independently
4. **Scalable**: Easy to add new sites following the same pattern
5. **Clear Naming**: No confusion about which site is which
