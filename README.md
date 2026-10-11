# Kubernetes-Based Sales Analytics API

A Flask REST API connected to PostgreSQL, containerized with Docker and deployed to Kubernetes using Docker Desktop.

## Project Overview

This project extends a containerized Sales Analytics API by introducing Kubernetes deployment, resource management, health probes, autoscaling configuration, and pod recovery testing.

## Features

- REST API for sales records and analytics
- Flask and PostgreSQL integration
- Docker image for the API
- Kubernetes Deployment with two replicas
- CPU and memory requests and limits
- Readiness and liveness probe configuration
- Horizontal Pod Autoscaler (HPA)
- Metrics Server monitoring
- Pod recovery testing

## Tech Stack

- Python and Flask
- PostgreSQL
- Docker and Docker Compose
- Kubernetes and kubectl
- Metrics Server
- PowerShell

## Architecture

PowerShell Client → Kubernetes Service → Flask API Pods → PostgreSQL

The API runs in Kubernetes. PostgreSQL remains in Docker Compose and is accessed through `host.docker.internal` in the local Docker Desktop environment.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Check API and database connectivity |
| GET | `/sales` | Retrieve sales records |
| POST | `/sales` | Add a sales record |
| GET | `/summary` | Calculate sales metrics |

## Kubernetes Configuration

The `k8s/` directory contains:

- `sales-api-deployment.yaml` — API deployment, resource limits, probes, and database configuration.
- `sales-api-hpa.yaml` — CPU-based horizontal autoscaling configuration.

## Verify the Deployment

Check Kubernetes resources:

```powershell
kubectl get deployments
kubectl get pods
kubectl get services
kubectl get hpa
```

Check resource usage:

```powershell
kubectl top pods
```

Inspect deployment details:

```powershell
kubectl describe deployment sales-api
```

## Access the API Locally

Start port forwarding in one terminal:

```powershell
kubectl port-forward service/sales-api 5001:5000
```

In a second terminal, test the endpoints:

```powershell
Invoke-RestMethod http://localhost:5001/health
Invoke-RestMethod http://localhost:5001/sales
Invoke-RestMethod http://localhost:5001/summary
```

## Learning Outcomes

- Deploying containerized applications to Kubernetes
- Managing replicas and application resources
- Configuring readiness and liveness probes
- Understanding horizontal pod autoscaling
- Monitoring CPU and memory usage
- Testing Kubernetes pod recovery
- Connecting a Kubernetes application to a database running outside the cluster

## Local Development Note

The Kubernetes manifests are intended for the local Docker Desktop environment used during development. Configure the required Kubernetes Secret and verify the database connection before applying the manifests. Do not commit passwords, tokens, or other secrets to GitHub.
