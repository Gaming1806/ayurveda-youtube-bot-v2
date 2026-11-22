#!/usr/bin/env python3
"""
Change the privacy status of an already-uploaded YouTube video.
Use this after you review the private video and want to make it public.
"""
import argparse
import os
import sys
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = [
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
                print("❌ client_secret.json not found in project root.")
                sys.exit(1)
            flow = InstalledAppFlow.from_client_secrets_file(
                "client_secret.json", SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open(token_file, "w", encoding="utf-8") as f:
            f.write(creds.to_json())

    return build("youtube", "v3", credentials=creds)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--video-id", required=True, help="YouTube video ID (e.g. dQw4w9WgXcQ)"
    )
    parser.add_argument(
        "--privacy",
        default="public",
        choices=["public", "private", "unlisted"],
        help="Target privacy status",
    )
    args = parser.parse_args()

    youtube = get_service()

    request = youtube.videos().update(
        part="status",
        body={
            "id": args.video_id,
            "status": {"privacyStatus": args.privacy},
        },
    )
    response = request.execute()

    print(f"✅ Video {args.video_id} is now {args.privacy}")
    print(f"🔗 https://youtu.be/{args.video_id}")


if __name__ == "__main__":
    main()