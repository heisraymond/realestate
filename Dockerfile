# ============================
# Base Image
# ============================
FROM python:3.12-slim AS base

# ============================
# Environment Variables
# ============================
ENV PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive \
    PIP_NO_CACHE_DIR=off \
    CHROME_BIN=/usr/bin/chromium \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8

# ============================
# Install System Dependencies
# ============================
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    curl \
    unzip \
    gnupg \
    ca-certificates \
    fonts-liberation \
    libnss3 \
    libxss1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libx11-xcb1 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxi6 \
    libxtst6 \
    xdg-utils \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# ============================
# Install Chromium and ChromeDriver
# ============================
RUN apt-get update && apt-get install -y --no-install-recommends \
    chromium \
    chromium-driver \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# ============================
# Set Working Directory
# ============================
WORKDIR /app

# ============================
# Install Python Dependencies
# ============================
# Copy only requirements first for caching
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# ============================
# Copy Application Code
# ============================
COPY . .

# ============================
# Default Command
# ============================
CMD ["python", "main.py"]
