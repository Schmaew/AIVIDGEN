import os
import random
import yt_dlp
import subprocess
import json
from shortGPT.config.path_utils import get_program_path

def getYoutubeVideoLink(url):
    format_filter = "[height<=1920]" if 'shorts' in url else "[height<=1080]"
    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "no_color": True,
        "no_call_home": True,
        "no_check_certificate": True,
        # Look for m3u8 formats first, then fall back to regular formats
        "format": f"bestvideo[ext=m3u8]{format_filter}/bestvideo{format_filter}"
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            dictMeta = ydl.extract_info(
                url,
                download=False)
            return dictMeta['url'], dictMeta['duration']
    except Exception as e:
        raise Exception(f"Failed getting video link from the following video/url {url} {e.args[0]}")

def extract_random_clip_from_video(video_url, video_duration, clip_duration, output_file):
    """Extracts a clip from a video using a signed URL.
    Args:
        video_url (str): The signed URL of the video.
        video_duration (int): Duration of the video.
        clip_duration (int): The duration of the clip in seconds.
        output_file (str): The output file path for the extracted clip.
    """
    if not video_duration:
        raise Exception("Could not get video duration")
    
    ffmpeg_path = get_program_path("ffmpeg") or "ffmpeg"
    
    # If video is shorter than needed, loop it
    if video_duration < clip_duration + 5:
        print(f"Background video ({int(video_duration)}s) shorter than clip ({int(clip_duration)}s), will loop video")
        # Use stream_loop to loop the video
        command = [
            ffmpeg_path,
            '-y',
            '-loglevel', 'error',
            '-stream_loop', '-1',  # Loop indefinitely
            '-i', video_url,
            '-t', str(clip_duration),
            '-c:v', 'libx264',
            '-preset', 'ultrafast',
            output_file
        ]
    else:
        # Normal extraction - pick random start point
        usable_duration = video_duration * 0.85  # Use 85% of video
        max_start = max(0, usable_duration - clip_duration)
        start_time = video_duration * 0.05 + random.random() * max_start
        
        command = [
            ffmpeg_path,
            '-y',
            '-loglevel', 'error',
            '-ss', str(start_time),
            '-t', str(clip_duration),
            '-i', video_url,
            '-c:v', 'libx264',
            '-preset', 'ultrafast',
            output_file
        ]
    
    subprocess.run(command, check=True)
    
    if not os.path.exists(output_file):
        raise Exception("Random clip failed to be written")
    return output_file


def get_aspect_ratio(video_file):
    ffprobe_path = get_program_path("ffprobe") or "ffprobe"
    cmd = '{} -i "{}" -v quiet -print_format json -show_format -show_streams'.format(ffprobe_path, video_file)
#     jsonstr = subprocess.getoutput(cmd)
    jsonstr = subprocess.check_output(cmd, shell=True, encoding='utf-8')
    r = json.loads(jsonstr)
    # look for "codec_type": "video". take the 1st one if there are mulitple
    video_stream_info = [x for x in r['streams'] if x['codec_type']=='video'][0]
    if 'display_aspect_ratio' in video_stream_info and video_stream_info['display_aspect_ratio']!="0:1":
        a,b = video_stream_info['display_aspect_ratio'].split(':')
        dar = int(a)/int(b)
    else:
        # some video do not have the info of 'display_aspect_ratio'
        w,h = video_stream_info['width'], video_stream_info['height']
        dar = int(w)/int(h)
        ## not sure if we should use this
        #cw,ch = video_stream_info['coded_width'], video_stream_info['coded_height']
        #sar = int(cw)/int(ch)
    if 'sample_aspect_ratio' in video_stream_info and video_stream_info['sample_aspect_ratio']!="0:1":
        # some video do not have the info of 'sample_aspect_ratio'
        a,b = video_stream_info['sample_aspect_ratio'].split(':')
        sar = int(a)/int(b)
    else:
        sar = dar
    par = dar/sar
    return dar