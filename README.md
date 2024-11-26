# Blog API

A FastAPI-based RESTful API for a blogging platform with authentication and authorization.

## Features

- User Authentication (JWT with Access & Refresh Tokens)
- Role-based Authorization (Admin/User)
- User Management
- Blog Posts
- Comments
- Likes
- User Following System
- Protected Routes

## Tech Stack

- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- JWT Authentication
- Python 3.10+

## Project Structure

blog/
├── database/
│   ├── __init__.py
│   ├── connection.py
│   └── models.py
├── routers/
│   ├── __init__.py
│   ├── auth.py
│   ├── users.py
│   ├── posts.py
│   ├── comments.py
│   └── likes.py
├── schemas/
│   ├── __init__.py
│   ├── user.py
│   ├── post.py
│   └── comment.py
├── utils/
│   ├── __init__.py
│   ├── auth.py
│   └── helpers.py
├── config.py
├── main.py
└── requirements.txt

## Installation

1. Clone the repository:

## Project Setup

### 1. Clone the repository:

## API Routes

### Authentication
- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login and get access token
- `POST /auth/refresh` - Refresh access token
- `POST /auth/logout` - Logout user

### Users
- `GET /users` - Get all users (Admin only)
- `GET /users/me` - Get current user profile
- `GET /users/{user_id}` - Get specific user profile
- `PUT /users/me` - Update current user profile
- `DELETE /users/me` - Delete current user account
- `POST /users/{user_id}/follow` - Follow a user
- `DELETE /users/{user_id}/unfollow` - Unfollow a user
- `GET /users/me/followers` - Get user's followers
- `GET /users/me/following` - Get users being followed

### Blog Posts
- `GET /posts` - Get all posts (with pagination)
- `POST /posts` - Create new post
- `GET /posts/{post_id}` - Get specific post
- `PUT /posts/{post_id}` - Update post (author only)
- `DELETE /posts/{post_id}` - Delete post (author only)
- `GET /users/{user_id}/posts` - Get all posts by specific user
- `GET /posts/feed` - Get posts from followed users

### Comments
- `GET /posts/{post_id}/comments` - Get all comments for a post
- `POST /posts/{post_id}/comments` - Add comment to post
- `PUT /posts/{post_id}/comments/{comment_id}` - Update comment (author only)
- `DELETE /posts/{post_id}/comments/{comment_id}` - Delete comment (author only)

### Likes
- `POST /posts/{post_id}/like` - Like a post
- `DELETE /posts/{post_id}/unlike` - Unlike a post
- `GET /posts/{post_id}/likes` - Get users who liked a post
- `GET /users/me/liked-posts` - Get posts liked by current user

### Admin Routes
- `GET /admin/users` - Get all users with detailed info
- `PUT /admin/users/{user_id}` - Update user roles/status
- `DELETE /admin/users/{user_id}` - Delete user account
- `GET /admin/posts` - Get all posts with moderation options
- `DELETE /admin/posts/{post_id}` - Delete any post

Each endpoint includes:
- Authentication requirements
- Request/Response schemas
- Query parameters for filtering/pagination where applicable
- Proper error responses
- Rate limiting on sensitive routes