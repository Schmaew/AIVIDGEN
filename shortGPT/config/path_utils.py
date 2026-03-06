import os
import platform
import sys
import subprocess
import subprocess
import tempfile
def search_program(program_name):
    try: 
        search_cmd = "where" if platform.system() == "Windows" else "which"
        return subprocess.check_output([search_cmd, program_name]).decode().strip()
    except subprocess.CalledProcessError:
        return None

def get_program_path(program_name):
    program_path = search_program(program_name)
    if program_path:
        return program_path
    # Fallback: check common Windows installation paths
    if platform.system() == "Windows":
        fallback_paths = [
            r"C:\Users\Paul\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0.1-full_build\bin",
            r"C:\ffmpeg\bin",
            r"C:\Program Files\ffmpeg\bin",
        ]
        for path in fallback_paths:
            full_path = os.path.join(path, f"{program_name}.exe")
            if os.path.exists(full_path):
                return full_path
    return None

def is_running_in_colab():
    return 'COLAB_GPU' in os.environ

def handle_path(path, extension = ".mp4"):
    if 'https' in path:
        if is_running_in_colab():
            temp_file = tempfile.NamedTemporaryFile(suffix= extension, delete=False)
            # The '-y' option overwrites the output file if it already exists.
            command = ['ffmpeg', '-y', '-i', path, temp_file.name]
            subprocess.run(command, check=True)
            temp_file.close()
            return temp_file.name
    return path