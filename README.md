# RealtorCRM

##  Features

-  **JWT Authentication**: Secure login and access control.
-  **CRUD Operations**:
    -  Listings
    -  Users
    -  Clients
-  **Filtering & Sorting**: Query listings by fields and sort them dynamically.
-  **Gmail SMTP Integration**: Send listing details via email.
-  **Dockerized**: Easy to set up and deploy with Docker.

---

##  Tech Stack

- **Backend Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **Database**: PostgreSQL
- **Authentication**: JWT
- **Email**: Gmail SMTP
- **Containerization**: Docker

---

##  Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/jusz22/RealtorCRM.git
cd RealtorCRM
```
### 2. Add environment variables


Create a .env file in the root directory with the following content:
```bash
POSTGRES_DB=RealtorCRM
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=db
DB_CONN_STR=postgresql+asyncpg://postgres:postgres@db:5432/RealtorCRM
ALGORITHM=HS256
SECRET_KEY=jwt_secret_key
ACCESS_TOKEN_EXPIRE_MINUTES=60
API_STR =/api/v1
GMAIL_GENERATED_PASSWORD=your-gmail-address@gmail.com
GMAIL_ADDRESS=your-app-password
```

Note: If using Gmail, you'll need to [generate an App Password](https://support.google.com/accounts/answer/185833?hl=en) if 2FA is enabled.

### 3. Build and run using Docker
```bash
docker-compose up --build
```

## Docs

- **Swagger UI**: http://localhost:8000/docs
