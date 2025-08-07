# Complete Multi-Site Deployment Checklist

## **Phase 1: GitHub Repository Setup**

### **✅ Backend Repository**
- [ ] Create `youth-poll-backend` in your LLC GitHub account
- [ ] Push current backend code with multi-site support
- [ ] Verify all files are included (main.py, schemas, requirements.txt)

### **✅ Frontend Repositories**
- [ ] Create `youth-poll-frontend` repository
- [ ] Create `teen-poll-frontend` repository  
- [ ] Create `parents-poll-frontend` repository
- [ ] Create `schools-poll-frontend` repository
- [ ] Copy frontend code to each repository
- [ ] Update config.js in each repository for correct API endpoint

## **Phase 2: Render Services Setup**

### **✅ Backend Service**
- [ ] Connect `youth-poll-backend` repository to Render
- [ ] Create PostgreSQL database on Render
- [ ] Set environment variables (DATABASE_URL)
- [ ] Deploy and test backend API

### **✅ Frontend Services**
- [ ] Connect `youth-poll-frontend` to Render (youth site)
- [ ] Connect `teen-poll-frontend` to Render (teen site)
- [ ] Connect `parents-poll-frontend` to Render (parents site)
- [ ] Connect `schools-poll-frontend` to Render (schools site)
- [ ] Set environment variables for each frontend
- [ ] Deploy all frontend services

## **Phase 3: Namecheap DNS Configuration**

### **✅ CNAME Records**
- [ ] Add CNAME: `youth` → `youth-poll-backend.onrender.com`
- [ ] Add CNAME: `teen` → `teen-poll-backend.onrender.com`
- [ ] Add CNAME: `parents` → `parents-poll-backend.onrender.com`
- [ ] Add CNAME: `schools` → `schools-poll-backend.onrender.com`

### **✅ SSL Certificates**
- [ ] Verify SSL is provisioned for all subdomains
- [ ] Test HTTPS access to all sites

## **Phase 4: Database Setup**

### **✅ Production Database**
- [ ] Run setup_production_db.py on Render
- [ ] Import all CSV data (youth, teen, parents, schools)
- [ ] Verify site filtering works correctly
- [ ] Test API endpoints for each site

## **Phase 5: Testing & Verification**

### **✅ Site-Specific Testing**
- [ ] Test `youth.myworldmysay.com` - shows only youth content
- [ ] Test `teen.myworldmysay.com` - shows only teen content
- [ ] Test `parents.myworldmysay.com` - shows only parents content
- [ ] Test `schools.myworldmysay.com` - shows only schools content

### **✅ Cross-Site Verification**
- [ ] Verify youth site doesn't show teen content
- [ ] Verify teen site doesn't show youth content
- [ ] Verify responses are stored with correct site value
- [ ] Verify results are filtered by site

## **Phase 6: Content Management**

### **✅ CSV Data Verification**
- [ ] Verify categories.csv has all 4 sites
- [ ] Verify questions.csv has all 4 sites
- [ ] Verify options.csv has all 4 sites
- [ ] Verify blocks.csv has all 4 sites

### **✅ Site-Specific Content**
- [ ] Youth site: Healing, Defense, Family, Dream Era, School, Chaos
- [ ] Teen site: Love, Friends, etc.
- [ ] Parents site: Parenting, Family, etc.
- [ ] Schools site: Education, Learning, etc.

## **Repository Structure Verification**

### **✅ Backend Repository**
```
youth-poll-backend/
├── main.py                    # Multi-site API
├── requirements.txt           # Python dependencies
├── schema_setup.sql          # Database schema
├── schema_results.sql        # Results schema
├── import_setup.py          # Data import script
├── setup_production_db.py   # Production setup
└── data/
    ├── categories.csv        # All sites data
    ├── questions.csv         # All sites data
    ├── options.csv           # All sites data
    └── blocks.csv            # All sites data
```

### **✅ Frontend Repositories**
```
youth-poll-frontend/
├── src/
│   ├── config.js            # youth.myworldmysay.com/api
│   └── ...

teen-poll-frontend/
├── src/
│   ├── config.js            # teen.myworldmysay.com/api
│   └── ...

parents-poll-frontend/
├── src/
│   ├── config.js            # parents.myworldmysay.com/api
│   └── ...

schools-poll-frontend/
├── src/
│   ├── config.js            # schools.myworldmysay.com/api
│   └── ...
```

## **Final Verification Checklist**

### **✅ All Sites Working**
- [ ] youth.myworldmysay.com loads correctly
- [ ] teen.myworldmysay.com loads correctly
- [ ] parents.myworldmysay.com loads correctly
- [ ] schools.myworldmysay.com loads correctly

### **✅ Site Isolation**
- [ ] Each site shows only its own content
- [ ] Each site stores responses with correct site value
- [ ] Each site shows results filtered by site

### **✅ Performance**
- [ ] All sites load quickly
- [ ] API responses are fast
- [ ] Database queries are optimized

## **Troubleshooting Guide**

### **Common Issues**
1. **DNS not working**: Check CNAME records in Namecheap
2. **API errors**: Check Render logs and environment variables
3. **Site mixing**: Verify site filtering in backend
4. **Frontend not loading**: Check build logs in Render

### **Debug Commands**
```bash
# Test DNS
dig youth.myworldmysay.com
dig teen.myworldmysay.com
dig parents.myworldmysay.com
dig schools.myworldmysay.com

# Test API endpoints
curl https://youth.myworldmysay.com/api/categories
curl https://teen.myworldmysay.com/api/categories
curl https://parents.myworldmysay.com/api/categories
curl https://schools.myworldmysay.com/api/categories
```

## **Next Steps After Deployment**

1. **Monitor**: Check Render dashboards regularly
2. **Backup**: Set up database backups
3. **Analytics**: Add site-specific analytics
4. **Content**: Add more content for each site
5. **Marketing**: Set up site-specific marketing campaigns
