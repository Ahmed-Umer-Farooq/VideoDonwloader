#!/usr/bin/env python3
"""
Video Downloader Pro - Simple & Easy to Use
Downloads videos directly - No complicated steps!
Version: 3.0.0
"""

import streamlit as st
import yt_dlp
from fake_useragent import UserAgent
import tempfile
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Page Configuration
st.set_page_config(
    page_title="Video Downloader Pro",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def get_random_user_agent():
    """Get a random user agent"""
    try:
        ua = UserAgent()
        return ua.random
    except:
        return "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

def format_size(bytes_size):
    """Format bytes to readable size"""
    if not bytes_size:
        return "Unknown"
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.1f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.1f} TB"

def format_duration(seconds):
    """Format seconds to MM:SS"""
    if not seconds:
        return "Unknown"
    minutes = seconds // 60
    secs = seconds % 60
    return f"{int(minutes)}:{int(secs):02d}"

def validate_url(url, platform_name):
    """Check if URL is valid"""
    url = url.strip()
    if not url:
        return False, "Please enter a URL"
    
    if platform_name == "youtube":
        if not any(d in url.lower() for d in ['youtube.com', 'youtu.be']):
            return False, "Please enter a valid YouTube URL"
    elif platform_name == "tiktok":
        if not any(d in url.lower() for d in ['tiktok.com', 'vm.tiktok.com']):
            return False, "Please enter a valid TikTok URL"
    
    return True, "OK"

def download_video(url, platform_name, progress_callback=None):
    """Download video and return file data"""
    try:
        logger.info(f"Downloading {platform_name}: {url}")
        
        if progress_callback:
            progress_callback("🔍 Getting video information...")
        
        # Create temp directory
        temp_dir = tempfile.mkdtemp()
        
        # Progress hook
        last_progress = [0]
        
        def progress_hook(d):
            if d['status'] == 'downloading' and progress_callback:
                try:
                    percent_str = d.get('_percent_str', '0%').strip()
                    if percent_str != f"{last_progress[0]}%":
                        progress_callback(f"⬇️ Downloading: {percent_str}")
                        last_progress[0] = int(float(percent_str.replace('%', '')))
                except:
                    pass
            elif d['status'] == 'finished' and progress_callback:
                progress_callback("✅ Processing video...")
        
        # Download options
        ydl_opts = {
            "format": "best[ext=mp4]/bestvideo[ext=mp4]+bestaudio[ext=m4a]/best",
            "outtmpl": os.path.join(temp_dir, "video.%(ext)s"),
            "quiet": True,
            "no_warnings": True,
            "progress_hooks": [progress_hook],
            "user_agent": get_random_user_agent(),
            "merge_output_format": "mp4",
        }
        
        if platform_name == "tiktok":
            ydl_opts["http_headers"] = {
                "User-Agent": get_random_user_agent(),
                "Referer": "https://www.tiktok.com/",
            }
        
        # Extract info first
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            title = info.get("title", "video")
            duration = info.get("duration", 0)
            thumbnail = info.get("thumbnail")
            uploader = info.get("uploader", "Unknown")
            
            # Get estimated file size
            formats = info.get("formats", [])
            estimated_size = 0
            for fmt in formats:
                size = fmt.get("filesize") or fmt.get("filesize_approx", 0)
                if size > estimated_size:
                    estimated_size = size
        
        if progress_callback:
            progress_callback(f"⬇️ Downloading: {title}")
        
        # Now download
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        # Find the downloaded file
        video_file = None
        for file in os.listdir(temp_dir):
            if file.startswith("video."):
                video_file = os.path.join(temp_dir, file)
                break
        
        if not video_file or not os.path.exists(video_file):
            return False, None, "Download failed - file not found"
        
        # Read file into memory
        if progress_callback:
            progress_callback("📦 Preparing download...")
        
        with open(video_file, 'rb') as f:
            video_data = f.read()
        
        # Clean up
        try:
            os.remove(video_file)
            os.rmdir(temp_dir)
        except:
            pass
        
        return True, {
            "title": title,
            "duration": duration,
            "thumbnail": thumbnail,
            "uploader": uploader,
            "size": len(video_data),
            "data": video_data,
            "filename": f"{title}.mp4"
        }, None
        
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Error: {error_msg}")
        return False, None, error_msg

def apply_styles():
    """Apply beautiful styles"""
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
        
        * {
            font-family: 'Inter', sans-serif;
        }
        
        .stApp {
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%);
            color: #ffffff;
        }
        
        #MainMenu, footer, header {visibility: hidden;}
        .stDeployButton {display: none;}
        
        .block-container {
            padding: 2rem !important;
            max-width: 1000px !important;
        }
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 1rem;
            background: transparent;
            justify-content: center;
            border-bottom: 2px solid rgba(255, 255, 255, 0.1);
            padding-bottom: 1rem;
            margin-bottom: 2rem;
        }
        
        .stTabs [data-baseweb="tab"] {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            padding: 0.8rem 2rem;
            font-weight: 600;
            color: #888;
            transition: all 0.3s;
        }
        
        .stTabs [data-baseweb="tab"][aria-selected="true"] {
            background: linear-gradient(135deg, #FF0000, #CC0000);
            color: white;
            box-shadow: 0 8px 25px rgba(255, 0, 0, 0.3);
        }
        
        /* Header */
        .main-header {
            text-align: center;
            padding: 2rem 0;
            margin-bottom: 2rem;
        }
        
        .main-title {
            font-size: 3rem;
            font-weight: 900;
            background: linear-gradient(135deg, #FF0000, #FF6B6B);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
        }
        
        .subtitle {
            font-size: 1.2rem;
            color: #888;
        }
        
        /* Cards */
        .info-card {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            padding: 2rem;
            margin: 1.5rem 0;
        }
        
        .video-card {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-left: 4px solid #FF0000;
            border-radius: 12px;
            padding: 1.5rem;
            margin: 1rem 0;
        }
        
        /* Input */
        .stTextInput > div > div > input {
            background: rgba(255, 255, 255, 0.05) !important;
            border: 2px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 12px !important;
            padding: 1.2rem !important;
            color: #fff !important;
            font-size: 1rem !important;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #FF0000 !important;
            box-shadow: 0 0 0 3px rgba(255, 0, 0, 0.1) !important;
        }
        
        /* Buttons */
        .stButton > button {
            background: linear-gradient(135deg, #FF0000, #CC0000) !important;
            color: white !important;
            border: none !important;
            border-radius: 10px !important;
            padding: 0.8rem 2rem !important;
            font-weight: 700 !important;
            font-size: 1rem !important;
            transition: all 0.3s !important;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 10px 30px rgba(255, 0, 0, 0.3) !important;
        }
        
        .stDownloadButton > button {
            background: linear-gradient(135deg, #00C853, #00E676) !important;
            color: white !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 1.2rem 2rem !important;
            font-weight: 700 !important;
            font-size: 1.2rem !important;
            width: 100% !important;
            box-shadow: 0 8px 20px rgba(0,200,83,0.3) !important;
        }
        
        .stDownloadButton > button:hover {
            transform: translateY(-3px) !important;
            box-shadow: 0 12px 30px rgba(0,200,83,0.4) !important;
        }
        
        h2, h3 {
            color: #FF0000 !important;
            font-weight: 700 !important;
        }
        
        .big-text {
            font-size: 1.1rem;
            line-height: 1.6;
            color: #ccc;
        }
        </style>
    """, unsafe_allow_html=True)

def render_tab(platform_name, platform_icon, platform_title):
    """Render download tab"""
    
    st.markdown(f"""
        <div class="main-header">
            <h1 class="main-title">{platform_icon} {platform_title}</h1>
            <p class="subtitle">Download videos easily - Just paste and click!</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Simple instructions
    st.markdown("""
        <div class="info-card">
            <h3 style="margin-top: 0;">📝 How to use:</h3>
            <p class="big-text">
                1️⃣ Copy the video URL from YouTube or TikTok<br>
                2️⃣ Paste it in the box below<br>
                3️⃣ Click "Download Video"<br>
                4️⃣ Wait for processing and click the green download button!
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # URL Input
    url_input = st.text_input(
        "Video URL",
        placeholder=f"Paste your {platform_title.split()[0]} video link here...",
        key=f"{platform_name}_url",
        label_visibility="collapsed"
    )
    
    # Download button
    if st.button(f"🎬 Download Video", type="primary", use_container_width=True, key=f"{platform_name}_download"):
        if not url_input.strip():
            st.error("❌ Please paste a video URL first!")
            return
        
        # Validate URL
        is_valid, message = validate_url(url_input, platform_name)
        if not is_valid:
            st.error(f"❌ {message}")
            return
        
        # Show progress
        progress_placeholder = st.empty()
        
        def update_progress(msg):
            progress_placeholder.info(msg)
        
        success, video_data, error = download_video(
            url_input, 
            platform_name,
            progress_callback=update_progress
        )
        
        progress_placeholder.empty()
        
        if not success:
            st.error(f"❌ Couldn't download this video")
            st.error(f"Error: {error}")
            st.info("💡 Tips:\n- Make sure the video is public\n- Check if the URL is correct\n- Try a different video")
            return
        
        # Show video info
        st.markdown(f"""
            <div class="video-card">
                <h2 style="margin-top: 0; font-size: 1.5rem;">✅ {video_data['title']}</h2>
                <p style="color: #888; margin: 0.5rem 0;">
                    👤 {video_data['uploader']} • 
                    ⏱️ {format_duration(video_data['duration'])} • 
                    💾 {format_size(video_data['size'])}
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        # Show thumbnail
        if video_data.get('thumbnail'):
            st.image(video_data['thumbnail'], use_container_width=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Create download button with actual file
        st.success("✅ Your video is ready! Click the button below to download:")
        
        st.download_button(
            label="⬇️ DOWNLOAD VIDEO NOW",
            data=video_data['data'],
            file_name=video_data['filename'],
            mime="video/mp4",
            use_container_width=True
        )
        
        st.balloons()
    
    # Help section
    with st.expander("ℹ️ Need Help?"):
        st.markdown("""
            **Common Issues:**
            
            • **Download takes too long?**  
              → Large videos take more time, please be patient
            
            • **Video won't download?**  
              → Make sure the video is public and not age-restricted
            
            • **Error message appears?**  
              → Try a different video or check your internet connection
            
            • **Downloaded file won't play?**  
              → Make sure you have a media player installed (VLC recommended)
        """)

def main():
    """Main app"""
    apply_styles()
    
    # Warning about Streamlit Cloud limitations
    st.info("ℹ️ **Note:** This app works best when run locally. On Streamlit Cloud, video size may be limited.")
    
    # Create tabs
    tab1, tab2 = st.tabs(["🎥 YouTube", "🎵 TikTok"])
    
    with tab1:
        render_tab("youtube", "🎥", "YouTube Downloader")
    
    with tab2:
        render_tab("tiktok", "🎵", "TikTok Downloader")
    
    # Footer
    st.markdown("""
        <div style="text-align: center; padding: 2rem 0; color: #666; margin-top: 3rem; border-top: 1px solid rgba(255,255,255,0.1);">
            Video Downloader Pro v3.0 • Simple & Easy<br>
            For personal use only
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Error: {e}")
        st.error("Something went wrong. Please refresh the page.")