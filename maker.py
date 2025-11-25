import random
import os
import glob
from gtts import gTTS
from moviepy.editor import *

def create_short():
    # --- 1. LOAD FACTS FROM FILE ---
    try:
        with open("facts.txt", "r", encoding="utf-8") as f:
            # Read lines and remove empty ones
            facts = [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        print("❌ ERROR: facts.txt not found! Please upload it.")
        return

    if not facts:
        print("❌ ERROR: facts.txt is empty!")
        return

    # Pick ONE random fact
    fact_text = random.choice(facts)
    print(f"1. Selected Fact: {fact_text}")
    
    # --- 2. GENERATE AUDIO ---
    print("2. Generating Voiceover...")
    tts = gTTS(text=fact_text, lang='en', slow=False)
    tts.save("voice.mp3")
    audio_clip = AudioFileClip("voice.mp3")
    
    # --- 3. PICK RANDOM BACKGROUND ---
    # This looks for ANY file starting with 'bg' and ending in '.mp4'
    # It works for bg1.mp4, bg2.mp4 ... bg100.mp4
    available_bgs = glob.glob("bg*.mp4")
    
    if not available_bgs:
        print("❌ ERROR: No background videos found! Upload bg1.mp4, bg2.mp4, etc.")
        return
        
    selected_bg = random.choice(available_bgs)
    print(f"3. Using Background: {selected_bg}")
    
    video_clip = VideoFileClip(selected_bg)
    
    # --- 4. EDITING ---
    # Resize to Vertical (9:16)
    video_clip = video_clip.resize(height=1920)
    video_clip = video_clip.crop(x1=None, y1=None, x2=None, y2=None, width=1080, height=1920, x_center=1080/2, y_center=1920/2)
    
    # Loop video to match audio length
    final_clip = video_clip.loop(duration=audio_clip.duration + 1.5)
    
    # --- 5. ADD TEXT ---
    # White text with black outline
    txt_clip = TextClip(fact_text, fontsize=70, color='white', stroke_color='black', stroke_width=2, font='Liberation-Sans-Bold', method='caption', size=(900, 1500))
    txt_clip = txt_clip.set_position('center').set_duration(audio_clip.duration + 1.5)
    
    final_video = CompositeVideoClip([final_clip, txt_clip])
    final_video = final_video.set_audio(audio_clip)
    
    # --- 6. EXPORT ---
    print("4. Rendering...")
    final_video.write_videofile("output.mp4", fps=24, codec='libx264', audio_codec='aac')
    print("✅ Video Generated Successfully!")

if __name__ == "__main__":
    create_short()
