FROM python:3.11-slim

WORKDIR /app

# Install PostgreSQL client
RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

# Copy shared root requirements file
COPY requirements.txt .
# Install all dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy service-specific code
COPY . .

# Make wait-for-db.sh executable
RUN chmod +x /app/wait-for-db.sh

ENV PYTHONUNBUFFERED=1

# Run FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]