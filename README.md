# Fitlog on Kubernetes

Designing, containerizing, and deploying a microservice on Kubernetes.

## Django Kubernetes Deployment Guide:

### Prerequisites
- Docker installed  
- Kubernetes cluster (Minikube for local testing)  
- kubectl configured  

### Step 1: Containerize the Django App
Create `app/Dockerfile`  
Build and test locally:
```bash
docker build -t django-app -f app/Dockerfile ./app
docker run -p 8000:8000 django-app
