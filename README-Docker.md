# 🐳 AIVidGen/ShortGPT Docker Setup Guide

This guide helps you run the complete AIVidGen project using Docker - no Python installation needed!

---

## 📋 Prerequisites

### For Mac Students:
1. Install Docker Desktop: https://docs.docker.com/desktop/install/mac-install/
2. Open Docker Desktop and wait for it to start (whale icon in menu bar)

### For Windows Students:
1. Install Docker Desktop: https://docs.docker.com/desktop/install/windows-install/
2. Enable WSL 2 when prompted during installation
3. Open Docker Desktop and wait for it to start (whale icon in system tray)

---

## 🚀 Quick Start (Easiest Method)

### Step 1: Get the Project Files
Download or clone the project to your computer.

### Step 2: Create API Keys File
Create a file called `.env` in the project folder with your API keys:

```bash
GEMINI_API_KEY=AIzaSyD_CJ6BVFo_d-KTimLQjUtaZtkEEiox_DA
OPENAI_API_KEY=sk-_put_your_openai_api_key_here
PEXELS_API_KEY=aeDdhQ1mjVsddaJxkrVIaGzOMA0zLW4TOLe7WjAuhfudBCQbOwardYcY
```

> **Note:** The `.env` file already exists in the project folder with these keys!

### Step 3: Open Terminal/Command Prompt
- **Mac**: Open Terminal, then `cd` to the project folder
- **Windows**: Open Command Prompt or PowerShell, then `cd` to the project folder

### Step 4: Run with Docker Compose (Recommended)
```bash
docker-compose up --build
```

⏳ **First build takes ~30 minutes** (downloads Python packages, PyTorch, etc.)

### Step 5: Open the App
Wait for the build to finish, then look for a message like:
```
Running on public URL: https://xxxxx.gradio.live
```
Open that URL in your browser, OR go to: **http://localhost:31415**

---

## 🔧 Alternative: Manual Docker Commands

If docker-compose doesn't work, use these commands:

```bash
# Build the image
docker build -t shortgpt:latest .

# Run the container
docker run -p 31415:31415 --env-file .env -v ./videos:/app/videos shortgpt:latest
```

---

## 📦 Pre-built Image (For Teachers)

### Export Image (on your computer):
```bash
docker build -t shortgpt:latest .
docker save shortgpt:latest > shortgpt-image.tar
```

### Share with Students:
Send them the `shortgpt-image.tar` file (will be ~5-8GB)

### Student Loads Image:
```bash
docker load < shortgpt-image.tar
docker run -p 31415:31415 --env-file .env -v ./videos:/app/videos shortgpt:latest
```

---

## 🛠️ Troubleshooting

### "Docker daemon not running"
- Make sure Docker Desktop is open and running

### "Port 31415 already in use"
- Change the port: `docker run -p 8080:31415 ...` then visit http://localhost:8080

### "Permission denied" (Mac/Linux)
- Run with sudo: `sudo docker-compose up`

### Videos not saving
- Make sure the `videos` folder exists in your project directory

---

## 📁 Project Structure
```
ShortGPT/
├── .env              ← Your API keys (create this!)
├── docker-compose.yml
├── Dockerfile
├── videos/           ← Generated videos appear here
└── ...
```

---

## 🎓 For Teaching

The Docker container includes:
- Python 3.11
- FFmpeg (video processing)
- All required packages (moviepy, edge-tts, gradio, etc.)
- Google Gemini & OpenAI integration

Students don't need to install Python or any packages - just Docker!
