# Youth Poll Deployment Guide

## **Domain Setup (Namecheap)**

### **1. DNS Configuration**
1. Log into your Namecheap account
2. Go to domain management for `myworldmysay.com`
3. Add **CNAME record**:
   - **Host**: `youth`
   - **Value**: `your-render-app-name.onrender.com` (we'll get this from Render)
   - **TTL**: Automatic

### **2. SSL Certificate**
- Namecheap will automatically provision SSL for `youth.myworldmysay.com`
- This ensures HTTPS works correctly

## **GitHub Repository Setup**

### **1. Create New Repository**
```bash
# In your LLC GitHub account
# Create: youth-poll-backend
# Create: youth-poll-frontend
```

### **2. Push Current Code**
```bash
# Backend
cd backend
git init
git add .
git commit -m "Initial youth poll backend with multi-site support"
git remote add origin https://github.com/your-llc-account/youth-poll-backend.git
git push -u origin main

# Frontend  
cd ../frontend
git init
git add .
git commit -m "Initial youth poll frontend with multi-site support"
git remote add origin https://github.com/your-llc-account/youth-poll-frontend.git
git push -u origin main
```

## **Render Deployment**

### **1. Backend Service (Web Service)**
1. Connect GitHub repository: `youth-poll-backend`
2. **Build Command**: `pip install -r requirements.txt`
3. **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. **Environment Variables**:
   ```
   DATABASE_URL=postgresql://your-render-db-url
   ```

### **2. Frontend Service (Static Site)**
1. Connect GitHub repository: `youth-poll-frontend`
2. **Build Command**: `npm install && npm run build`
3. **Publish Directory**: `dist`
4. **Environment Variables**:
   ```
   VITE_API_BASE_URL=https://youth.myworldmysay.com/api
   ```

### **3. Database Service**
1. Create PostgreSQL database on Render
2. Note the connection string for backend environment variable

## **Production Configuration**

### **1. Backend Environment**
The backend will automatically detect the site from the request headers:
- `X-Site: youth` (default)
- All responses filtered by site

### **2. Frontend Environment**
The frontend is configured to:
- Use `youth.myworldmysay.com/api` in production
- Use `localhost:8000` in development
- Display only youth content

### **3. Site-Specific Features**
- **Content**: Only youth categories, questions, and options
- **Responses**: All votes stored with `site = 'youth'`
- **Results**: Filtered by youth site only

## **Testing Production**

### **1. Before DNS Update**
- Test Render services directly using their URLs
- Verify backend API endpoints work
- Verify frontend builds and serves correctly

### **2. After DNS Update**
- Visit `https://youth.myworldmysay.com`
- Test complete user flow
- Verify site filtering works correctly

## **Multi-Site Expansion**

### **Future Sites**
When ready to add other sites:
1. **teen.myworldmysay.com**: Update frontend config to use teen site
2. **parents.myworldmysay.com**: Create new frontend with parents site
3. **schools.myworldmysay.com**: Create new frontend with schools site

### **Shared Backend**
- All sites use the same backend API
- Site filtering handled by `X-Site` header
- Database shared but responses separated by site

## **Monitoring & Maintenance**

### **1. Render Dashboard**
- Monitor service health
- Check logs for errors
- Scale resources as needed

### **2. Database Management**
- Regular backups
- Monitor performance
- Check site-specific data integrity

## **Security Considerations**

### **1. Environment Variables**
- Keep database URLs secure
- Use Render's environment variable system
- Never commit secrets to GitHub

### **2. CORS Configuration**
- Backend configured to accept requests from `youth.myworldmysay.com`
- Frontend configured to only call authorized API endpoints

## **Troubleshooting**

### **Common Issues**
1. **DNS not working**: Check CNAME record in Namecheap
2. **API errors**: Check Render logs and environment variables
3. **Site filtering issues**: Verify `X-Site` header is being sent
4. **Database connection**: Verify DATABASE_URL in Render environment

### **Debug Steps**
1. Check Render service logs
2. Verify DNS propagation with `dig youth.myworldmysay.com`
3. Test API endpoints directly
4. Check browser console for frontend errors
