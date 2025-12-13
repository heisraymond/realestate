 # Official python image from Docker Hub
FROM python

# # Installing required system dependencies
# #RUN apt-get update && apt-get install -y \
#     wget \
#     curl \
#     unzip \
#     chromium-driver \
#     && apt-get clean

# # The working directory
# WORKDIR /app

# # Copy the requirements.txt file first
# COPY requirements.txt /app/

# # Install Python dependencies
# RUN pip install --no-cache-dir -r requirements.txt

# # Copying scripts into the container
# COPY . /app

# # Environment variables to avoid Chrome headless mode errors
# ENV DISPLAY=:99
# ENV PYTHONUNBUFFERED=1

# # Command to run the script
# CMD ["python", "main.py"]
