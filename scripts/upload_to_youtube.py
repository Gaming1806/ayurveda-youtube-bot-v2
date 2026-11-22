#!/usr/bin/env python3
"""
Upload a video to YouTube (as private) and attach a thumbnail.
Uses OAuth 2.0 via token.json (restored from the YT_OAUTH_TOKEN secret in CI).
"""
import os
import sys
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = [
    "https://www.googleapis.com/auth/youtube",          # needed for videos.update / thumbnails
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.readonly",
]


def get_service():
    creds = None
    token_file = "token.json"

    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists("client_secret.json"):
                print("❌ No valid token.json and no client_secret.json. "
                      "Run scripts/oauth_setup.py locally and update the YT_OAUTH_TOKEN secret.")
                sys.exit(1)
            flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
            creds = flow.run_local_server(port=0)

        with open(token_file, "w", encoding="utf-8") as f:
            f.write(creds.to_json())

    return build("youtube", "v3", credentials=creds)


def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()


def main():
    title = read_file("content/title.txt")
    description = read_file("content/description.txt")
    tags_line = read_file("content/tags.txt")
    tags = [t.strip() for t in tags_line.split(",") if t.strip()]

    video_path = "final_video.mp4"
    thumb_path = "thumbnail.jpg"

    if not os.path.exists(video_path):
        print(f"❌ Video not found: {video_path}")
        sys.exit(1)
    if not os.path.exists(thumb_path):
        print(f"❌ Thumbnail not found: {thumb_path}")
        sys.exit(1)

    youtube = get_service()

    body = {
        "snippet": {
            "title": title[:100],
            "description": description,
            "tags": tags,
            "categoryId": "26",  # Howto & Style
            "defaultLanguage": "en",
        },
        "status": {
            "privacyStatus": "private",
            "selfDeclaredMadeForKids": False,
        },
    }

    media = MediaFileUpload(video_path, mimetype="video/mp4", resumable=True)
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)

    try:
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                print(f"⬆️  Uploading... {int(status.progress() * 100)}%")
    except HttpError as e:
        print(f"❌ Upload failed: {e}")
        sys.exit(1)

    video_id = response["id"]
    print(f"✅ Video uploaded: https://youtu.be/{video_id} (private)")

    # Thumbnail (requires a verified YouTube channel; failure here is non-fatal)
    try:
        youtube.thumbnails().set(
            videoId=video_id,
            media_body=MediaFileUpload(thumb_path, mimetype="image/jpeg"),
        ).execute()
        print(f"✅ Thumbnail attached to video {video_id}")
    except HttpError as e:
        print(f"⚠️ Video uploaded, but thumbnail could not be set: {e}")
        print("   (Custom thumbnails require a verified channel: youtube.com/verify)")


if __name__ == "__main__":
    main()
