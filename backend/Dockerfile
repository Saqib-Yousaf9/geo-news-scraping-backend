# Use official Python base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Download the spaCy language model
RUN python -m spacy download en_core_web_sm

# Copy your app code
COPY . .

# Command to run your app
CMD ["python", "app.py"]
