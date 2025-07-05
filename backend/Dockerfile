# Use an official Python slim image as the base image
FROM python:3.10-slim AS base

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# # Create a non-root user
# RUN useradd -m appuser

# Copy and install dependencies
COPY requirements.txt .

# # Run the install script to set up the environment
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY app /app    
# COPY {python file name} {relative location}

# Change ownership of the application folder to the non-root user
# RUN chown -R appuser:appuser /app
# RUN chown -R appuser:appuser /app/uploads /app/output

# Switch to the non-root user
# USER appuser

# Expose the application port
EXPOSE 8000

# # Set environment variables for Flask and Python
# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1
# ENV FLASK_APP=app/app.py
# ENV FLASK_ENV=production

# Run the Flask application
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
