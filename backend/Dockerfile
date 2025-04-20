# Use a Python slim image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies and pip if needed
RUN apt-get update && apt-get install -y python3 python3-pip build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements.txt to the container
COPY requirements.txt .

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Install the spaCy model
RUN python3 -m spacy download en_core_web_sm

# Copy the rest of the app code into the container
COPY . .

# Expose the port that the app will run on
EXPOSE 8080

# Command to run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
