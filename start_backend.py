#!/usr/bin/env python3
import os
import subprocess
import sys

# Change to the backend directory
os.chdir('backend')

# Start uvicorn
cmd = [
    'uvicorn', 
    'main:app', 
    '--host', '0.0.0.0', 
    '--port', os.environ.get('PORT', '8000')
]

print(f"Starting uvicorn with command: {' '.join(cmd)}")
print(f"Current directory: {os.getcwd()}")

# Run uvicorn
subprocess.run(cmd)
