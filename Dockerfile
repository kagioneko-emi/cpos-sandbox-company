# Base image
FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose the port (HTTPS is handled by Azure Container Apps ingress)
EXPOSE 8001

# Run the dashboard
CMD ["uvicorn", "dashboard:app", "--host", "0.0.0.0", "--port", "8001"]
