#!/usr/bin/env python3
"""
Local Development Startup Script
This script loads the local environment and starts the backend server
"""

import os
from dotenv import load_dotenv
import uvicorn

# Load local environment variables
load_dotenv('env.local')

# Set default values for local development
if not os.getenv('DATABASE_URL'):
    os.environ['DATABASE_URL'] = 'postgresql://localhost/mwms_local_db'
if not os.getenv('DEBUG'):
    os.environ['DEBUG'] = 'true'

print("🚀 Starting Youth Poll Backend (Local Development)")
print(f"📊 Database: {os.getenv('DATABASE_URL')}")
print(f"🐛 Debug: {os.getenv('DEBUG')}")
print("=" * 50)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
