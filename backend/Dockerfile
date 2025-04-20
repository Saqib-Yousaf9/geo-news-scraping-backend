# Use an official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies if needed (optional)
RUN apt-get update && apt-get install -y gcc

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# ✅ Download the spaCy model
RUN python -m spacy download en_core_web_sm

# Copy the rest of your app
COPY . .

# Run the app
CMD ["python", "app.py"]
