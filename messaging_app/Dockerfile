# 1. Base Image
FROM python:3.10-slim

# 2. Environment Variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Work Directory
WORKDIR /app

# 4. Install COMPREHENSIVE System Dependencies -p
# build-essential: Includes gcc, make, and core compilers
# pkg-config: Helps Python find system libraries
# default-libmysqlclient-dev: Required for MySQL drivers
# libpq-dev: Required for PostgreSQL drivers
# libyaml-dev: Required for PyYAML
# libffi-dev: Required for Cryptography/PyJWT
RUN apt-get update && apt-get install -y \
    build-essential \
    pkg-config \
    default-libmysqlclient-dev \
    libpq-dev \
    libyaml-dev \
    libffi-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# 5. Non-root user setup
RUN addgroup --system appgroup && adduser --system --group appuser

# 6. Install Python Dependencies
COPY requirements.txt /app/
# Increased timeout to handle slow compilations
RUN pip install --no-cache-dir --default-timeout=100 -r requirements.txt

# 7. Copy Code
COPY . /app/
RUN chown -R appuser:appgroup /app

# 8. User & Port
USER appuser
EXPOSE 8000

# 9. Run
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]