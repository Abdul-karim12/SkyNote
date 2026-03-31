
## Key details

- API runs inside a Docker container using Gunicorn
- Exposed on port 80 with proper port mapping (80 → 5000)
- Deployed on a Linux EC2 instance with security group configuration
- Infrastructure created using Terraform (VPC, subnet, security group)
- Handles HTTP requests publicly with a working health endpoint

# SkyNote

I built SkyNote as a simple cloud-based notes API to practice real-world deployment using AWS and Docker.

The app is written in Flask, containerized with Docker, and deployed on an EC2 instance. Infrastructure is managed using Terraform, and Kubernetes configs are included for future scaling.

## Live API

http://98.80.138.253

Health check:
http://98.80.138.253/health


## What I used

- Flask (Python)
- Docker
- AWS EC2
- Terraform
- Kubernetes (setup files included)


## What this project shows

- I can deploy a backend service to the cloud
- I understand Docker and container workflows
- I can manage infrastructure with Terraform
- I can expose a public API and keep it running


## How it runs

I build the Docker image locally, push it to Docker Hub, then pull and run it on an EC2 instance using port 80.


# SkyNote

I built SkyNote as a simple cloud-based notes API to practice real-world deployment using AWS and Docker.

The app is written in Flask, containerized with Docker, and deployed on an EC2 instance. Infrastructure is managed using Terraform, and Kubernetes configs are included for future scaling.

## Live API

http://98.80.138.253

Health check:
http://98.80.138.253/health
---
## What I used

- Flask (Python)
- Docker
- AWS EC2
- Terraform
- Kubernetes (setup files included)

## What this project shows

- I can deploy a backend service to the cloud
- I understand Docker and container workflows
- I can manage infrastructure with Terraform
- I can expose a public API and keep it running

## How it runs

I build the Docker image locally, push it to Docker Hub, then pull and run it on an EC2 instance using port 80.

## Project structure

app/         Flask API
terraform/   AWS infrastructure setup
kubernetes/  deployment configs
scripts/     setup scripts

## Status

Running live on AWS EC2.
