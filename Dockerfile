FROM ubuntu:20.04

# Set the working directory
WORKDIR /app

# Add adb for Android
RUN apt-get update && apt-get install -y adb

# Install necessary tools
RUN apt-get update && apt-get install -y tzdata sudo systemd && apt-get clean

# Install Python
RUN apt-get install -y python3 python3-pip

# Install dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the script
COPY self-healing-trigger/ ./self-healing-trigger/

CMD ["python3", "self-healing-trigger/classify-errors-and-trigger-self-healing.py"]
