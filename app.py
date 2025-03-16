from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import os
from datetime import datetime

app = Flask(__name__)

# YouTube API setup
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]
VIDEO_ID = "C6YmndnN8kw"
CLIENT_SECRETS_FILE = "client_secret_606109583103-8vnnt7n67ttaoabvig06fmchcntq92mb.apps.googleusercontent.com.json"

# def get_youtube_service():
#     flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
#     credentials = flow.run_local_server(port=0)
#     return build("youtube", "v3", credentials=credentials)
#
def get_youtube_service():
    # Create flow instance with specific redirect URI
    flow = InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        SCOPES,
        redirect_uri='http://localhost:8080/'
    )

    # Run the local server on port 8080
    # Different port than Flask to avoid conflicts
    credentials = flow.run_local_server(
        port=8080,
        prompt='consent',
        authorization_prompt_message='Please authorize this application to access your YouTube account'
    )

    # Build and return the service
    return build("youtube", "v3", credentials=credentials)

# Database setup
def log_event(action, details):
    conn = sqlite3.connect("events.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS events (id INTEGER PRIMARY KEY, timestamp TEXT, action TEXT, details TEXT)")
    c.execute("INSERT INTO events (timestamp, action, details) VALUES (?, ?, ?)",
              (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), action, details))
    conn.commit()
    conn.close()

# Routes
@app.route("/")
def index():
    youtube = get_youtube_service()
    video_response = youtube.videos().list(part="snippet,statistics", id=VIDEO_ID).execute()
    video = video_response["items"][0]
    log_event("fetch_video", f"Fetched details for video {VIDEO_ID}")
    return render_template("index.html", video=video)

@app.route("/comment", methods=["POST"])
def comment():
    youtube = get_youtube_service()
    comment_text = request.form["comment"]
    youtube.commentThreads().insert(
        part="snippet",
        body={
            "snippet": {
                "videoId": VIDEO_ID,
                "topLevelComment": {"snippet": {"textOriginal": comment_text}}
            }
        }
    ).execute()
    log_event("add_comment", f"Commented: {comment_text}")
    return redirect(url_for("index"))

@app.route("/update_title", methods=["POST"])
def update_title():
    youtube = get_youtube_service()
    new_title = request.form["title"]
    youtube.videos().update(
        part="snippet",
        body={"id": VIDEO_ID, "snippet": {"title": new_title, "categoryId": "22"}}
    ).execute()
    log_event("update_title", f"Updated title to: {new_title}")
    return redirect(url_for("index"))

@app.route("/delete_comment", methods=["POST"])
def delete_comment():
    youtube = get_youtube_service()
    comment_id = request.form["comment_id"]
    youtube.comments().delete(id=comment_id).execute()
    log_event("delete_comment", f"Deleted comment ID: {comment_id}")
    return redirect(url_for("index"))

@app.route("/logs")
def logs():
    conn = sqlite3.connect("events.db")
    c = conn.cursor()
    c.execute("SELECT * FROM events ORDER BY timestamp DESC")
    events = c.fetchall()
    conn.close()
    return render_template("logs.html", events=events)

if __name__ == "__main__":
    app.run(debug=True)

