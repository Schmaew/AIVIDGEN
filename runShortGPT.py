import os
import platform

# Add FFmpeg to PATH at startup for Windows
if platform.system() == "Windows":
    ffmpeg_paths = [
        r"C:\Users\Paul\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0.1-full_build\bin",
        r"C:\ffmpeg\bin",
        r"C:\Program Files\ffmpeg\bin",
    ]
    for path in ffmpeg_paths:
        if os.path.exists(path):
            os.environ["PATH"] = path + os.pathsep + os.environ.get("PATH", "")
            break

from gui.gui_gradio import ShortGptUI

app = ShortGptUI(colab=False)
app.launch()