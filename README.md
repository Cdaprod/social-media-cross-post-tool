# My Multi-Service Application

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

Environment Variables

Each service has its own .example.env file in its directory. Copy this file to .env and fill in the required values.

`cp app/.example.env app/.env`