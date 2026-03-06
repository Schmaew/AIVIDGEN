"""
================================================================================
🎓 LEARN SHORTGPT - A Teaching Guide for AI Video Generation
================================================================================

This file demonstrates the CORE CONCEPTS of automated video generation.
It's simplified for learning - the full project has more features.

CONCEPTS YOU'LL LEARN:
1. AI Script Generation (using Gemini/OpenAI)
2. Text-to-Speech (TTS) 
3. Video Editing with MoviePy
4. Putting it all together

REQUIREMENTS:
- pip install google-generativeai edge-tts moviepy

================================================================================
"""

import os
import asyncio

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyCxRE9jfhNS8VeBAdENIeMiBNIZJuJJ9pI")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

DEMO_MODE = True  # Change to False when you have a working API key

# Choose which AI to use: "gemini" or "openai"
AI_PROVIDER = "gemini" if GEMINI_API_KEY else "openai"

# Output settings
OUTPUT_FOLDER = "videos"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


# ============================================================================
# STEP 2: AI SCRIPT GENERATION
# ============================================================================
def generate_script(topic: str) -> str:
    """
    Uses AI to generate a video script.
    Supports Gemini, OpenAI, or Demo mode.
    """
    # DEMO MODE: Use a sample script (no API needed)
    if DEMO_MODE:
        sample_scripts = {
            "default": """Did you know the ocean is absolutely WILD?

First, the Mariana Trench is so deep, Mount Everest could fit inside with room to spare.

Second, there's a jellyfish that can literally reverse aging and live forever.

And third, we've only explored about 5 percent of the ocean. 95 percent is still a complete mystery.

The ocean is basically an alien world right here on Earth."""
        }
        script = sample_scripts["default"]
        print(f"📝 Generated Script (DEMO MODE):\n{script}\n")
        return script
    
    # REAL API MODE
    prompt = f"""
    You are a viral TikTok content creator. Generate a short, engaging script about: {topic}
    
    Rules:
    - Maximum 100 words (30 seconds when spoken)
    - Start with a hook that grabs attention
    - Use simple, conversational language
    - End with something memorable
    
    Output ONLY the script, nothing else.
    """
    
    import time
    max_retries = 3
    
    # Demo script fallback
    demo_script = """Did you know the ocean is absolutely WILD?

First, the Mariana Trench is so deep, Mount Everest could fit inside with room to spare.

Second, there's a jellyfish that can literally reverse aging and live forever.

And third, we've only explored about 5 percent of the ocean. 95 percent is still a complete mystery.

The ocean is basically an alien world right here on Earth."""
    
    for attempt in range(max_retries):
        try:
            if AI_PROVIDER == "gemini":
                try:
                    from google import genai
                except ImportError:
                    print("⚠️ google-genai not installed. Run: pip install google-genai")
                    print("   Falling back to demo script...")
                    return demo_script
                client = genai.Client(api_key=GEMINI_API_KEY)
                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=prompt
                )
                script = response.text.strip()
            else:
                try:
                    from openai import OpenAI
                except ImportError:
                    print("⚠️ openai not installed. Run: pip install openai")
                    print("   Falling back to demo script...")
                    return demo_script
                client = OpenAI(api_key=OPENAI_API_KEY)
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}]
                )
                script = response.choices[0].message.content.strip()
            
            print(f"📝 Generated Script:\n{script}\n")
            return script
            
        except Exception as e:
            if "429" in str(e) or "quota" in str(e).lower():
                wait_time = 20 * (attempt + 1)
                print(f"⏳ Rate limited. Waiting {wait_time}s before retry ({attempt+1}/{max_retries})...")
                time.sleep(wait_time)
            else:
                print(f"⚠️ API error: {e}")
                print("   Falling back to demo script...")
                return demo_script
    
    # If all retries failed, use demo script
    print("⚠️ API quota exhausted. Using demo script instead.")
    return demo_script


# ============================================================================
# STEP 3: TEXT-TO-SPEECH (TTS)
# ============================================================================
# VALID EDGE TTS VOICES (Microsoft voices only!)
# Male:   en-US-GuyNeural, en-US-ChristopherNeural, en-GB-RyanNeural
# Female: en-US-JennyNeural, en-US-AriaNeural, en-GB-SoniaNeural
# DO NOT use Google voices like "en-US-Wavenet-D" - they won't work!
VOICE = "en-US-GuyNeural"

async def generate_voice_async(script: str, output_path: str) -> str:
    import edge_tts
    
    # Validate voice name (must end with "Neural" for Edge TTS)
    voice = VOICE
    if not voice.endswith("Neural"):
        print(f"⚠️ Invalid voice '{voice}'. Must be an Edge TTS voice (ends with 'Neural')")
        print("   Using default: en-US-GuyNeural")
        voice = "en-US-GuyNeural"
    
    # Generate the audio
    communicate = edge_tts.Communicate(script, voice)
    await communicate.save(output_path)
    
    print(f"🔊 Voice generated: {output_path}")
    return output_path


def generate_voice(script: str, output_path: str) -> str:
    return asyncio.run(generate_voice_async(script, output_path))


# ============================================================================
# STEP 4: VIDEO CREATION WITH MOVIEPY
# ============================================================================
def create_video(audio_path: str, output_path: str, background_color=(255, 255, 25)) -> str:
    """
    Creates a simple video with the voiceover.
    
    HOW IT WORKS:
    - Load the audio file
    - Create a background (solid color or image)
    - Combine them into a video file
    
    In the full project, we also add:
    - Background videos from YouTube
    - Images that match the script
    - Animated captions
    - Music
    """
    from moviepy import AudioFileClip, ColorClip
    
    # Load the voiceover audio
    audio = AudioFileClip(audio_path)
    duration = audio.duration
    
    # Create a simple colored background
    # Size is 1080x1920 (vertical video for TikTok/Shorts)
    video = ColorClip(size=(1080, 1920), color=background_color, duration=duration)
    
    # Add the audio to the video
    video = video.with_audio(audio)
    
    # Export the final video
    video.write_videofile(
        output_path,
        fps=24,
        codec='libx264',
        audio_codec='aac'
    )
    
    # Close clips to release file handles
    audio.close()
    video.close()
    
    print(f"🎬 Video created: {output_path}")
    return output_path


# ============================================================================
# STEP 5: PUTTING IT ALL TOGETHER
# ============================================================================
def create_short_video(topic: str) -> str:
    """
    Main function that orchestrates the entire video creation process.
    
    THE PIPELINE:
    1. Generate script with AI
    2. Convert script to speech
    3. Create video with the voiceover
    4. Save final video
    """
    print(f"\n{'='*60}")
    print(f"🚀 Creating video about: {topic}")
    print(f"{'='*60}\n")
    
    print("Step 1: Generating script with AI...")
    script = generate_script(topic)

    print("\nStep 2: Converting script to speech...")
    audio_path = os.path.join(OUTPUT_FOLDER, "temp_audio.mp3")
    generate_voice(script, audio_path)
    
    print("\nStep 3: Creating video...")
    video_path = os.path.join(OUTPUT_FOLDER, f"{topic.replace(' ', '_')}_short.mp4")
    create_video(audio_path, video_path)
    
    # Clean up temp audio after video is fully created
    try:
        if os.path.exists(audio_path):
            os.remove(audio_path)
    except Exception as e:
        print(f"⚠️ Could not delete temp audio: {e}")
    
    print(f"\n{'='*60}")
    print(f"✅ DONE! Video saved to: {video_path}")
    print(f"{'='*60}\n")
    
    return video_path


# ============================================================================
# STEP 6: RUN IT!
# ============================================================================
if __name__ == "__main__":
    TOPIC = "3 mind-blowing facts about the ocean"
    
    if not GEMINI_API_KEY and not OPENAI_API_KEY:
        print("⚠️  Please set an API key first!")
        print("   Option 1 (Gemini): set GEMINI_API_KEY=your-key")
        print("   Option 2 (OpenAI): set OPENAI_API_KEY=your-key")
    else:
        print(f"Using AI provider: {AI_PROVIDER.upper()}")
        create_short_video(TOPIC)


# ============================================================================
# 📚 TEACHING NOTES
# ============================================================================
"""
CONCEPTS DEMONSTRATED:

1. API INTEGRATION
   - How to call external AI services (Gemini)
   - Prompt engineering for specific outputs

2. ASYNC PROGRAMMING
   - Edge TTS uses async/await
   - asyncio.run() bridges sync and async code

3. VIDEO PROCESSING
   - MoviePy for video editing
   - Combining audio and video
   - Video codecs and formats

4. FILE MANAGEMENT
   - Creating directories
   - Temp files and cleanup
   - Output organization

EXERCISES FOR STUDENTS:

1. EASY: Change the TTS voice to a different one
2. MEDIUM: Add a background image instead of solid color
3. HARD: Add text captions that appear on screen
4. ADVANCED: Add background music that loops

FULL PROJECT FEATURES NOT SHOWN HERE:
- YouTube video backgrounds
- Bing image search for visuals
- Animated word-by-word captions
- Whisper for audio transcription
- Multiple video templates
- Gradio web UI
"""
