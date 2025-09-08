# Use official Python image
FROM python:3.9-slim

# Accept AccuWeather key as build argument
ARG ACCU_API_KEY
ENV ACCU_API_KEY=$ACCU_API_KEY

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY app.py .

# Expose port
EXPOSE 5000

# Run app
CMD ["python", "app.py"]
