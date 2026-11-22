#!/usr/bin/env python3
"""
One-time OAuth flow to create token.json for YouTube uploads.
Run locally once, then add token.json content as GitHub Secret YT_OAUTH_TOKEN.
"""
import os
import sys
import webbrowser
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.readonly",
]


def main():
    if not os.path.exists("client_secret.json"):
        print("❌ client_secret.json not found in project root.")
        sys.exit(1)

    # Read client_id from the file
    import json
    with open("client_secret.json", "r") as f:
        data = json.load(f)

    # Check if it's a web or installed type
    if "web" in data:
        client_type = "web"
    elif "installed" in data:
        client_type = "installed"
    else:
        print("❌ Invalid client_secret.json. Re-download from Google Cloud Console.")
        sys.exit(1)

    print(f"✅ Detected {client_type} OAuth client")

    flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)

    # Try run_local_server with a fixed port
    print("\n🔐 Opening browser for authentication...")
    print("If the browser doesn't open automatically, visit the URL printed below.\n")

    try:
        creds = flow.run_local_server(
            port=8080,
            open_browser=True,
            authorization_prompt_message="Please visit this URL to authorize: {url}",
            success_message="Authentication successful! You can close this tab.",
        )
    except Exception as e:
        print(f"❌ run_local_server failed: {e}")
        print("\nTrying alternate method...\n")
        # Fallback: manual URL + code entry
        auth_url, _ = flow.authorization_url(
            access_type="offline",
            include_granted_scopes="true",
        )
        print(f"Open this URL in your browser:\n{auth_url}\n")
        auth_code = input("Enter the authorization code: ").strip()
        try:
            flow.fetch_token(code=auth_code)
            creds = flow.credentials
        except Exception as e2:
            print(f"❌ Failed to fetch token: {e2}")
            sys.exit(1)

    with open("token.json", "w", encoding="utf-8") as f:
        f.write(creds.to_json())

    print("\n✅ OAuth token saved to token.json")


if __name__ == "__main__":
    main()