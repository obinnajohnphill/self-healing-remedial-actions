<p align="center">
  <img src="cross-logo-dark.png" alt="CROSS Logo" width="250"/>
</p>

<h1 align="center">CROSS</h1>
<p align="center"><strong>Cross-platform Remediation and Observability Self-Healing System</strong></p>

<p align="center">
  <em>An intelligent, ML-driven self-healing framework for Android, Linux, macOS, and Windows, integrating real-time observability and automated cross-platform remediation.</em>
</p>

This repository contains an implementation of a self-healing system that performs automated remedial actions (e.g., system updates, service restarts, and resource optimisation) upon detecting anomalies in system logs.

---

## Features

- **Log Analysis** — Detects errors and warnings from system logs.
- **Automated Remedial Actions** — Executes actions such as restarting services, system updates, and resource clean-up.
- **Modular Design** — Built with Python scripts for flexibility and ease of use.
- **Dockerised Environment** — Easily deployable using Docker.
- **Kubernetes Support** — Optional cluster deployment for scalability and fault tolerance.
- **Grafana Monitoring** — Track metrics and remediation actions with Grafana dashboards.

---

## 📁 Dataset

The preprocessed dataset used for experiments (multi-platform logs + features) is available on Zenodo:

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.15249598.svg)](https://doi.org/10.5281/zenodo.15249598)  
**CROSS Dataset:** Multi-Platform System Logs and Preprocessed Data for Self-Healing Evaluation.

> **Source datasets:** derived from the Loghub collection curated by LOGPAI (ISSRE 2023). See <https://github.com/logpai/loghub> for terms and citation.

---

## 🔁 Reproducibility (No Code Changes)

CROSS expects the **preprocessed logs** to be available inside the repository at:

```
self-healing-trigger/dataset/system-logs/multiple-system-log-dataset/preprocessed-data
```

Create the folders and place the CSVs from the Zenodo DOI there.

```bash
# from the repo root
mkdir -p self-healing-trigger/dataset/system-logs/multiple-system-log-dataset/preprocessed-data
# copy your downloaded CSVs into that 'preprocessed-data' folder
```

### Option A — Docker (recommended)

Build and run without modifying project files. Bind-mount the dataset folder so the container sees the expected path:

```bash
# build
docker build -t self-healing-app .

# run (read-only mount of the dataset)
docker run --rm -it   -v "$(pwd)/self-healing-trigger/dataset/system-logs/multiple-system-log-dataset/preprocessed-data:/app/self-healing-trigger/dataset/system-logs/multiple-system-log-dataset/preprocessed-data:ro"   self-healing-app
```

### Option B — Docker Compose (keep repo pristine)

Create a **local** override file (untracked) to inject the dataset mount:

```yaml
# docker-compose.local.yaml  (do not commit)
services:
  app:
    volumes:
      - ./self-healing-trigger/dataset/system-logs/multiple-system-log-dataset/preprocessed-data:/app/self-healing-trigger/dataset/system-logs/multiple-system-log-dataset/preprocessed-data:ro
```

Run with both files:

```bash
docker compose -f docker-compose.yaml -f docker-compose.local.yaml up -d --build
```

### Sanity checks

- The container should **not** error with “file/dir not found”.  
- `docker logs <container>` should show it picked up files from `/app/self-healing-trigger/dataset/system-logs/multiple-system-log-dataset/preprocessed-data`.  
- If enabled, a metrics endpoint will be printed in the logs.

---

## Architectural Overview

<p align="center">
  <img src="proposed_system600.png" alt="CROSS Architecture Diagram" width="100%"/>
</p>

**Figure**: *Architectural Overview of the CROSS Framework.*  
A modular design showing OS-specific execution paths and threshold-driven remediation triggers. The system integrates anomaly detection, log vectorisation, rule-based evaluation, and a unified dispatcher to automate recovery actions across Android, Linux, macOS, and Windows. Metrics are exported to Prometheus and visualised via Grafana.

---

## Prerequisites

- **Python** ≥ 3.9  
- **Docker & Docker Compose**  
- **Kubernetes** (optional, for cluster deployment)  
- **Git**

---

## Setup

```bash
git clone <repository-url>
cd <repository-folder>

# prepare dataset folder
mkdir -p self-healing-trigger/dataset/system-logs/multiple-system-log-dataset/preprocessed-data
# copy Zenodo CSVs into that folder
```

---

## Running the Self-Healing System, Grafana, and Prometheus

### 1) Build the Docker image

```bash
docker build -t self-healing-app .
# or without cache:
# docker build --no-cache -t self-healing-app .
```

### 2) Run the container (dataset mount)

```bash
docker run --rm -it   -v "$(pwd)/self-healing-trigger/dataset/system-logs/multiple-system-log-dataset/preprocessed-data:/app/self-healing-trigger/dataset/system-logs/multiple-system-log-dataset/preprocessed-data:ro"   self-healing-app
```

### 3) Start the full stack with Docker Compose

```bash
docker compose up -d
# classic syntax: docker-compose up -d
```

This typically starts:
- **Self-Healing System** (log processing + remediation)
- **Prometheus** (metrics collection)
- **Grafana** (visualisation)

### 4) Access dashboards

- **Prometheus:** <http://localhost:9090>  
- **Grafana:** <http://localhost:3000>  
  - Default credentials: `admin / admin` (change after first login)

### 5) Logs & lifecycle

```bash
docker compose logs -f
docker compose ps
docker compose down
```

### 6) Add Prometheus as a data source in Grafana

1. Grafana → **Configuration** → **Data Sources** → **Add data source**  
2. Choose **Prometheus**  
3. URL: `http://prometheus:9090`  
4. **Save & Test**, then build dashboards.

### 7) Import a sample Grafana dashboard

- Grafana Labs ID **315** (or any preferred dashboard)
- Select Prometheus as data source → **Import**

---

## Kubernetes Deployment (optional)

```bash
# start a local cluster (e.g., Minikube)
minikube start
kubectl get nodes -o wide
```

Install Prometheus/Grafana via Helm (example):

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

kubectl create namespace monitoring
helm install prometheus prometheus-community/prometheus -n monitoring
kubectl get pods -n monitoring
```

Deploy the application:

```bash
kubectl apply -f deployment.yaml
kubectl get pods
```

Expose services as needed (NodePort/Ingress).

---

## File Structure

```
.
├── self-healing-trigger/
│   ├── classify-errors-and-trigger-self-healing.py
│   ├── dataset/
│   │   └── system-logs/multiple-system-log-dataset/preprocessed-data/   # ← put CSVs here
│   └── ...
├── requirements.txt
├── Dockerfile
├── deployment.yaml
├── docker-compose.yaml
├── prometheus.yml
├── README.md
```

> If you run into a “missing file/directory” message, ensure the **preprocessed-data** folder exists and contains CSVs from the Zenodo DOI.

---

## Licence

MIT — see `LICENSE`.
