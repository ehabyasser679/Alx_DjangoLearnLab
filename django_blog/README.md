# Django Blog Project

## Features

### User Authentication
- **Registration**: Users can register for an account using the `/register/` endpoint.
- **Login/Logout**: Users can log in and out to access protected features.
- **Profile**: Authenticated users can view their profile at `/profile/`.

### Blog Posts
- **List Posts**: View all blog posts at `/post/`.
- **Create Post**: Authenticated users can create new posts at `/post/new/`.
- **Edit/Delete Post**: Authors can edit or delete their own posts.
- **View Post**: Click on a post title to view the full content.

### Tagging and Search
- **Tags**: Posts can be tagged. Click on a tag to see all related posts.
- **Search**: Search for posts by title, content, or tags using the search bar in the header.

### Comments
- **View Comments**: Comments are displayed at the bottom of each post detail page.
- **Add Comment**: Authenticated users can add comments to any post.
- **Edit/Delete Comment**: Users can edit or delete their own comments.

## Setup

1.  **Install Dependencies**: Install Django and other requirements.
2.  **Database**: Run migrations:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```
3.  **Run Server**:
    ```bash
    python manage.py runserver
    ```
