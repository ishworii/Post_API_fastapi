# FastAPI Blog API

This is a **FastAPI**-based RESTful API for managing posts and users with JWT-based authentication. The API allows users to create, read, update, and delete posts, and provides authentication through token-based login. Users need a valid token to access protected routes.

## Features

- **JWT Authentication**: Secure your API endpoints with token-based authentication.
- **CRUD Operations**: Create, read, update, and delete posts.
- **User Management**: User sign-up, login, and access control for creating/updating/deleting posts.
- **Post Management**: Get all posts, get a single post, create, update, and delete posts.
- **Token Expiry**: Tokens expire after 30 minutes by default, ensuring enhanced security.

## Prerequisites

- **Python 3.10+**
- **FastAPI**
- **SQLAlchemy**
- **Alembic**
- **PostgreSQL** or any SQL database
- **JWT (Json Web Token)** for authentication
- **Docker** (optional, for deployment)

## Project Structure

```bash
project-root/
├── alembic/                 # Alembic migrations
├── app/
│   ├── api/                 # API routes (users, posts, auth)
│   ├── core/                # Config, security, and middleware
│   ├── crud/                # CRUD operations
│   ├── db/                  # Database initialization
│   ├── models/              # SQLAlchemy models
│   ├── schemas/             # Pydantic models (request/response)
│   └── main.py              # Main entry point for the application
├── alembic.ini              # Alembic configuration file
└── README.md                # Project documentation
```

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/ishworii/Post_API_fastapi.git
cd Post_API_fastapi
```

### 2. Set Up a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the project root with the following contents:

```
SECRET_KEY=your_secret_key
ALGORITHM=HS256
SQLALCHEMY_DATABASE_URL=postgresql://user:password@localhost/dbname
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Replace `your_secret_key` and `SQLALCHEMY_DATABASE_URL` with your actual values.

### 5. Initialize the Database

Run Alembic migrations to set up the database schema.

```bash
alembic upgrade head
```

### 6. Run the Application

Start the FastAPI server to run in a development environment

```bash
fastapi dev app/main.py
```

The API will be available at `http://127.0.0.1:8000`.

## Endpoints

### Authentication

#### **POST** `/user/register`

Create a new user.

- **Request Body**:
  ```json
  {
    "username": "USERNAME",
    "email": "EMAIL",
    "fullname": "FULL NAME",
    "password": "PASSWORD"
  }
  ```
- **Response**:
  ```json
  {
    "username": "USERNAME",
    "email": "EMAIL",
    "full_name": "FULL NAME",
    "id": "ID",
    "posts": []
  }
  ```

#### **POST** `/user/login`

Login to get an access token.

- **Request Body (form-data)**:
  ```json
  {
    "username": "your_username",
    "password": "your_password"
  }
  ```
- **Response**:
  ```json
  {
    "access_token": "your_token",
    "token_type": "bearer",
    "expires_in": "30 minutes"
  }
  ```

#### **GET** `/users/me`

Get details of the current logged-in user. Requires an authentication token.

- **Authorization Header**:

  ```
  Authorization: Bearer your_token
  ```

- **Response**:
  ```json
  {
    "username": "your_username",
    "id": 1,
    "email": "your email",
    "full_name": "your full name",
    "posts": []
  }
  ```

### Posts

#### **GET** `/posts`

Get all posts.

- **Response**:
  ```json
  [
      {
          "id": 1,
          "title": "First Post",
          "content": "This is the content of the first post",
      },
      ...
  ]
  ```

#### **POST** `/posts`

Create a new post. Requires an authentication token.

- **Authorization Header**:

  ```
  Authorization: Bearer your_token
  ```

- **Request Body**:

  ```json
  {
    "title": "New Post",
    "content": "This is the content of the new post"
  }
  ```

- **Response**:
  ```json
  {
    "id": 1,
    "title": "New Post",
    "content": "This is the content of the new post"
  }
  ```

#### **GET** `/posts/{id}`

Get a single post by ID.

- **Response**:
  ```json
  {
    "id": 1,
    "title": "First Post",
    "content": "This is the content of the first post"
  }
  ```

#### **PUT** `/posts/{id}`

Update a post by ID. Requires an authentication token.

- **Authorization Header**:

  ```
  Authorization: Bearer your_token
  ```

- **Request Body**:

  ```json
  {
    "title": "Updated Post",
    "content": "This is the updated content"
  }
  ```

- **Response**:
  ```json
  {
    "id": 1,
    "title": "Updated Post",
    "content": "This is the updated content"
  }
  ```

#### **DELETE** `/posts/{id}`

Delete a post by ID. Requires an authentication token.

- **Authorization Header**:

  ```
  Authorization: Bearer your_token
  ```

## Security

- **JWT Token Expiry**: Tokens are valid for 30 minutes. After this period, the token expires, and the user needs to log in again to get a new token.
- **Token Validation**: Tokens are checked for expiration and validity on every request to protected routes.

## Contributing

Feel free to submit issues or pull requests for improvements and bug fixes!
