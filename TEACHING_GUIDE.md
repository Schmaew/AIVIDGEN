# 🎓 ShortGPT Teaching Guide

## For Instructors: How to Teach This Project

---

## 📋 Overview

This guide helps you teach AI video generation concepts using ShortGPT. Start with the simplified `learn_shortgpt.py` file before diving into the full project.

---

## 🎯 Learning Path (Recommended Order)

### Level 1: Basic Concepts (1-2 hours)
**File:** `learn_shortgpt.py`

| Concept | Function | What Students Learn |
|---------|----------|---------------------|
| AI APIs | `generate_script()` | How to call Gemini API, prompt engineering |
| TTS | `generate_voice()` | Text-to-speech, async programming |
| Video | `create_video()` | MoviePy basics, video codecs |
| Pipeline | `create_short_video()` | Orchestrating multiple steps |

**Exercise:** Run the file and change the topic

```bash
python learn_shortgpt.py
```

---

### Level 2: Understanding the Full Architecture (2-3 hours)

```
ShortGPT/
├── runShortGPT.py          # Entry point - starts the web UI
├── gui/                     # Web interface (Gradio)
│   ├── gui_gradio.py       # Main UI setup
│   └── ui_tab_*.py         # Different UI tabs
├── shortGPT/
│   ├── engine/             # Video generation logic
│   │   ├── abstract_content_engine.py  # Base class
│   │   ├── content_short_engine.py     # Short video engine
│   │   └── facts_short_engine.py       # Facts-specific logic
│   ├── gpt/                # AI/LLM integration
│   │   ├── gpt_utils.py    # API calls
│   │   └── facts_gpt.py    # Facts generation
│   ├── audio/              # Text-to-speech
│   │   └── edge_voice_module.py
│   ├── editing_framework/  # Video editing
│   │   └── core_editing_engine.py
│   └── config/             # Settings & API keys
└── videos/                 # Output folder
```

---

### Level 3: Key Files to Study

#### 1. Entry Point
```python
# runShortGPT.py - Just 3 lines of important code!
from gui.gui_gradio import ShortGptUI
app = ShortGptUI()
app.launch()
```

#### 2. Video Generation Pipeline
```python
# shortGPT/engine/content_short_engine.py
# The 12 steps to create a video:

Step 1:  _generateScript      # AI writes the script
Step 2:  _generateTempAudio   # Convert to speech
Step 3:  _speedUpAudio        # Adjust speed
Step 4:  _timeCaptions        # Sync words with audio
Step 5:  _generateImageSearchTerms  # Find relevant images
Step 6:  _generateImageUrls   # Search Bing for images
Step 7:  _chooseBackgroundMusic     # Select music
Step 8:  _chooseBackgroundVideo     # Select video
Step 9:  _prepareBackgroundAssets   # Download/process
Step 10: _prepareCustomAssets       # Add watermark etc
Step 11: _editAndRenderShort        # Create final video
Step 12: _addYoutubeMetadata        # Add title/description
```

---

## 🧪 Student Exercises

### Beginner
1. Change the TTS voice in `learn_shortgpt.py`
2. Modify the script generation prompt
3. Change video dimensions

### Intermediate
4. Add a background image instead of solid color
5. Add background music that loops
6. Display the script text on screen

### Advanced
7. Add word-by-word animated captions
8. Integrate a different AI model (OpenAI, Claude)
9. Add automatic image search based on script

---

## 🔑 Key Concepts to Explain

### 1. Prompt Engineering
```python
# Good prompt structure:
prompt = """
Role: You are a [specific role]
Task: [What you want]
Rules:
- Rule 1
- Rule 2
Format: [Expected output format]
"""
```

### 2. Video Composition (MoviePy)
```python
from moviepy import *

# Layers work like Photoshop:
# Z-index determines what's on top
background = VideoFileClip("bg.mp4")      # z=0 (bottom)
image = ImageClip("img.png")               # z=1 (middle)
text = TextClip("Hello")                   # z=2 (top)

final = CompositeVideoClip([background, image, text])
```

### 3. Async vs Sync Code
```python
# Sync (blocking) - waits for each line
result1 = slow_function()
result2 = slow_function()  # Waits for result1

# Async (non-blocking) - runs in parallel
async def main():
    result1, result2 = await asyncio.gather(
        slow_function(),
        slow_function()
    )
```

---

## 📝 Assessment Ideas

1. **Quiz:** Name the 12 steps in video generation
2. **Project:** Create a custom video type (recipes, jokes, etc.)
3. **Debug:** Give broken code, ask to fix
4. **Design:** Plan a new feature (whiteboard exercise)

---

## 🛠️ Common Issues & Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| "API key missing" | No key configured | Set in Config tab or .env |
| "FFmpeg not found" | Not installed | `winget install ffmpeg` |
| "Video too short" | Background video < audio | Use longer video or loop |
| "Black video" | Wrong crop settings | Check resize parameters |

---

## 📚 Additional Resources

- [MoviePy Documentation](https://zulko.github.io/moviepy/)
- [Gradio Documentation](https://gradio.app/docs/)
- [Google Gemini API](https://ai.google.dev/)
- [Edge TTS](https://github.com/rany2/edge-tts)

---

## Quick Demo Script

```bash
# 1. Install dependencies
pip install google-generativeai edge-tts moviepy

# 2. Set API key
set GEMINI_API_KEY=your-key-here

# 3. Run simplified version
python learn_shortgpt.py

# 4. Run full version
python runShortGPT.py
```

---

*Created for teaching ShortGPT - AI Video Generation*
