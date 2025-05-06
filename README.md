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
```
Push to Docker Hub: 
```bash
docker tag todo-app yourusername/todo-app
docker push yourusername/todo-app
```
### Step 2: Kubernetes Manifests
Creating deployment.yaml and service.yaml
### Step 3: CI/CD Pipeline
.github/workflows/deploy.yml
### Step 4: Deployment
For Minikube:
```bash
minikube start
kubectl apply -f k8s/
minikube service django-service
```
