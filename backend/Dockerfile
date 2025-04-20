# Use an official Python image as the base image
FROM python:3.12-slim

# Install system dependencies and Google Chrome
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    libnss3 \
    libgdk-pixbuf2.0-0 \
    libasound2 \
    libx11-xcb1 \
    libxtst6 \
    libgtk-3-0 \
    libxss1 \
    libxcomposite1 \
    libgdk-pixbuf2.0-0 \
    ca-certificates \
    fonts-liberation \
    libappindicator3-1 \
    libpangocairo-1.0-0 \
    xdg-utils \
    google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Install required Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variable for headless Chrome
ENV DISPLAY=:99

# Expose necessary ports
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]
