### How to Get the Detailed Information about a YouTube Video?

Get detailed information about a YouTube video.
    
```python
import subprocess
import json

# The URL of the YouTube video to get information from 
url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# Run the command to get the video information
cmd = [
    'yt-dlp',
    '--dump-json',
    '--no-playlist',
    url
]

# Run the command and get the result
result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

# Parse JSON response
video_info = json.loads(result.stdout)

# Extract and format information
info_result = []
print(f"YouTube Video: {video_info.get('title', 'Unknown title')}")
print("=" * 50)

# Basic info
print(f"Video ID: {video_info.get('id', 'Unknown')}")
print(f"URL: {video_info.get('webpage_url', url)}")
print(f"Duration: {video_info.get('duration_string', 'Unknown')}")
print(f"Upload date: {video_info.get('upload_date', 'Unknown')}")

# Channel info
print(f"Channel: {video_info.get('uploader', 'Unknown')}")
print(f"Channel ID: {video_info.get('channel_id', 'Unknown')}")
print(f"Channel URL: {video_info.get('channel_url', 'Unknown')}")

# Stats
print(f"View count: {video_info.get('view_count', 'Unknown')}")
print(f"Like count: {video_info.get('like_count', 'Unknown')}")
print(f"Comment count: {video_info.get('comment_count', 'Unknown')}")

# Description
description = video_info.get('description', '')
if description:
    # Limit description length
    if len(description) > 500: # you can change the length of the description
        description = description[:500] + "..."
    print(f"\nDescription:")
    print(description)

# Tags
tags = video_info.get('tags', [])
if tags:
    print(f"\nTags: {', '.join(tags[:10])}")
    if len(tags) > 10: # you can change the number of tags to print
        print(f"... and {len(tags) - 10} more tags")

# Categories
categories = video_info.get('categories', [])
if categories:
    print(f"Categories: {', '.join(categories)}")

# Available formats info
formats = video_info.get('formats', [])
if formats:
    print(f"\nAvailable formats: {len(formats)}")
    
    # Show some format details
    video_formats = [f for f in formats if f.get('vcodec', 'none') != 'none']
    audio_formats = [f for f in formats if f.get('acodec', 'none') != 'none' and f.get('vcodec', 'none') == 'none']
    
    if video_formats:
        best_video = max(video_formats, key=lambda x: x.get('height', 0))
        print(f"Best video quality: {best_video.get('height', 'Unknown')}p")
    
    if audio_formats:
        best_audio = max(audio_formats, key=lambda x: x.get('abr', 0))
        print(f"Best audio quality: {best_audio.get('abr', 'Unknown')} kbps")

# Thumbnail
thumbnail = video_info.get('thumbnail')
if thumbnail:
    print(f"Thumbnail: {thumbnail}")
```

### How to Extract the Whole Audio Sound from an Online YouTube Video?

Extract audio from a YouTube video and save as a local MP3 file.
    
```python
import os
import yt_dlp
from urllib.parse import urlparse, parse_qs
from mutagen.mp3 import MP3


# The URL of the YouTube video to extract audio from
url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# Extract the video ID from the URL
video_id = None

if 'youtube.com' in url:
    parsed_url = urlparse(url)
    video_id = parse_qs(parsed_url.query).get('v', [None])[0]
elif 'youtu.be' in url:
    parsed_url = urlparse(url)
    video_id = parsed_url.path.lstrip('/')

if not video_id:
    print(f"Error: Could not extract video ID from URL: {url}")

# Create the output template for the downloaded audio file
output_template = os.path.join("downloads", f"{video_id}_%(title)s.%(ext)s")

# Set the options for the YouTube downloader
ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': output_template,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'quiet': True,
    'no_warnings': True,
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:

    # Extract info first
    info = ydl.extract_info(url, download=False)
    
    print(f"YouTube Audio Extraction\n")
    print(f"Video URL: {url}\n")
    print(f"Video ID: {video_id}\n")
    print(f"Title: {info.get('title', 'N/A')}\n")
    print(f"Uploader: {info.get('uploader', 'N/A')}\n")
    
    # Duration
    duration = info.get('duration')
    if duration:
        minutes, seconds = divmod(duration, 60)
        hours, minutes = divmod(minutes, 60)
        if hours:
            duration_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        else:
            duration_str = f"{minutes:02d}:{seconds:02d}"
        print(f"Duration: {duration_str}\n")
    
    print("\n")
    
    # Check available audio formats
    formats = info.get('formats', [])
    audio_formats = [f for f in formats if f.get('acodec') != 'none']
    
    if audio_formats:
        best_audio = max(audio_formats, key=lambda x: x.get('abr') or 0)
        print(f"Best available audio quality: {best_audio.get('abr', 'Unknown')} kbps\n")
        print(f"Audio codec: {best_audio.get('acodec', 'Unknown')}\n\n")
    
    # Download audio
    print("Starting audio download...\n")
    ydl.download([url])
    print("Audio download completed.\n")
    
    # Look for downloaded audio file
    audio_files = []
    for file in os.listdir("downloads"):
        if video_id in file and file.endswith('.mp3'):
            audio_files.append(os.path.join("downloads", file))
    
    if audio_files:
        for audio_file in audio_files:
            file_size = os.path.getsize(audio_file)
            file_size_mb = file_size / (1024 * 1024)
            
            print(f"\nDownloaded audio file: {audio_file}\n") # Print the path to the downloaded audio file
            print(f"File size: {file_size_mb:.2f} MB\n")
            
            # get audio metadata
            audio = MP3(audio_file)
            print(f"Audio length: {audio.info.length:.2f} seconds\n")
            print(f"Bitrate: {audio.info.bitrate} bps\n")
    else:
        print("Audio file not found after download. Check downloads directory.\n")
```

### How to Catch A Screenshot from the Middle of A YouTube Video?

Get a screenshot from a YouTube video at the specified timestamp. Returns The path to the downloaded screenshot file.

Download video segment and extract screenshot.
```python
import os
import json
import tempfile
import subprocess

# The URL of the YouTube video to get a screenshot from
url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
# The timestamp of the video to get a screenshot from, for example, "00:01:30" for the 1 minute 30 seconds mark
timestamp = "00:02:20"

# Get video info for filename generation
info_cmd = [
    'yt-dlp',
    '--dump-json',
    '--no-playlist',
    url
]

result = subprocess.run(info_cmd, capture_output=True, text=True, timeout=30)

if result.returncode != 0:
    print(f"Error getting video info: {result.stderr}")

video_info = json.loads(result.stdout)
video_id = video_info.get('id', 'unknown')
video_title = video_info.get('title', 'Unknown Video')

# Generate output filename
clean_timestamp = timestamp.replace(':', '')
output_path = os.path.join("downloads", f"{video_id}_{clean_timestamp}.jpg")

# Method 1: Download video segment and extract screenshot
def timestamp_to_seconds(ts):
    parts = ts.split(':')
    if len(parts) == 3:  # HH:MM:SS
        return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
    elif len(parts) == 2:  # MM:SS
        return int(parts[0]) * 60 + int(parts[1])
    else:
        return int(parts[0])

start_seconds = timestamp_to_seconds(timestamp)
end_seconds = start_seconds + 5  # Download 5 second segment, change it if you want to download a different segment (e.g. 10 seconds)

# Create temp file
with tempfile.NamedTemporaryFile(suffix='.%(ext)s', delete=False, dir="downloads") as temp_file:
    temp_template = temp_file.name

# Download video segment using yt-dlp
download_cmd = [
    'yt-dlp',
    '--format', 'best[height<=720]',
    '--external-downloader', 'ffmpeg',
    '--external-downloader-args', f'ffmpeg_i:-ss {start_seconds} -t 5',
    '--output', temp_template,
    url
]

download_result = subprocess.run(download_cmd, capture_output=True, text=True, timeout=120)

# Find downloaded file
downloaded_file = None
for ext in ['mp4', 'webm', 'mkv', 'flv']:
    potential_file = temp_template.replace('.%(ext)s', f'.{ext}')
    if os.path.exists(potential_file):
        downloaded_file = potential_file
        break

if downloaded_file and os.path.exists(downloaded_file):
    # Extract screenshot from video segment
    ffmpeg_cmd = [
        'ffmpeg',
        '-i', downloaded_file,
        '-ss', '0',  # Screenshot from segment start
        '-vframes', '1',
        '-q:v', '2',
        '-y',
        output_path
    ]
    
    ffmpeg_result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True, timeout=30)
    
    # Clean up temp file
    os.remove(downloaded_file)
    
    if ffmpeg_result.returncode == 0 and os.path.exists(output_path):
        file_size = os.path.getsize(output_path)
        print(f"Screenshot captured successfully!\nVideo: {video_title}\nTimestamp: {timestamp}\nSaved to: {output_path}\nFile size: {file_size} bytes")
    else:
        print(f"Screenshot failed.")
else:
    print(f"Screenshot failed.")
```

An alternative that directly screenshot with `yt-dlp` + `ffmpeg`.
```python
import os
import json
import subprocess

# The URL of the YouTube video to get a screenshot from
url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
# The timestamp of the video to get a screenshot from, for example, "00:01:30" for the 1 minute 30 seconds mark
timestamp = "00:02:20"

# Get video info for filename generation
info_cmd = [
    'yt-dlp',
    '--dump-json',
    '--no-playlist',
    url
]

result = subprocess.run(info_cmd, capture_output=True, text=True, timeout=30)

if result.returncode != 0:
    print(f"Error getting video info: {result.stderr}")

video_info = json.loads(result.stdout)
video_id = video_info.get('id', 'unknown')
video_title = video_info.get('title', 'Unknown Video')

# Generate output filename
clean_timestamp = timestamp.replace(':', '')
output_path = os.path.join("downloads", f"{video_id}_{clean_timestamp}.jpg")

screenshot_cmd = [
    'yt-dlp',
    '--format', 'best[height<=720]',
    '--exec', f'ffmpeg -ss {timestamp} -i "{{}}" -vframes 1 -q:v 2 -y "{output_path}"',
    '--exec-before-download', f'echo "Processing video..."',
    url
]

# Run the command to get the screenshot
screenshot_result = subprocess.run(screenshot_cmd, capture_output=True, text=True, timeout=180)
file_size = os.path.getsize(output_path)
print(f"Screenshot captured successfully!\nVideo: {video_title}\nTimestamp: {timestamp}\nSaved to: {output_path}\nFile size: {file_size} bytes")
```

### How to Get Subtitles from a YouTube Video?

Get subtitles from a YouTube video in the specified language. Supports manual subtitles, auto-generated subtitles, and fallback to common languages.

```python
import json
import os
import glob
import subprocess

# The URL of the YouTube video to get subtitles from
url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
# The language of the subtitles to get, for example, "en" for English, "zh" for Chinese, "es" for Spanish, "fr" for French, "de" for German, "ja" for Japanese, "ko" for Korean
language = "en"

downloads_dir = "downloads"
os.makedirs(downloads_dir, exist_ok=True)

# Get video info first
info_cmd = [
    'yt-dlp',
    '--dump-json',
    '--no-playlist',
    url
]

info_result = subprocess.run(info_cmd, capture_output=True, text=True, timeout=30)

if info_result.returncode != 0:
    print(f"Error getting video info: {info_result.stderr}")
    exit(1)

video_info = json.loads(info_result.stdout)
video_id = video_info.get('id', 'unknown')
video_title = video_info.get('title', 'Unknown Video')
output_path = os.path.join(downloads_dir, video_id)

print(f"YouTube Subtitle Download")
print("=" * 50)
print(f"Video: {video_title}")
print(f"Video ID: {video_id}")
print(f"Requested language: {language}")
print()

# Try to download manual subtitles first
print("Attempting to download manual subtitles...")
subtitle_cmd = [
    'yt-dlp',
    '--write-sub',
    '--skip-download',
    '--sub-format', 'srt',
    '--sub-langs', language,
    '-o', output_path,
    url
]

result = subprocess.run(subtitle_cmd, capture_output=True, text=True, timeout=60)

# Check if subtitles were downloaded
subtitle_files = glob.glob(f"{output_path}*.srt")

if result.returncode == 0 and subtitle_files:
    subtitle_file = subtitle_files[0]
    file_size = os.path.getsize(subtitle_file)
    
    print(f"Manual subtitles downloaded successfully!")
    print(f"File: {subtitle_file}")
    print(f"File size: {file_size} bytes")
    print()
    
    # Read and display the complete subtitle content
    with open(subtitle_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("Complete subtitles:")
    print("-" * 30)
    print(content)

# If specified language failed, try auto-generated subtitles
elif not subtitle_files:
    print("Manual subtitles not available. Trying auto-generated subtitles...")
    auto_cmd = [
        'yt-dlp',
        '--write-auto-sub',
        '--skip-download',
        '--sub-format', 'srt',
        '--sub-langs', language,
        '-o', output_path,
        url
    ]
    
    auto_result = subprocess.run(auto_cmd, capture_output=True, text=True, timeout=60)
    subtitle_files = glob.glob(f"{output_path}*.srt")
    
    if auto_result.returncode == 0 and subtitle_files:
        subtitle_file = subtitle_files[0]
        file_size = os.path.getsize(subtitle_file)
        
        print(f"Auto-generated subtitles downloaded successfully!")
        print(f"File: {subtitle_file}")
        print(f"File size: {file_size} bytes")
        print("Note: These are auto-generated subtitles")
        print()
        
        # Read and display the subtitle content
        with open(subtitle_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("Complete subtitles:")
        print("-" * 30)
        print(content)

# If still no subtitles, try common languages
if not subtitle_files:
    print("Auto-generated subtitles not available. Trying common languages...")
    common_languages = ['en', 'zh-Hans', 'zh-Hant', 'es', 'fr', 'de', 'ja', 'ko']
    
    for lang in common_languages:
        if lang == language:
            continue
        
        print(f"Trying language: {lang}")
        lang_cmd = [
            'yt-dlp',
            '--write-sub',
            '--skip-download',
            '--sub-format', 'srt',
            '--sub-langs', lang,
            '-o', output_path,
            url
        ]
        
        lang_result = subprocess.run(lang_cmd, capture_output=True, text=True, timeout=30)
        subtitle_files = glob.glob(f"{output_path}*.srt")
        
        if lang_result.returncode == 0 and subtitle_files:
            subtitle_file = subtitle_files[0]
            file_size = os.path.getsize(subtitle_file)
            
            print(f"Subtitles found in different language!")
            print(f"Requested: {language}, Found: {lang}")
            print(f"File: {subtitle_file}")
            print(f"File size: {file_size} bytes")
            print()
            
            # Read and display the subtitle content
            with open(subtitle_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            print("Complete subtitles:")
            print("-" * 30)
            print(content)
            
            break

if not subtitle_files:
    print(f"No subtitles available for this video.")
    print(f"Requested language: {language}")
    print("Tried manual, auto-generated, and common languages, but none were found.")
```