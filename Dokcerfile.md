# Dockerfile.md

# Detailed Explanation of Your Dockerfile

This document explains each section of your Dockerfile, why it exists, and how it contributes to building a containerized scraping environment using Python, Selenium, and Chromium.

---

## 1. Base Image

```dockerfile
FROM python:3.12-slim AS base
```

* Uses Python 3.12 slim image as the base.
* `slim` is lightweight and contains minimal packages, reducing image size.
* `AS base` names the build stage, useful for multi-stage builds.

**Purpose:** Provides a minimal Python environment for your scraping project.

---

## 2. Environment Variables

```dockerfile
ENV PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive \
    PIP_NO_CACHE_DIR=off \
    CHROME_BIN=/usr/bin/chromium \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8
```

* `PYTHONUNBUFFERED=1`: Ensures Python logs print in real-time.
* `DEBIAN_FRONTEND=noninteractive`: Avoids interactive prompts during package installation.
* `PIP_NO_CACHE_DIR=off`: Controls pip caching.
* `CHROME_BIN`: Path to Chromium for Selenium.
* `LANG` and `LC_ALL`: Set UTF-8 locale to handle unicode characters.

**Purpose:** Ensures consistent environment behavior, proper text handling, and smooth Selenium integration.

---

## 3. Install System Dependencies

```dockerfile
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget curl unzip gnupg ca-certificates \
    fonts-liberation libnss3 libxss1 libasound2 \
    libatk-bridge2.0-0 libgtk-3-0 libx11-xcb1 \
    libxcomposite1 libxcursor1 libxdamage1 libxi6 \
    libxtst6 xdg-utils \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
```

* Installs packages required for:

  * Downloading (`wget`, `curl`)
  * Extracting files (`unzip`)
  * Chromium dependencies (`libgtk-3-0`, `libnss3`, etc.)
* `--no-install-recommends`: Installs only essential packages.
* Cleans up temporary files to reduce image size.

**Purpose:** Provides all system-level dependencies required to run Chromium and scraping tools.

---

## 4. Install Chromium Browser

```dockerfile
RUN apt-get update && apt-get install -y --no-install-recommends chromium \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
```

* Installs Chromium, the open-source version of Chrome.
* Cleans up after installation.

**Purpose:** Allows Selenium to automate browser actions for scraping.

---

## 5. Install ChromeDriver Matching Chromium

```dockerfile
RUN CHROME_VERSION=$(chromium --version | awk '{print $2}' | cut -d. -f1-3) && \
    wget -qO /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/${CHROME_VERSION}/chromedriver_linux64.zip && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin/ && \
    rm /tmp/chromedriver.zip && \
    chmod +x /usr/local/bin/chromedriver
```

* Gets Chromium version and extracts major.minor.patch.
* Downloads matching ChromeDriver from Google.
* Unzips and places it in `/usr/local/bin/`.
* Sets executable permissions.

**Purpose:** Ensures Selenium works correctly by matching ChromeDriver to the installed Chromium version.

---

## 6. Set Working Directory

```dockerfile
WORKDIR /app
```

* Sets `/app` as the working directory inside the container.
* All subsequent commands (copy, run, CMD) execute relative to this path.

**Purpose:** Organizes project files inside the container.

---

## 7. Install Python Dependencies

```dockerfile
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install -r requirements.txt
```

* Copies only `requirements.txt` first to leverage Docker caching.
* Upgrades pip.
* Installs Python libraries (e.g., Selenium, BeautifulSoup, Requests).

**Purpose:** Prepares Python environment with all necessary packages for scraping and data processing.

---

## 8. Copy Application Code

```dockerfile
COPY . .
```

* Copies your entire project into `/app`.

**Purpose:** Makes your scraping scripts and project files available inside the container.

---

## 9. Default Command

```dockerfile
CMD ["python", "main.py"]
```

* Runs `main.py` by default when the container starts.
* Can be overridden at runtime if needed.

**Purpose:** Automatically starts your scraping script inside the container.

---

## ✅ Summary

1. Start with lightweight Python base.
2. Set environment variables for Python and Selenium.
3. Install Chromium + system dependencies.
4. Install matching ChromeDriver.
5. Install Python packages efficiently using caching.
6. Copy your code and set working directory.
7. Define default command for scraping execution.

This setup ensures a **reproducible, production-ready scraping environment** for collecting real estate data or any other web automation tasks using Selenium and Python.
