# Use Python slim image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Download spaCy model
RUN python -m spacy download en_core_web_sm

# Copy the rest of your app code
COPY . .

# Expose the port Railway listens on
EXPOSE 5000

# Command to run your app (adjust based on your app setup)
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
