# 🌿 Ayurvedic YouTube Bot – Fully Automated & Free

A complete, ready-to-run pipeline that creates, assembles, and uploads Ayurvedic videos to YouTube **without any paid API keys**.  
The only external account you need is a free Google Cloud project for OAuth (YouTube uploads).

## ✨ What this project does

| Step | Tool | Cost |
|------|------|------|
| 1. Pick an Ayurvedic topic & write script/title/tags | Built-in Python templates | Free |
| 2. Convert script to voice-over | `pyttsx3` (offline TTS) | Free |
| 3. Get video footage | Local `footage/` folder OR ffmpeg-generated clip | Free |
| 4. Create a 1280×720 thumbnail | `Pillow` (image + text) | Free |
| 5. Merge footage + voice into final MP4 | `ffmpeg` | Free |
| 6. Upload to YouTube as **private** | YouTube Data API v3 + OAuth | Free |
| 7. You review the private video | YouTube Studio (manual) | Free |
| 8. You click **Publish** from GitHub | `publish-video.yml` workflow | Free |

---

## 📂 Repository Structure

```
ayurveda-youtube-bot/
├─ .github/
│  ├─ workflows/
│  │  ├─ daily-publish.yml      # Creates a private video daily (or on demand)
│  │  └─ publish-video.yml      # YOU click this to make the video public/unlisted
├─ scripts/
│  ├─ generate_content.py       # Picks topic, writes script/title/tags
│  ├─ text_to_speech.py         # Offline voice-over (pyttsx3)
│  ├─ fetch_footage.py          # Local footage or ffmpeg placeholder
│  ├─ generate_thumbnail.py     # Pillow thumbnail generator
│  ├─ assemble_video.py         # ffmpeg video merger
│  ├─ upload_to_youtube.py      # Uploads video as private + sets thumbnail
│  ├─ set_privacy.py            # Changes private → public/unlisted after your review
│  └─ oauth_setup.py            # One-time OAuth to create token.json
├─ footage/                     # (Optional) Drop your own royalty-free MP4 clips here
├─ content/                     # Created automatically at runtime
├─ .gitignore
├─ requirements.txt
├─ .env.example
├─ client_secret.json           # Your Google OAuth file (replace placeholder)
└─ README.md                    # This file
```

---

## 🚀 Step-by-Step Setup

### 1️⃣ Create the GitHub repository

1. Go to <https://github.com/new>
2. Repository name: `ayurveda-youtube-bot` (or any name you like)
3. Set it to **Public** or **Private**
4. **Do not** initialize with README, .gitignore, or license (we will add those)
5. Click **Create repository**

### 2️⃣ Add all project files

Copy every file from the repository structure above into your repo (via GitHub web UI upload or `git push`).

### 3️⃣ Install prerequisites on your computer (for the one-time OAuth step)

You need **Python 3.10+** and **ffmpeg**.

**Windows:**
```powershell
# Install Python from https://python.org (check "Add to PATH")
# Install ffmpeg from https://ffmpeg.org/download.html and add ffmpeg to PATH
```

**macOS:**
```bash
brew install python ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update && sudo apt install -y python3 python3-pip ffmpeg
```

### 4️⃣ Set up free Google OAuth for YouTube uploads

This is the **only external account step**, and it is completely free.

1. Go to <https://console.cloud.google.com/>
2. Create a new project (e.g., `ayurveda-youtube-bot`)
3. **Enable APIs:**  
   *APIs & Services → Library → search "YouTube Data API v3" → Enable*
4. **Create OAuth credentials:**  
   *APIs & Services → Credentials → Create credentials → OAuth client ID*  
   *Application type:* **Desktop app**  
   *Name:* `AyurTubeBot`  
   Click **Create**, then download the JSON file.
5. Rename the downloaded file to `client_secret.json` and place it in the **root of this project** (next to `README.md`).

### 5️⃣ Run the one-time OAuth flow locally

Open a terminal in the project folder and run:

```bash
# Create a virtual environment (recommended)
python -m venv .venv

# Activate it
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run OAuth (a browser window will open; sign in and grant permission)
python scripts/oauth_setup.py
```

After you approve, a file named **`token.json`** will appear in the project folder.  
**Do not commit `token.json`** (it is already in `.gitignore`).

### 6️⃣ Store the OAuth token as a GitHub Secret

GitHub Actions cannot open a browser, so we store the token as a secret.

1. Encode `token.json` to base64:
   *macOS / Linux:* `base64 -i token.json`  
   *Windows (PowerShell):* `[Convert]::ToBase64String([System.IO.File]::ReadAllBytes("token.json"))`
2. Copy the entire output string.
3. In your GitHub repo, go to **Settings → Secrets and variables → Actions → New repository secret**
   *Name:* `YT_OAUTH_TOKEN`  
   *Value:* (paste the base64 string)

> If you do not add this secret, the upload and publish steps will be skipped.

### 7️⃣ Commit, push, and run the workflow

```bash
git add -A
git commit -m "Initial commit: Ayurvedic YouTube automation"
git push origin main   # or master, depending on your default branch
```

Go to your repo → **Actions** tab → **Ayurvedic Video Bot** → **Run workflow**.  
The pipeline will create a **private** video on your YouTube channel. You can check YouTube Studio → Content to see it.

### 8️⃣ Schedule automatic runs (optional)

Edit `.github/workflows/daily-publish.yml` and change the cron line:

```yaml
# Every day at 09:00 UTC
cron: '0 9 * * *'

# Every Monday at 09:00 UTC
cron: '0 9 * * 1'

# Every 2 days
cron: '0 9 */2 * *'
```

Commit the change and GitHub will run it automatically.

---

## 🔄 Review → Publish Workflow

This project uses a **human review gate** before any video goes live.

### Step A: Bot creates a private video
- Run **Actions → Ayurvedic Video Bot → Run workflow**.
- The bot uploads the video as **private**.
- In the action logs, you will see a link like:
  ```
  ✅ Video uploaded: https://youtu.be/abc123XYZ (private)
  ```
- Copy the video ID (`abc123XYZ`).

### Step B: You review the video
1. Open **YouTube Studio** → **Content**.
2. Find the video with visibility **Private**.
3. Click it, watch it, check title / thumbnail / description.
4. If you are happy, note the Video ID again from the URL: `youtube.com/watch?v=abc123XYZ`.

### Step C: Publish from GitHub
1. Go to your GitHub repo → **Actions** tab.
2. On the left, click **Publish YouTube Video**.
3. Click the **Run workflow** dropdown button on the right.
4. Paste the **Video ID** (just the ID, not the full URL).
5. Choose **public** (default) or **unlisted** if you prefer.
6. Click **Run workflow**.

### Step D: Done
The action calls the YouTube API and flips the video to **public**.  
You will see in the action log:
```
✅ Video abc123XYZ is now public
🔗 https://youtu.be/abc123XYZ
```

---

## 🛠️ Customising the Content

Edit `scripts/generate_content.py` to add your own Ayurvedic topics, scripts, titles, and tags. The script randomly picks one each run.

You can also place your own royalty-free MP4 clips inside the `footage/` folder; the bot will pick one at random. If the folder is empty, it generates a simple orange background clip with ffmpeg.

---

## ⚠️ Important Notes

* **Videos are uploaded as `private`** by default. Change `--privacy public` in the workflow or in `upload_to_youtube.py` when you are ready to publish.
* **YouTube Partner Program** requires 1,000 subscribers and 4,000 watch hours (or 10M Shorts views). Automation helps you publish consistently, but real audience growth still depends on content quality and compliance with YouTube’s Community Guidelines.
* Add a medical disclaimer in descriptions (the template already includes "Not medical advice").
* Do **not** commit `token.json`, `.env`, or `client_secret.json` with real secrets. Use GitHub Secrets instead.

---

## 🛠️ Troubleshooting

| Problem | Fix |
|---------|-----|
| `ffmpeg` not found | Install ffmpeg and add it to your system PATH |
| `token.json` missing | Run `python scripts/oauth_setup.py` locally once |
| Upload fails with 403 | Make sure YouTube Data API v3 is enabled in Google Cloud Console |
| GitHub Action skips upload | Add `YT_OAUTH_TOKEN` secret (base64 of `token.json`) |
| Thumbnail text overflows | Shorten the title in `generate_content.py` |

---

## 📄 License

MIT License – use freely for personal or commercial projects.

---

### 🎉 You're ready!

1. Download / copy the project files into your GitHub repo.  
2. Complete the **Google OAuth** setup once.  
3. Add `YT_OAUTH_TOKEN` as a GitHub secret.  
4. Run the **Ayurvedic Video Bot** action to create a private video.  
5. Review it in YouTube Studio.  
6. Run the **Publish YouTube Video** action to make it public.

Let me know if you want to add Twitter/Discord auto-posting, more languages, or a different upload schedule!