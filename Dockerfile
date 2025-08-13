# Use Python 3.11 with Rust support
FROM rust:1.75-slim as rust-builder

# Install Python and build tools
RUN apt-get update && apt-get install -y \
    python3.11 \
    python3.11-dev \
    python3.11-distutils \
    python3-pip \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Set up Python
RUN python3.11 -m pip install --upgrade pip

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Set working directory
WORKDIR /app

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
