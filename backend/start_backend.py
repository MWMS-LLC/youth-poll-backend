#!/usr/bin/env python3
import os
import subprocess
import sys

# Start uvicorn
cmd = ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", os.environ.get("PORT", "8000")]

# Ensure we're in the right directory for imports
if os.getcwd().endswith('/backend'):
    # We're in /app/backend, main.py is in the same directory
    pass
else:
    # We're in /app, need to change to backend directory
    os.chdir('backend')

print("Starting uvicorn with command:", " ".join(cmd))
print("Current directory:", os.getcwd())

# Run uvicorn
subprocess.run(cmd)
