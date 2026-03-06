from urllib.error import HTTPError
from shortGPT.config.path_utils import get_program_path
import os
from shortGPT.config.path_utils import handle_path
import numpy as np
from typing import Any, Dict, List, Union
from moviepy import (AudioFileClip, CompositeVideoClip, CompositeAudioClip, ImageClip,
                    TextClip, VideoFileClip, AudioClip)
from moviepy.Clip import Clip
from moviepy import vfx, afx
from shortGPT.editing_framework.rendering_logger import MoviepyProgressLogger
import json

def load_schema(json_path):
    return json.loads(open(json_path, 'r', encoding='utf-8').read())

class CoreEditingEngine:

    def generate_image(self, schema:Dict[str, Any],output_file , logger=None):
        assets = dict(sorted(schema['visual_assets'].items(), key=lambda item: item[1]['z']))
        clips = []

        for asset_key in assets:
            asset = assets[asset_key]
            asset_type = asset['type']
            if asset_type == 'image':
                clip = self.process_image_asset(asset)
            elif asset_type == 'text':
                clip = self.process_text_asset(asset)
                clips.append(clip)
            else:
                raise ValueError(f'Invalid asset type: {asset_type}')
            clips.append(clip)

        image = CompositeVideoClip(clips)
        image.save_frame(output_file)
        return output_file

    def generate_video(self, schema:Dict[str, Any], output_file, logger=None, force_duration=None, threads=None) -> None:
        import os
        
        # Convert to absolute path to ensure file is written correctly
        output_file = os.path.abspath(output_file)
        output_dir = os.path.dirname(output_file)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        print(f"DEBUG: Output directory: {output_dir}")
        print(f"DEBUG: Output file (absolute): {output_file}")
        
        visual_assets = dict(sorted(schema['visual_assets'].items(), key=lambda item: item[1]['z']))
        audio_assets = dict(sorted(schema['audio_assets'].items(), key=lambda item: item[1]['z']))
        
        visual_clips = []
        background_clip = None
        
        for asset_key in visual_assets:
            asset = visual_assets[asset_key]
            asset_type = asset['type']
            try:
                if asset_type == 'video':
                    clip = self.process_video_asset(asset)
                    if 'background' in asset_key:
                        background_clip = clip
                elif asset_type == 'image':
                    clip = self.process_image_asset(asset)
                elif asset_type == 'text':
                    clip = self.process_text_asset(asset)
                else:
                    raise ValueError(f'Invalid asset type: {asset_type}')
                visual_clips.append(clip)
            except Exception as e:
                print(f"WARNING: Failed to load {asset_type} asset '{asset_key}': {str(e)}")
                continue
        
        audio_clips = []
        for asset_key in audio_assets:
            asset = audio_assets[asset_key]
            asset_type = asset['type']
            try:
                if asset_type == "audio":
                    audio_clip = self.process_audio_asset(asset)
                    audio_clips.append(audio_clip)
                else:
                    raise ValueError(f"Invalid asset type: {asset_type}")
            except Exception as e:
                print(f"WARNING: Failed to load audio asset '{asset_key}': {str(e)}")
                continue

        print(f"DEBUG: Loaded {len(visual_clips)} visual clips, {len(audio_clips)} audio clips")
        
        if not visual_clips:
            raise Exception("No visual clips to render - all assets failed to load")
        
        # Force video size to 1080x1920 (vertical short format)
        video = CompositeVideoClip(visual_clips, size=(1080, 1920))
        audio = None
        
        if audio_clips:
            audio = CompositeAudioClip(audio_clips)
            video = video.with_audio(audio)
            video = video.with_duration(audio.duration)
        if force_duration:
            video = video.with_duration(force_duration)
        
        print(f"DEBUG: Video duration: {video.duration}s, size: {video.size}")
        print(f"DEBUG: Writing video to: {output_file}")
        
        try:
            video.write_videofile(
                output_file, 
                threads=threads or 4,
                codec='libx264', 
                audio_codec='aac', 
                fps=25, 
                preset='veryfast',
                logger='bar',
                temp_audiofile='temp-audio.m4a',
                remove_temp=True
            )
            
            if not os.path.exists(output_file):
                raise Exception(f"Video file was not created at {output_file}")
            
            file_size = os.path.getsize(output_file)
            print(f"DEBUG: Video created successfully! Size: {file_size / 1024 / 1024:.2f} MB")
            
        except Exception as e:
            print(f"ERROR during video rendering: {str(e)}")
            import traceback
            traceback.print_exc()
            raise
        finally:
            try:
                video.close()
                if audio:
                    audio.close()
                for clip in visual_clips:
                    clip.close()
                for clip in audio_clips:
                    clip.close()
            except:
                pass
        
        return output_file
    
    def generate_audio(self, schema:Dict[str, Any], output_file, logger=None) -> None:
        audio_assets = dict(sorted(schema['audio_assets'].items(), key=lambda item: item[1]['z']))
        audio_clips = []

        for asset_key in audio_assets:
            asset = audio_assets[asset_key]
            asset_type = asset['type']
            if asset_type == "audio":
                audio_clip = self.process_audio_asset(asset)
            else:
                raise ValueError(f"Invalid asset type: {asset_type}")

            audio_clips.append(audio_clip)
        audio = CompositeAudioClip(audio_clips)
        audio.fps = 44100
        if logger:
            my_logger = MoviepyProgressLogger(callBackFunction=logger)
            audio.write_audiofile(output_file, logger=my_logger)
        else:
            audio.write_audiofile(output_file)
        return output_file
    # Process common actions
    def process_common_actions(self,
                                   clip: Union[VideoFileClip, ImageClip, TextClip, AudioFileClip],
                                   actions: List[Dict[str, Any]]) -> Union[VideoFileClip, AudioFileClip, ImageClip, TextClip]:
        for action in actions:
            if action['type'] == 'set_time_start':
                clip = clip.with_start(action['param'])
                continue
   
            if action['type'] == 'set_time_end':
                clip = clip.with_end(action['param'])
                continue
            
            if action['type'] == 'subclip':
                clip = clip.subclipped(**action['param'])
                continue

        return clip

    # Process common visual clip actions
    def process_common_visual_actions(self,
                                   clip: Clip,
                                   actions: List[Dict[str, Any]]) -> Union[VideoFileClip, ImageClip, TextClip]:
        clip = self.process_common_actions(clip, actions)
        for action in actions:
 
            if action['type'] == 'resize':
                clip = clip.with_effects([vfx.Resize(**action['param'])])
                continue

            if action['type'] == 'crop':
                clip = clip.with_effects([vfx.Crop(**action['param'])])
                continue

            if action['type'] == 'screen_position':
                clip = clip.with_position(**action['param'])
                continue

            if action['type'] == 'green_screen':
                params = action['param']
                color = params['color'] if  params['color'] else [52, 255, 20]
                thr = params["threshold"] if params["threshold"] else 100
                s = params['stiffness'] if params['stiffness'] else 5
                clip = clip.with_effects([vfx.MaskColor(color=color,threshold=thr, stiffness=s)])
                continue

            if action['type'] == 'normalize_image':
                clip = clip.image_transform(self.__normalize_frame)
                continue

            if action['type'] == 'auto_resize_image':
                ar = clip.aspect_ratio
                height = action['param']['maxHeight']
                width = action['param']['maxWidth']
                if ar <1:
                    clip = clip.with_effects([vfx.Resize((height*ar, height))])
                else:
                    clip = clip.with_effects([vfx.Resize((width, width/ar))])
                continue

            if action['type'] == 'resize_and_center_crop':
                target_w = action['param']['target_width']
                target_h = action['param']['target_height']
                target_ratio = target_w / target_h
                
                clip_w, clip_h = clip.size
                clip_ratio = clip_w / clip_h
                
                if clip_ratio > target_ratio:
                    new_h = target_h
                    new_w = int(clip_ratio * target_h)
                else:
                    new_w = target_w
                    new_h = int(target_w / clip_ratio)
                
                clip = clip.with_effects([vfx.Resize((new_w, new_h))])
                
                x_center = (new_w - target_w) // 2
                y_center = (new_h - target_h) // 2
                clip = clip.with_effects([vfx.Crop(x1=x_center, y1=y_center, x2=x_center + target_w, y2=y_center + target_h)])
                continue

        return clip

    # Process audio actions
    def process_audio_actions(self, clip: AudioClip,
                            actions: List[Dict[str, Any]]) -> AudioClip:
        clip = self.process_common_actions(clip, actions)
        for action in actions:
            if action['type'] == 'normalize_music':
                clip = clip.with_effects([afx.AudioNormalize()])
                continue

            if action['type'] == 'loop_background_music':
                target_duration = action['param']
                start = clip.duration * 0.15
                clip = clip.subclipped(start)
                clip = clip.with_effects([afx.AudioLoop(duration=target_duration)])
                continue

            if action['type'] == 'volume_percentage':
                clip = clip.with_effects([afx.MultiplyVolume(action['param'])])
                continue

        return clip
    # Process individual asset types
    def process_video_asset(self, asset: Dict[str, Any]) -> VideoFileClip:
        params = {
            'filename': handle_path(asset['parameters']['url'])
        }
        if 'audio' in asset['parameters']:
            params['audio'] = asset['parameters']['audio']
        clip = VideoFileClip(**params)
        return self.process_common_visual_actions(clip, asset['actions'])

    def process_image_asset(self, asset: Dict[str, Any]) -> ImageClip:
        clip = ImageClip(asset['parameters']['url'])
        return self.process_common_visual_actions(clip, asset['actions'])

    def process_text_asset(self, asset: Dict[str, Any]) -> TextClip:
        text_clip_params = asset['parameters']
        
        if not (any(key in text_clip_params for key in ['text','fontsize', 'size'])):
            raise Exception('You must include at least a size or a fontsize to determine the size of your text')
        text_method = text_clip_params.get('method', 'label')
        clip_info = {
            'text': text_clip_params['text'],
            'font': text_clip_params.get('font'),
            'font_size': text_clip_params.get('font_size'),
            'color': text_clip_params.get('color'),
            'stroke_width': text_clip_params.get('stroke_width'),
            'stroke_color': text_clip_params.get('stroke_color'),
            'size': text_clip_params.get('size'),
            'method': text_method,
            'text_align': text_clip_params.get('text_align', 'center')
        }
        clip_info = {k: v for k, v in clip_info.items() if v is not None}
        clip = TextClip(**clip_info)
        return self.process_common_visual_actions(clip, asset['actions'])

    def process_audio_asset(self, asset: Dict[str, Any]) -> AudioFileClip:
        clip = AudioFileClip(asset['parameters']['url'])
        return self.process_audio_actions(clip, asset['actions'])
    
    def __normalize_image(self, clip):
        def f(get_frame, t):
            if f.normalized_frame is not None:
                return f.normalized_frame
            else:
                frame = get_frame(t)
                f.normalized_frame = self.__normalize_frame(frame)
                return f.normalized_frame

        f.normalized_frame = None

        return clip.fl(f)


    def __normalize_frame(self, frame):
        shape = np.shape(frame)
        [dimensions, ] = np.shape(shape)

        if dimensions == 2:
            (height, width) = shape
            normalized_frame = np.zeros((height, width, 3))
            for y in range(height):
                for x in range(width):
                    grey_value = frame[y][x]
                    normalized_frame[y][x] = (grey_value, grey_value, grey_value)
            return normalized_frame
        else:
            return frame
        

