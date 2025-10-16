FROM python:3.9-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV FLASK_HOST=0.0.0.0
ENV FLASK_PORT=8080

# Expose port
EXPOSE 8080

# Run the application
CMD ["python", "main.py", "start"]
