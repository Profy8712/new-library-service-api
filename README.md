# Library Service API

A web-based library management system for tracking books, borrowings, users, and payments.  
Built with Django, Django REST Framework, PostgreSQL, Celery, Redis, Stripe, and Telegram integration.

---

## 1. Features

1.1. Manage books inventory (CRUD)  
1.2. User registration & JWT authentication  
1.3. Borrowings (create, return, list, filters)  
1.4. Stripe payments and fines  
1.5. Telegram notifications (async via Celery)  
1.6. Admin panel and user permissions  
1.7. API documentation (Swagger/Redoc/OpenAPI)  
1.8. Dockerized for easy deployment

---

## 2. Tech Stack

2.1. Python 3.11  
2.2. Django 5.x, Django REST Framework  
2.3. PostgreSQL  
2.4. Celery & Redis  
2.5. Stripe API  
2.6. Telegram Bot API  
2.7. drf-spectacular (OpenAPI 3.0 schema, Swagger/Redoc)  
2.8. Docker & docker-compose

---

## 3. Quickstart (Docker)

### 3.1. Clone the repository

bash
git clone https://github.com/your-username/library-service-api.git
cd library-service-api
3.2. Create and configure .env file
Copy the sample and fill in all required values:

bash
Copy
Edit
cp .env.sample .env
Edit .env with your real secrets and credentials.

3.3. Build and start all services
bash
Copy
Edit
docker-compose up --build
The API will be available at http://localhost:8000/

Swagger UI: http://localhost:8000/swagger/

Redoc: http://localhost:8000/redoc/

Admin panel: http://localhost:8000/admin/

3.4. Apply migrations
bash
Copy
Edit
docker-compose exec web python manage.py migrate
3.5. Create a superuser (optional)
bash
Copy
Edit
docker-compose exec web python manage.py createsuperuser
4. Environment Variables
See .env.sample for all required variables.
You must set your own:

4.1. Django secret key
4.2. Database credentials (POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD, etc.)
4.3. Stripe API keys (test keys are fine for local dev)
4.4. Telegram Bot token & chat ID

5. API Documentation
5.1. OpenAPI JSON schema: /api/schema/
5.2. Swagger UI: /swagger/
5.3. Redoc: /redoc/

Interactive docs let you register, login, create borrowings, pay, and more directly from the browser.

6. Endpoints Overview
#	Resource	Endpoint	Description
6.1	Books	/api/books/	CRUD, read for all, write for admin
6.2	Users	/api/users/, /api/users/me/	Registration, user profile
6.3	Auth	/api/users/token/, /api/users/token/refresh/	JWT obtain/refresh
6.4	Borrowings	/api/borrowings/, /api/borrowings/{id}/return/	List, create, return
6.5	Payments	/api/payments/, /api/payments/create/	List, detail, create payment
6.6	Stripe Webhook	/api/stripe/webhook/	Stripe webhook endpoint

Check Swagger or Redoc for details on request/response structure and filters.

7. Running Tests
7.1. Locally
bash
Copy
Edit
pytest --cov
7.2. In Docker
bash
Copy
Edit
docker-compose exec web pytest --cov
All custom functionality is covered by tests (min. 60% coverage).
Test coverage report is available in terminal or in htmlcov/ after run.

8. Notifications
8.1. Telegram: All new borrowings trigger an async Telegram notification to the library channel or admin chat.
8.2. Stripe: Payment creation returns a Stripe payment session URL. The webhook updates payment status after Stripe payment.

9. User Roles & Permissions
Unauthenticated users: can view book list only

Authenticated users: can create borrowings, see/pay their payments, return books

Admin users: full CRUD for all entities

10. Docker Compose Services
web: Django application with Gunicorn

db: PostgreSQL database

redis: Redis (for Celery broker/result)

celery: Celery worker (async tasks)

celery-beat: Celery scheduler (for periodic tasks)

11. Development Notes
Use Trello for task tracking. Example columns: To Do, In Progress, On Review, Done.

Use feature branches for each task, merge via PR with code review.

All sensitive config/secrets must be set via .env and never committed!

To add new libraries: update requirements.txt and rebuild Docker.

12. Security


Never commit .env or secrets.

For production: set DJANGO_DEBUG=False, configure proper ALLOWED_HOSTS.

Rotate keys before deploying to real users.