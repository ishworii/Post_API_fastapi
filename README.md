Here’s an updated README that includes **like**, **comment**, **user endpoints**, and **notification via WebSocket** features:

---

# FastAPI Blog API

This is a **FastAPI**-based RESTful API for managing posts and users with JWT-based authentication. The API allows users to create, read, update, and delete posts, and provides authentication through token-based login. Users need a valid token to access protected routes.

## TODO
- **Add query params to filter query by author, title, search string, or something else**
- **Add role-based user (normal/admin)**
- **Add functionality so that user can subscribe to a post**
- **Only receive notifications if user is an author, has commented, or has subscribed to a post.**

## DISCLAIMER
### Alembic migrations currently not functional, will fix later.

## Features

- **JWT Authentication**: Secure your API endpoints with token-based authentication.
- **CRUD Operations**: Create, read, update, and delete posts.
- **User Management**: User sign-up, login, and access control for creating/updating/deleting posts.
- **Post Management**: Get all posts, get a single post, create, update, and delete posts.
- **Token Expiry**: Tokens expire after 30 minutes by default, ensuring enhanced security.
- **Like/Dislike**: Authenticated users can like and dislike posts.
- **Commenting**: Authenticated users can comment on posts.
- **WebSocket for Notifications**: Authenticated users receive real-time notifications for new comments (see #TODO for planned enhancements).

## Prerequisites

- **Python 3.10+**
- **FastAPI**
- **SQLAlchemy**
- **Alembic**
- **PostgreSQL** (or any SQL database)
- **JWT (Json Web Token)** for authentication
- **Docker** (optional, for deployment)

## Project Structure

```bash
project-root/
├── alembic/                 # Alembic migrations
├── app/
│   ├── api/                 # API routes (users, posts, comments, auth)
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
### Needs to be fixed!!!

```bash
alembic upgrade head
```

### 6. Run the Application

Start the FastAPI server to run in a development environment:

```bash
fastapi dev app/main.py
```

The API will be available at `http://127.0.0.1:8000`.

## Endpoints

### Authentication

#### **POST** `/users/register`

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
    "id": "ID"
  }
  ```

#### **POST** `/users/login`

Login to get an access token.

- **Request Body (x-www-form-urlencoded)**:
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
    "full_name": "your full name"
  }
  ```

#### **GET** `/users/{id}`

Get user details by ID. Requires an authentication token.

- **Authorization Header**:
  
  ```
  Authorization: Bearer your_token
  ```

- **Response**:
  ```json
  {
    "username": "your_username",
    "email": "your_email",
    "full_name": "your_full_name",
    "id": 1
  }
  ```

#### **GET** `/users/{id}/posts`

Get all posts by a specific user.

- **Authorization Header**:
  
  ```
  Authorization: Bearer your_token
  ```

- **Response**:
  ```json
  [
    {
      "title": "Post Title",
      "content": "Post Content",
      "id": 1,
      "author_id": 1,
      "like_count": 0,
      "dislike_count": 0
    }
  ]
  ```

### Likes/Dislikes

#### **POST** `/posts/{id}/like`

Like a post.

- **Authorization Header**:
  
  ```
  Authorization: Bearer your_token
  ```

- **Response**:
  ```json
  {
    "is_like": true,
    "like_count": 1,
    "dislike_count": 0
  }
  ```

#### **POST** `/posts/{id}/dislike`

Dislike a post.

- **Authorization Header**:
  
  ```
  Authorization: Bearer your_token
  ```

- **Response**:
  ```json
  {
    "is_like": false,
    "like_count": 0,
    "dislike_count": 1
  }
  ```

### Comments

#### **POST** `/posts/{id}/comments`

Add a comment to a post.

- **Authorization Header**:
  
  ```
  Authorization: Bearer your_token
  ```

- **Request Body**:
  ```json
  {
    "content": "This is a comment"
  }
  ```

- **Response**:
  ```json
  {
    "id": 1,
    "content": "This is a comment",
    "post_id": 1,
    "user_id": 1
  }
  ```

#### **GET** `/comments/{id}`

Get a specific comment by ID.

- **Authorization Header**:
  
  ```
  Authorization: Bearer your_token
  ```

- **Response**:
  ```json
  {
    "id": 1,
    "content": "This is a comment",
    "post_id": 1,
    "user_id": 1
  }
  ```

#### **GET** `/posts/{id}/comments`

Get all comments for a specific post.

- **Response**:
  ```json
  [
    {
      "id": 1,
      "content": "This is a comment",
      "post_id": 1,
      "user_id": 1
    }
  ]
  ```

#### **GET** `/users/{id}/comments`

Get all comments by a specific user.

- **Response**:
  ```json
  [
    {
      "id": 1,
      "content": "This is a comment",
      "post_id": 1,
      "user_id": 1
    }
  ]
  ```

### WebSocket Notifications

Authenticated users can subscribe to real-time notifications for new comments on posts they are either the author of, have commented on, or have subscribed to.

#### **WebSocket** `/ws/notifications`

- Connect to `/ws/notifications` via WebSocket.
- The server will push real-time notifications for new comments on relevant posts.
- Notifications will be sent if the user:
  - Is the author of the post.
  - Has commented on the post.
  - Has subscribed to the post.

---

## Security

- **JWT Token Expiry**: Tokens are valid for 30 minutes. After this period, the token expires, and the user needs to log in again to get a new token.
- **Token Validation**: Tokens are checked for expiration and validity on every request to protected routes.

## Contributing

Feel free to submit issues or pull requests for improvements and bug fixes!

---

This updated README includes details about the **like**, **dislike**, **comment**, and **WebSocket notification** features. Let me know if you need any further

 changes!