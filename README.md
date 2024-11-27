# My Multi-Platform Cross-Posting Application

This repository contains multiple services, each in its own directory, and a root `docker-compose.yaml` to orchestrate them.

## Services

- **Crosspost Application** (`app/`): A Flask application to cross-post content between social media platforms.
- **Other Service 1** (`other_service1/`): Description of other service 1.
- **Other Service 2** (`other_service2/`): Description of other service 2.

## Deployment

### Deploy All Services

To deploy all services defined in the root `docker-compose.yaml`:

```bash
docker-compose up --build
``` 

To deploy the crosspost application as a microservice:

```bash
cd app
docker-compose -f docker-compose.crosspost.yaml up --build
``` 

## Environment Variables

Each service has its own .example.env file in its directory. Copy this file to .env and fill in the required values.

`cp app/.example.env app/.env`

## Directory Structure

``` 
Cdaprod/social-media-crosspost-tool/.
├── docker-compose.yaml
├── app
│   ├── Dockerfile
│   ├── docker-compose.crosspost.yaml
│   ├── requirements.txt
│   ├── main.py
│   ├── config.py
│   ├── __init__.py
│   ├── tasks.py
│   ├── rate_limiter.py
│   ├── utils.py
│   ├── threads.py
│   ├── templates
│   │   └── index.html
│   ├── api
│   │   ├── __init__.py
│   │   ├── crosspost.py
│   │   ├── threads_endpoints.py
│   │   └── health.py
│   ├── tests
│   │   └── test_app.py
│   └── .example.env
├── other_service1
│   ├── Dockerfile
│   └── docker-compose.other_service1.yaml
├── other_service2
│   ├── Dockerfile
│   └── docker-compose.other_service2.yaml
├── docs
│   ├── 00-CLUSTERING-MINIO.md
│   └── 01-PROVISION-KUBERNETES-STORAGE.md
└── README.md
``` 

## Usage

- API Documentation: Accessible at /swagger/ when the application is running.
- Health Check: Endpoint available at /health/.
- Crosspost Endpoint: /crosspost/ accepts POST requests to cross-post content.
- Threads Endpoints: Under /threads/ for managing threads.