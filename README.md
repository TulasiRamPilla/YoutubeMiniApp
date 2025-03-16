# YouTube API Mini-App

This application connects to the YouTube API to manage a specific YouTube video. It allows users to view video details, update the video title, add comments, and delete comments.

## Features

1. View video details (title, description, views, likes)
2. Update video title
3. Add comments to the video
4. Delete comments
5. Track all events in a SQLite database
6. View event logs

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Home page, displays video and comments |
| `/comment` | POST | Add a new comment to the video |
| `/update_title` | POST | Update the video title |
| `/delete_comment` | POST | Delete a comment |
| `/logs` | GET | View all logged events |

## Database Schema

The application uses SQLite with a single table:

### Events Table

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| timestamp | TEXT | Time when the event occurred |
| action | TEXT | Type of action (fetch_video, add_comment, update_title, delete_comment, error) |
| details | TEXT | Additional information about the event |

## Setup and Installation

1. Clone this repository
2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
3. Create OAuth 2.0 credentials in the Google Cloud Console:
   - Go to https://console.developers.google.com/
   - Create a new project
   - Enable the YouTube Data API v3
   - Create OAuth 2.0 Client IDs
   - Download the client secrets file and save it in the project directory as specified in app.py

4. Update the `VIDEO_ID` in app.py with your unlisted YouTube video ID

5. Run the application:
   ```
   python app.py
   ```

## Deployment

This application can be deployed to platforms like Heroku, Render, or Vercel. For Heroku, you can use the included Procfile.

### Deployment Steps

1. Create an account on your preferred deployment platform
2. Connect your GitHub repository or upload the files directly
3. Set up environment variables if needed
4. Deploy the application
