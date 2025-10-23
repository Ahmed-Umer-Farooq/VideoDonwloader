#!/usr/bin/env python3
"""
Video Downloader Pro - Simple & Easy to Use
Download videos directly to your device - No technical knowledge needed!
Version: 2.0.0
"""

import streamlit as st
import yt_dlp
from fake_useragent import UserAgent
import time
import logging
import base64
from io import BytesIO

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

# Configuration
class Config:
    VERSION = "2.0.0"
    MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB for in-memory download
    TIMEOUT = 30

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

def get_video_info_and_file(url, platform_name, progress_callback=None):
    """Get video info and download link"""
    try:
        logger.info(f"Processing {platform_name}: {url}")
        
        if progress_callback:
            progress_callback("Getting video information...")
        
        # Get video info
        ydl_opts = {
            "quiet": True,
            "no_warnings": True,
            "skip_download": True,
            "user_agent": get_random_user_agent(),
            "format": "best[ext=mp4]/bestvideo[ext=mp4]+bestaudio[ext=m4a]/best",
        }
        
        if platform_name == "tiktok":
            ydl_opts["http_headers"] = {
                "User-Agent": get_random_user_agent(),
                "Referer": "https://www.tiktok.com/",
            }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
        
        if not info:
            return False, None, "Could not get video information"
        
        title = info.get("title", "video")
        duration = info.get("duration", 0)
        thumbnail = info.get("thumbnail")
        uploader = info.get("uploader", "Unknown")
        
        # Get the best download URL
        download_url = None
        estimated_size = 0
        
        # Try to get direct URL
        if info.get("url"):
            download_url = info.get("url")
            estimated_size = info.get("filesize") or info.get("filesize_approx") or 0
        else:
            # Look through formats for best quality
            formats = info.get("formats", [])
            best_format = None
            best_quality = 0
            
            for fmt in formats:
                # Prefer mp4 formats with both video and audio
                if fmt.get("ext") == "mp4":
                    height = fmt.get("height", 0)
                    has_video = fmt.get("vcodec", "none") != "none"
                    has_audio = fmt.get("acodec", "none") != "none"
                    
                    if has_video and has_audio and height > best_quality:
                        best_quality = height
                        best_format = fmt
            
            # If no combined format, get best video
            if not best_format:
                for fmt in formats:
                    if fmt.get("vcodec", "none") != "none":
                        height = fmt.get("height", 0)
                        if height > best_quality:
                            best_quality = height
                            best_format = fmt
            
            if best_format:
                download_url = best_format.get("url")
                estimated_size = best_format.get("filesize") or best_format.get("filesize_approx") or 0
        
        if not download_url:
            return False, None, "Could not find download link for this video"
        
        if progress_callback:
            progress_callback("Ready to download!")
        
        return True, {
            "title": title,
            "duration": duration,
            "thumbnail": thumbnail,
            "uploader": uploader,
            "size": estimated_size,
            "download_url": download_url
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
            border-radius: 10px !important;
            padding: 1rem 2rem !important;
            font-weight: 700 !important;
            font-size: 1.1rem !important;
            width: 100% !important;
        }
        
        .stDownloadButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 10px 30px rgba(0, 200, 83, 0.3) !important;
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
        
        .highlight {
            background: rgba(255, 0, 0, 0.1);
            padding: 0.2rem 0.6rem;
            border-radius: 6px;
            color: #FF6B6B;
            font-weight: 600;
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
            <h3 style="margin-top: 0;">How to use:</h3>
            <p class="big-text">
                1️⃣ Copy the video URL from YouTube or TikTok<br>
                2️⃣ Paste it in the box below<br>
                3️⃣ Click "Download Video"<br>
                4️⃣ Wait a few seconds and your video will download!
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
        with st.spinner("🔍 Getting video information..."):
            progress_placeholder = st.empty()
            
            def update_progress(msg):
                progress_placeholder.info(msg)
            
            success, video_info, error = get_video_info_and_file(
                url_input, 
                platform_name,
                progress_callback=update_progress
            )
            
            progress_placeholder.empty()
        
        if not success:
            st.error(f"❌ Couldn't download this video. Error: {error}")
            st.info("💡 Tip: Make sure the video is public and not age-restricted")
            return
        
        # Show video info
        st.markdown(f"""
            <div class="video-card">
                <h2 style="margin-top: 0; font-size: 1.5rem;">✅ {video_info['title']}</h2>
                <p style="color: #888; margin: 0.5rem 0;">
                    👤 {video_info['uploader']} • 
                    ⏱️ {format_duration(video_info['duration'])} • 
                    💾 {format_size(video_info['size'])}
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        # Show thumbnail
        if video_info.get('thumbnail'):
            st.image(video_info['thumbnail'], use_container_width=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Download button
        if video_info.get('download_url'):
            st.markdown(f"""
                <a href="{video_info['download_url']}" download="{video_info['title']}.mp4" target="_blank">
                    <button style="
                        background: linear-gradient(135deg, #00C853, #00E676);
                        color: white;
                        border: none;
                        border-radius: 10px;
                        padding: 1rem 2rem;
                        font-weight: 700;
                        font-size: 1.1rem;
                        width: 100%;
                        cursor: pointer;
                        transition: all 0.3s;
                    ">
                        ⬇️ CLICK HERE TO DOWNLOAD
                    </button>
                </a>
            """, unsafe_allow_html=True)
            
            st.success("✅ Click the green button above to download your video!")
        else:
            st.error("❌ Couldn't generate download link. Please try again.")
    
    # Help section
    with st.expander("ℹ️ Need Help?"):
        st.markdown("""
            **Common Issues:**
            
            • **Video won't download?**  
              → Make sure the video is public and not age-restricted
            
            • **Download button doesn't work?**  
              → Right-click the button and select "Save link as..."
            
            • **Video is too large?**  
              → Large videos (>100MB) will open in a new tab for download
            
            • **Still having problems?**  
              → Try a different video or check your internet connection
        """)

def main():
    """Main app"""
    apply_styles()
    
    # Create tabs
    tab1, tab2 = st.tabs(["🎥 YouTube", "🎵 TikTok"])
    
    with tab1:
        render_tab("youtube", "🎥", "YouTube Downloader")
    
    with tab2:
        render_tab("tiktok", "🎵", "TikTok Downloader")
    
    # Footer
    st.markdown("""
        <div style="text-align: center; padding: 2rem 0; color: #666; margin-top: 3rem; border-top: 1px solid rgba(255,255,255,0.1);">
            Video Downloader Pro • Simple & Easy<br>
            For personal use only
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Error: {e}")
        st.error("Something went wrong. Please refresh the page.")