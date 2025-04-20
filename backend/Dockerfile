FROM python:3.12-slim

# Install system dependencies including Xvfb
RUN apt-get update && apt-get install -y \
    xvfb \
    && rm -rf /var/lib/apt/lists/*
RUN apt-get update && apt-get install -y xvfb

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your app code
COPY . /app
WORKDIR /app

CMD ["flask", "run"]
