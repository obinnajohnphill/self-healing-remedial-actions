
# Self-Healing Remedial Actions

This repository contains an implementation of a self-healing system that performs automated remedial actions (e.g., system updates, service restarts, and resource optimization) upon detecting anomalies in system logs.

## Features

- **Log Analysis**: Detects errors and warnings from system logs.
- **Automated Remedial Actions**: Executes actions such as restarting services, system updates, and resource cleanup.
- **Modular Design**: Built with Python scripts for flexibility and ease of use.
- **Dockerized Environment**: Easily deployable using Docker.
- **Kubernetes Support**: Deploy the application to a Kubernetes cluster for scalability and fault tolerance.

---

## Prerequisites

Before setting up the application, ensure the following tools are installed:

1. **Python**: Version 3.9 or above
2. **Docker**: Installed and running
3. **Kubernetes**: Installed and configured
4. **Git**: To clone the repository

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-folder>
```

### 2. Build and Run with Docker

1. **Build the Docker Image**:

   ```bash
   docker build -t self-healing-app .
   ```

2. **Run the Container**:

   ```bash
   docker run --rm -it self-healing-app
   ```

The application will automatically start analyzing logs and executing remedial actions.

---

## Kubernetes Deployment

### 1. Start Kubernetes

If you’re using Minikube, start the cluster:

```bash
minikube start
```

For OrbStack, ensure Kubernetes is enabled and running. Verify the node is ready:

```bash
kubectl get nodes -o wide
```

You should see output similar to this:

```plaintext
NAME       STATUS   ROLES                  AGE    VERSION        INTERNAL-IP    EXTERNAL-IP   OS-IMAGE   KERNEL-VERSION                        CONTAINER-RUNTIME
orbstack   Ready    control-plane,master   2m7s   v1.29.3+orb1   198.19.249.2   <none>        OrbStack   6.11.6-orbstack-00279-g28c6c77332e6   docker://27.3.1
```

### 2. Deploy the Application

1. Apply the deployment configuration:

   ```bash
   kubectl apply -f deployment.yaml
   ```

2. Verify the deployment and pods:

   ```bash
   kubectl get pods
   ```

3. Expose the service using NodePort:

   ```bash
   kubectl expose pod nginx --type=NodePort --port=80
   ```

### 3. Access the Service

1. Get the service details:

   ```bash
   kubectl get svc nginx
   ```

   Example output:

   ```plaintext
   NAME    TYPE       CLUSTER-IP      EXTERNAL-IP   PORT(S)        AGE
   nginx   NodePort   10.96.0.1       <none>        80:31234/TCP   2m
   ```

2. Access the service at `http://<INTERNAL-IP>:<NodePort>`. For OrbStack, replace `<INTERNAL-IP>` with `198.19.249.2` (from `kubectl get nodes`) and `<NodePort>` with the service port (e.g., `31234`).

   Example:

   ```bash
   curl http://198.19.249.2:31234
   ```

   You should see the Nginx welcome page if the service is running correctly.

---

## Troubleshooting

1. **Pod Not Running**: Check pod logs for errors:

   ```bash
   kubectl logs <pod-name>
   ```

2. **Service Not Accessible**: Ensure the NodePort is open and the Kubernetes configuration allows external traffic.

3. **Restart Kubernetes Services**: For OrbStack, restart Kubernetes or Docker Desktop if needed:

   ```bash
   minikube stop
   minikube start
   ```

---

## File Structure

```
.
├── self-healing-trigger/
│   ├── classify-errors-and-trigger-self-healing.py
│   ├── dataset/
│   │   ├── <log files>
│   ├── <other scripts>
├── requirements.txt
├── Dockerfile
├── deployment.yaml
├── README.md
```

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.
