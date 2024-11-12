# FastAPI Social Media API

# History

Initially this was supposed to be a simple blog api written with FastAPI but as I progressed through the project, I
decided to make it full blown social media API with all the standard features that a social media app will have. I know,
there are few more features to add before this becomes "Social Media API" but I am calling it now. I am more concerned about
learning features and understanding FastAPI rather than making it production ready social media api. I might make few blogs
along the way about the whole experience.

### Here's a list of todos, most completed few in the progress:

### TODO

- [x] **Add query params to filter query by author, title, search string, or something else**
- [x] **Add role-based user (normal/admin)**
  - [x] **Admin can delete any post,comment**
  - [x] **Normal users can only delete or update their post,comment,and user details**
- [x] **Add functionality so that user can subscribe to a post**
- [x] **Only receive notifications if user is an author, has commented, or has subscribed to a post.**
- [x] **Add tests for subscription**
- [x] **Add tests for websockets**
- [x] **Debug failing test cases**
- [x] **Implement CI/CD**
- [x] **Add docker file**
- [x] **Added Redis as Cache**
- **Add terraform file**
- [x] **Full-text search and filtering**
- [x] **Content Moderation System**
- **Email Notification**
- **Performance Optimization**
- **Advanced RBAC**
- **User Analytics**
- [x] **Setup test-db in docker and change tests to use Postgresql**
- **Better understand alembic and its workings**
- [x] **Fix the bugs preventing the post to be persistent**
- [x] **Fix the jwt token validation bug**
- **Add advanced rate limiting specific to user roles**
- **Fix the mockup redis in testing**
- **Add ability to follow other people**
- **Add GraphQL**
- **Add background tasks**
- **Add fuzzy match based searching**
- **Add tags to the post**
- **Add logging**
- [x] **Evaluate poetry for better package management**
- **Update readme to reflect poetry addition**

## Prerequisites

- **Python 3.10+**
- **FastAPI**
- **SQLAlchemy**
- **Alembic**
- **PostgreSQL** (or any SQL database)
- **Docker**
- **Redis**

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/ishworii/FastAPI_Social_Media_API.git
cd FastAPI_Social_Media_API
```

### 2. Set Up a Virtual Environment

```bash
python -m venv env
source env/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the project root with the following contents:
Also create `.env.docker` for docker and `.env.ci` for GitHub Actions, the contents will be similar for these files
Just slight altercations.

```
SECRET_KEY=your_secret_key
ALGORITHM=HS256
SQLALCHEMY_DATABASE_URL=postgresql://<user>:<password>@<localhost>/<dbname>
ACCESS_TOKEN_EXPIRE_MINUTES=30
REDIS_URL=redis://<localhost>:<port_number>/0
SQLALCHEMY_TEST_DATABASE_URL=postgresql://<user>:<password>@<localhost>/<test_dbname>
```

Replace the variables with actual values

### 5. Run redis in a docker or locally

### 6. Run the Application

Start the FastAPI server to run in a development environment:

```bash
fastapi dev app/main.py
```

The API will be available at `http://127.0.0.1:8000`.
Check the documentation at `http://127.0.0.1:8000/docs` or `http://127.0.0.1:8000/redoc` , I prefer the later.

### 7. To test the app

Create the test db beforehand.

```bash
pytest
```

# Endpoints

Here's the brief overview of endpoints:

1. GET /posts : get all the post
2. POST /posts : Create a new post
3. GET /posts/search?query={query} : Full text based search
4. GET /posts/{id} : Get post with {id}
5. PUT /posts/{id} : Update a specific post
6. DELETE /posts/{id} : Delete a specific post
7. POST /posts/{id}/{action} : Action can be like or dislike a post and suscribe or unsuscribe from a post
8. POST /posts/{id}/comment : Add a new comment under a post
9. GET /comments/{comment_id} : Get a comment
10. PUT /comments/{comment_id} : Update a comment
11. DELETE /comments/{comment_id} : Delete a comment
12. POST /users/register : Register a user
13. POST /users/login : Login
14. GET /users/me : Get current user

#### I completely forgot about the websockets and authentication, i will add it later.
