# FROM python:3.10-slim

# WORKDIR /qr_challenge

# RUN apt-get update && apt-get install -y \
#     libpq-dev gcc \
#     && rm -rf /var/lib/apt/lists/*

# COPY requirements.txt .
# RUN pip install --upgrade pip
# RUN pip install --no-cache-dir -r requirements.txt

# COPY . .

# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]