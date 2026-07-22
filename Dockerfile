FROM python:3.12-slim

WORKDIR /app

# Install system dependencies for oracledb and matplotlib
RUN apt-get update && apt-get install -y --no-install-recommends \
    libaio1 \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd --create-home botuser

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p logs && chown -R botuser:botuser /app
USER botuser

CMD ["python", "main.py"]
