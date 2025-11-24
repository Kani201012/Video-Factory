import random
import os
from gtts import gTTS
from moviepy.editor import *
# We do not need to specify ImageMagick path for Linux/GitHub, it finds it automatically.

# --- CONTENT ---
FACT_TEXT = "Did you know? Octopuses have three hearts. Two pump blood to the gills, while the third pumps it to the rest of the body."

def create_short():
    print("1. Generating Voiceover...")
    tts = gTTS(text=FACT_TEXT, lang='en', slow=False)
    tts.save("voice.mp3")
    
    print("2. Loading Files...")
    audio_clip = AudioFileClip("voice.mp3")
    
    # We will assume you uploaded one background video named 'bg1.mp4'
    # If you have more, add them to the list
    bg_files = ["bg1.mp4"] 
    selected_bg = random.choice(bg_files)
    
    video_clip = VideoFileClip(selected_bg)
    
    print("3. Editing Video...")
    # Resize to HD Vertical
    # Note: If your source video is small, this might pixelate it, but it works for testing
    video_clip = video_clip.resize(height=1920)
    video_clip = video_clip.crop(x1=None, y1=None, x2=None, y2=None, width=1080, height=1920, x_center=1080/2, y_center=1920/2)
    final_clip = video_clip.loop(duration=audio_clip.duration + 1.5)
    
    print("4. Adding Text...")
    # Linux servers handle fonts differently. We use 'Liberation-Sans-Bold' which is standard on Linux.
    txt_clip = TextClip(FACT_TEXT, fontsize=70, color='white', font='Liberation-Sans-Bold', method='caption', size=(900, 1500))
    txt_clip = txt_clip.set_position('center').set_duration(audio_clip.duration + 1.5)
    
    final_video = CompositeVideoClip([final_clip, txt_clip])
    final_video = final_video.set_audio(audio_clip)
    
    print("5. Rendering (This will take time)...")
    # We use 'output.mp4' as the filename
    final_video.write_videofile("output.mp4", fps=24, codec='libx264', audio_codec='aac')
    print("✅ DONE! Video Saved.")

if __name__ == "__main__":
    create_short()
