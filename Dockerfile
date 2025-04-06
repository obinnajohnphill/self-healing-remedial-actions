# Dockerfile.ubuntu - updated with ADB and correct syntax

FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

RUN apt-get update && apt-get install -y \
    curl \
    wget \
    unzip \
    tzdata \
    sudo \
    python3 \
    python3-pip \
    systemd \
    && apt-get clean

# Install Android ADB tools
RUN apt-get install -y android-tools-adb

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY self-healing-trigger/ ./self-healing-trigger/

EXPOSE 8000

CMD ["python3", "self-healing-trigger/classify-errors-and-trigger-self-healing.py"]
