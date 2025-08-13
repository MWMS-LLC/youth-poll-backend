#!/usr/bin/env python3
"""
Start script for Render deployment
This file tells Render how to start the backend service
"""

import uvicorn
from main import app

if __name__ == "__main__":
    # Render expects the app to run on port 10000
    # and bind to all interfaces (0.0.0.0)
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=10000,
        reload=False  # Disable reload in production
    )
