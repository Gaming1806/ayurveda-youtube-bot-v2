#!/usr/bin/env python3
"""
One-time OAuth flow to create token.json for YouTube uploads.
Run locally once, then add the base64 of token.json as GitHub Secret YT_OAUTH_TOKEN.
"""
import json
import os
import sys
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = [
    "https://www.googleapis.com/auth/youtube",
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.readonly",
]


def main():
    if not os.path.exists("client_secret.json"):
        print("❌ client_secret.json not found in project root.")
        sys.exit(1)

    with open("client_secret.json", "r") as f:
        data = json.load(f)

    if "installed" in data:
        print("✅ Detected desktop (installed) OAuth client")
    elif "web" in data:
        print("⚠️ Detected a 'web' OAuth client. Recommended: create a 'Desktop app' client instead.")
        print("   (A web client must have http://localhost:8080/ as an authorised redirect URI.)")
    else:
        print("❌ Invalid client_secret.json. Re-download from Google Cloud Console.")
        sys.exit(1)

    flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)

    print("\n🔐 Starting authentication...")
    try:
        creds = flow.run_local_server(
            port=8080,
            open_browser=True,
            prompt="consent",          # ensures a refresh token is returned
            authorization_prompt_message="If the browser doesn't open, visit: {url}",
            success_message="Authentication successful! You can close this tab.",
        )
    except Exception as e:
        print(f"❌ Authentication failed: {e}")
        sys.exit(1)

    if not creds.refresh_token:
        print("❌ No refresh token returned. Remove the app at "
              "https://myaccount.google.com/permissions and run this script again.")
        sys.exit(1)

    with open("token.json", "w", encoding="utf-8") as f:
        f.write(creds.to_json())

    print("\n✅ OAuth token saved to token.json")
    print("Next: base64-encode it and save it as the GitHub secret YT_OAUTH_TOKEN.")


if __name__ == "__main__":
    main()
