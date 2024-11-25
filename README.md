# FastAPI Social Media API

## History

Initially, this project started as a simple blog API written in FastAPI. However, as I progressed, I decided to expand it into a full-fledged social media API, incorporating the features you'd expect from a social media application. While not yet production-ready, the focus is on learning FastAPI and its ecosystem.

I plan to document the development process in blogs and continue adding features to make it more robust.

## Features

- Role-based access control (normal/admin users)
- Subscription-based notifications
- WebSockets for real-time updates
- Content moderation with automated tools
- Redis for caching
- Full-text search and filtering
- Tags for posts
- CI/CD pipeline with GitHub Actions
- Dockerized setup for easy deployment

## TODO

### Here's a list of todos, most completed few in the progress:

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
- [x] **Add ability to follow other people**
- **Add GraphQL**
- **Add background tasks**
- **Add fuzzy match based searching**
- [x] **Add tags to the post**
- **Add logging**
- [x] **Fix the search query bugs**
- [x] **Evaluate poetry for better package management**
- [x] **Update readme to reflect poetry addition**

## Prerequisites

- **Python 3.10+**
- **FastAPI**
- **SQLAlchemy**
- **Alembic**
- **PostgreSQL**
- **Redis**
- **Docker**

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/ishworii/FastAPI_Social_Media_API.git
cd FastAPI_Social_Media_API
```

### 2. Set Up Poetry

Ensure Poetry is installed. You can install it via:

```bash
pip install poetry
```

Install dependencies using Poetry:

```bash
poetry install
```

Activate the virtual environment:

```bash
poetry shell
```

### 3. Set Up Environment Variables

Create a `.env` file in the project root with the following variables. You'll also need `.env.docker` and `.env.ci` for Docker and CI/CD configurations:

```
SECRET_KEY=your_secret_key
ALGORITHM=HS256
SQLALCHEMY_DATABASE_URL=postgresql://<user>:<password>@<localhost>/<dbname>
ACCESS_TOKEN_EXPIRE_MINUTES=30
REDIS_URL=redis://localhost:6379/0
SQLALCHEMY_TEST_DATABASE_URL=postgresql://<user>:<password>@<localhost>/<test_dbname>
```

Replace `<user>`, `<password>`, `<dbname>`, and `<test_dbname>` with your values.

## Running the App with Docker

To simplify setup, use Docker to run the application along with Redis and PostgreSQL.

1. Build the Docker image:

   ```bash
   docker-compose build
   ```

2. Start the containers:

   ```bash
   docker-compose up
   ```

The API will be available at `http://127.0.0.1:8000`. Redis will be running on `localhost:6379`.

## Running the Application Locally

If you prefer to run the app without Docker:

1. Start Redis locally or in Docker:

   ```bash
   docker run -d --name redis -p 6379:6379 redis
   ```

2. Start PostgreSQL locally or in Docker.

3. Run the application:

   ```bash
   poetry run uvicorn app.main:app --reload
   ```

   or

   ```
   fastapi run app/main.py
   ```

Access the API at `http://127.0.0.1:8000`.

## Testing the Application

Run tests using Pytest:

1. Ensure the test database is created.
2. Execute the tests:

   ```bash
   poetry run pytest
   ```

For tests using Redis, ensure Redis is running locally or in Docker.

## WebSocket Routes

WebSocket endpoints enable real-time updates for subscribed users:

1. **Subscribe to notifications:**

   - Endpoint: `ws://127.0.0.1:8000/ws/notifications`
   - Description: Clients can connect to receive real-time updates for posts they are subscribed to.

2. **Broadcast notifications:**
   - Internal endpoint triggered by actions such as new comments or likes.

## Endpoints

Here's a brief overview of the REST API endpoints:

1. **Posts**

   - `GET /posts` - Retrieve all posts
   - `POST /posts` - Create a new post
   - `GET /posts/search?query={query}` - Full-text search for posts
   - `GET /posts/{id}` - Retrieve a post by ID
   - `PUT /posts/{id}` - Update a specific post
   - `DELETE /posts/{id}` - Delete a specific post
   - `POST /posts/{id}/{action}` - Like, dislike, subscribe, or unsubscribe from a post

2. **Comments**

   - `POST /posts/{id}/comment` - Add a comment under a post
   - `GET /comments/{comment_id}` - Retrieve a comment
   - `PUT /comments/{comment_id}` - Update a comment
   - `DELETE /comments/{comment_id}` - Delete a comment

3. **Users**

   - `POST /users/register` - Register a user
   - `POST /users/login` - Login a user
   - `GET /users/me` - Retrieve the current user's details

4. **Follow**

   - `POST /{user_id}/follow` - Follow a user
   - `POST /{user_id}/unfollow` - Unfollow a user
   - `GET /{user_id}/followers` - List of followers
   - `GET /{user_id}/following` - List of following

5. **WebSockets**
   - `ws://127.0.0.1:8000/ws/notifications` - Real-time notifications for post subscriptions

## Future Features

- Email notifications
- Performance optimizations
- Advanced role-based access control
- GraphQL support
- Fuzzy matching in search
- Background tasks for async processing
- Logging
- User analytics

Feel free to suggest any updates or raise issues in the repository!

```

```
