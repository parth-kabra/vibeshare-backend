- # VibeShare Backend Documentation
## Introduction

Welcome to the documentation for the VibeShare social media app backend. This Flask-based backend is responsible for handling user data, posts, comments, likes, and more. Below, you'll find information on how to interact with the API, including available endpoints and their functionalities.
## Getting Started

To use the VibeShare backend, follow the steps below: 
1. Clone the repository: `git clone <repository-url>` 
2. Install dependencies: `pip install -r requirements.txt` 
3. Set up Cloudinary account: [Cloudinary](https://cloudinary.com/)  and obtain API credentials (cloud_name, api_key, api_secret).
4. Configure the Flask app by adding your Cloudinary credentials and SQLAlchemy database URI to the code.

```python
cloudinary.config( 
  cloud_name = "your_cloud_name", 
  api_key = "your_api_key", 
  api_secret = "your_api_secret"
)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "your_database_uri"
```


## Endpoints
### 1. `POST /api/get-user` 
- **Description:**  Retrieve user information by username. 
- **Request:** 

```json
{
  "username": "user123"
}
``` 
- **Response:** 

```json
{
  "user": {
    "state": true,
    "name": "John Doe",
    "username": "user123",
    "pfp": "https://cloudinary.com/image.jpg"
  }
}
```
### 2. `GET /api/get-posts` 
- **Description:**  Retrieve all posts. 
- **Response:** 

```json
{
  "posts": [
    {
      "name": "John Doe",
      "username": "user123",
      "text": "Hello, VibeShare!",
      "pfp": "https://cloudinary.com/image.jpg",
      "img": "https://cloudinary.com/post_image.jpg",
      "likes": 5,
      "post_id": 1
    },
    // ... other posts
  ],
  "status": true
}
```
### 3. `POST /api/like-post` 
- **Description:**  Like or unlike a post. 
- **Request:** 

```json
{
  "post_id": 1,
  "user_email": "user@example.com"
}
``` 
- **Response:** 

```json
{
  "status": true,
  "message": "Post liked successfully"
}
```
### 4. `POST /api/check-liked` 
- **Description:**  Check if a user has liked a post. 
- **Request:** 

```json
{
  "post_id": 1,
  "user_email": "user@example.com"
}
``` 
- **Response:** 

```json
{
  "liked": true
}
```
### 5. `POST /api/create-post` 
- **Description:**  Create a new post. 
- **Request:** 

```json
{
  "user": "John Doe",
  "username": "user123",
  "text": "New post on VibeShare!",
  "img": "base64_encoded_image",
  "pfp": "https://cloudinary.com/image.jpg"
}
``` 
- **Response:** 

```json
{
  "status": true
}
```
### 6. `POST /api/create-user` 
- **Description:**  Create a new user. 
- **Request:** 

```json
{
  "name": "John Doe",
  "username": "user123",
  "email": "user@example.com",
  "pfp": "https://cloudinary.com/image.jpg"
}
``` 
- **Response:** 

```json
{
  "status": true
}
```
### 7. `POST /api/create-comment` 
- **Description:**  Add a comment to a post. 
- **Request:** 

```json
{
  "text": "Great post!",
  "post_id": 1,
  "user_email": "user@example.com",
  "name": "John Doe"
}
``` 
- **Response:** 

```json
{
  "status": true,
  "message": "Comment added successfully!"
}
```
### 8. `POST /api/get-comments` 
- **Description:**  Get comments for a specific post. 
- **Request:** 

```json
{
  "post_id": 1
}
``` 
- **Response:** 

```json
{
  "status": true,
  "message": "Post comments found",
  "comments": [
    {
      "name": "John Doe",
      "email": "user@example.com",
      "text": "Great post!"
    },
    // ... other comments
  ]
}
```
### 9. `GET /api/get-featured` 
- **Description:**  Get featured users. 
- **Response:** 

```json
{
  "status": true,
  "message": "Fetched users.",
  "accounts": [
    {
      "name": "John Doe",
      "username": "user123",
      "img": "https://cloudinary.com/image.jpg"
    },
    // ... other featured users
  ]
}
```
### 10. `POST /api/get-post` 
- **Description:**  Get details of a specific post. 
- **Request:** 

```json
{
  "post_id": 1
}
``` 
- **Response:** 

```json
{
  "name": "John Doe",
  "username": "user123",
  "pfp": "https://cloudinary.com/image.jpg",
  "img": "https://cloudinary.com/post_image.jpg",
  "text": "Hello, VibeShare!",
  "status": true,
  "post_id": 1,
  "likes": 5
}
```
## Additional Notes 
- The base URL for the API is the root of your Flask application (e.g., `http://localhost:5000/`).
- All image URLs are assumed to be Cloudinary URLs.
- The API provides basic error handling, but additional error handling may be needed for production use. 

Feel free to reach out for further assistance or clarification. Happy coding!
