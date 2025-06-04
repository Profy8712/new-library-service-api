# new-library-service-api

# Library Service API

Library Service API is a Django-based microservice project designed for city libraries to manage books, borrowings, payments, and notifications.

## Features

- Books inventory management (CRUD)
- User registration and JWT authentication
- Book borrowings management
- Filtering by borrowing status
- Notifications via Telegram (Celery + Redis)
- Stripe integration for payments
- PostgreSQL as main database
- Dockerized for development
- Swagger auto-generated documentation
- 60%+ test coverage for custom code

## Quickstart

### Prerequisites

- Python 3.10+
- Docker & Docker Compose

### Setup

```bash
cp .env.sample .env
# (Set your own secrets)
docker-compose up --build
