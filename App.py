#!/usr/bin/env python3
"""
Video Downloader Pro - Beautiful & Fast
Downloads videos directly - Stunning Design!
Version: 5.0.1
"""

import streamlit as st
import yt_dlp
from fake_useragent import UserAgent
import tempfile
import os
import logging
import time

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
    if not bytes_size or bytes_size == 0:
        return "Unknown"
    try:
        bytes_size = float(bytes_size)
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes_size < 1024.0:
                return f"{bytes_size:.1f} {unit}"
            bytes_size /= 1024.0
        return f"{bytes_size:.1f} TB"
    except:
        return "Unknown"

def format_duration(seconds):
    """Format seconds to MM:SS"""
    if not seconds:
        return "Unknown"
    try:
        seconds = int(float(seconds))
        minutes = seconds // 60
        secs = seconds % 60
        return f"{int(minutes)}:{int(secs):02d}"
    except:
        return "Unknown"

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
            progress_callback("🔍 Getting video information...", 10)
        
        temp_dir = tempfile.mkdtemp()
        last_progress = [0]
        
        def progress_hook(d):
            if d['status'] == 'downloading' and progress_callback:
                try:
                    percent_str = d.get('_percent_str', '0%').strip().replace('%', '')
                    percent = int(float(percent_str))
                    if percent != last_progress[0]:
                        progress_callback(f"⬇️ Downloading: {percent}%", min(percent, 90))
                        last_progress[0] = percent
                except:
                    pass
            elif d['status'] == 'finished' and progress_callback:
                progress_callback("✅ Processing video...", 95)
        
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
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            title = info.get("title", "video")
            duration = info.get("duration", 0)
            thumbnail = info.get("thumbnail")
            uploader = info.get("uploader", "Unknown")
            
            formats = info.get("formats", [])
            estimated_size = 0
            for fmt in formats:
                size = fmt.get("filesize") or fmt.get("filesize_approx", 0)
                if size and size > estimated_size:
                    estimated_size = size
        
        if progress_callback:
            progress_callback(f"⬇️ Downloading: {title[:50]}...", 20)
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        video_file = None
        for file in os.listdir(temp_dir):
            if file.startswith("video."):
                video_file = os.path.join(temp_dir, file)
                break
        
        if not video_file or not os.path.exists(video_file):
            return False, None, "Download failed - file not found"
        
        if progress_callback:
            progress_callback("📦 Preparing download...", 98)
        
        with open(video_file, 'rb') as f:
            video_data = f.read()
        
        try:
            os.remove(video_file)
            os.rmdir(temp_dir)
        except:
            pass
        
        if progress_callback:
            progress_callback("✅ Complete!", 100)
        
        return True, {
            "title": title,
            "duration": duration,
            "thumbnail": thumbnail,
            "uploader": uploader,
            "size": len(video_data),
            "data": video_data,
            "filename": f"{title[:100]}.mp4"
        }, None
        
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Error: {error_msg}")
        return False, None, error_msg

def apply_styles():
    """Apply beautiful optimized styles"""
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800;900&display=swap');
        
        * {
            font-family: 'Poppins', sans-serif;
        }
        
        .stApp {
            background: linear-gradient(135deg, #0a0012 0%, #1a0520 50%, #0a0a1f 100%);
            color: #ffffff;
        }
        
        #MainMenu, footer, header {visibility: hidden;}
        .stDeployButton {display: none;}
        
        .block-container {
            padding: 2rem !important;
            max-width: 1200px !important;
        }
        
        /* Hero Section */
        .hero-box {
            text-align: center;
            padding: 4rem 2rem;
            margin: 2rem 0;
            background: linear-gradient(135deg, rgba(255, 0, 100, 0.1), rgba(138, 43, 226, 0.1));
            border: 2px solid rgba(255, 0, 100, 0.3);
            border-radius: 30px;
            box-shadow: 0 20px 60px rgba(255, 0, 100, 0.3);
        }
        
        .hero-title {
            font-size: 3.5rem;
            font-weight: 900;
            background: linear-gradient(135deg, #ff0064, #ff6b9d, #8a2be2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 1rem;
        }
        
        .hero-subtitle {
            font-size: 1.4rem;
            color: rgba(255, 255, 255, 0.7);
            margin-bottom: 1.5rem;
        }
        
        .badge {
            display: inline-block;
            padding: 0.7rem 1.5rem;
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 50px;
            margin: 0.3rem;
            font-weight: 600;
        }
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 1.5rem;
            background: transparent;
            justify-content: center;
            border-bottom: 2px solid rgba(255, 255, 255, 0.1);
            padding-bottom: 1rem;
            margin: 2rem 0;
        }
        
        .stTabs [data-baseweb="tab"] {
            background: rgba(255, 255, 255, 0.05);
            border: 2px solid rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 1rem 2.5rem;
            font-weight: 700;
            font-size: 1.2rem;
            color: #888;
            transition: all 0.3s;
        }
        
        .stTabs [data-baseweb="tab"][aria-selected="true"] {
            background: linear-gradient(135deg, rgba(255, 0, 100, 0.2), rgba(138, 43, 226, 0.2));
            color: white;
            border-color: rgba(255, 0, 100, 0.5);
            box-shadow: 0 10px 40px rgba(255, 0, 100, 0.4);
        }
        
        /* Cards */
        .glass-card {
            background: rgba(255, 255, 255, 0.05);
            border: 2px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 2rem;
            margin: 1.5rem 0;
        }
        
        .feature-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1.5rem;
            margin: 2rem 0;
        }
        
        .feature-card {
            background: rgba(255, 255, 255, 0.05);
            border: 2px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 2rem;
            text-align: center;
            transition: all 0.3s;
        }
        
        .feature-card:hover {
            background: rgba(255, 0, 100, 0.1);
            border-color: rgba(255, 0, 100, 0.4);
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(255, 0, 100, 0.3);
        }
        
        .feature-icon {
            font-size: 3rem;
            margin-bottom: 1rem;
        }
        
        /* Input */
        .stTextInput > div > div > input {
            background: rgba(255, 255, 255, 0.05) !important;
            border: 2px solid rgba(255, 255, 255, 0.2) !important;
            border-radius: 15px !important;
            padding: 1.5rem !important;
            color: #fff !important;
            font-size: 1.1rem !important;
            transition: all 0.3s !important;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #ff0064 !important;
            background: rgba(255, 0, 100, 0.05) !important;
            box-shadow: 0 0 0 4px rgba(255, 0, 100, 0.2) !important;
        }
        
        /* Buttons */
        .stButton > button {
            background: linear-gradient(135deg, #ff0064, #8a2be2) !important;
            color: white !important;
            border: none !important;
            border-radius: 15px !important;
            padding: 1.5rem 2.5rem !important;
            font-weight: 700 !important;
            font-size: 1.2rem !important;
            transition: all 0.3s !important;
            box-shadow: 0 10px 30px rgba(255, 0, 100, 0.4) !important;
        }
        
        .stButton > button:hover {
            transform: translateY(-3px) !important;
            box-shadow: 0 15px 40px rgba(255, 0, 100, 0.5) !important;
        }
        
        .stDownloadButton > button {
            background: linear-gradient(135deg, #00ff88, #00ffff) !important;
            color: #000 !important;
            border: none !important;
            border-radius: 15px !important;
            padding: 1.8rem 3rem !important;
            font-weight: 800 !important;
            font-size: 1.4rem !important;
            width: 100% !important;
            box-shadow: 0 15px 50px rgba(0, 255, 136, 0.5) !important;
            transition: all 0.3s !important;
        }
        
        .stDownloadButton > button:hover {
            transform: translateY(-4px) !important;
            box-shadow: 0 20px 60px rgba(0, 255, 136, 0.6) !important;
        }
        
        /* Progress Bar */
        .stProgress > div > div > div {
            background: linear-gradient(90deg, #ff0064, #8a2be2, #0096ff) !important;
            border-radius: 10px !important;
        }
        
        /* Result Card */
        .result-card {
            background: linear-gradient(135deg, rgba(255, 0, 100, 0.15), rgba(138, 43, 226, 0.1));
            border: 2px solid rgba(255, 0, 100, 0.4);
            border-radius: 20px;
            padding: 2rem;
            margin: 1.5rem 0;
        }
        
        .stat-badge {
            display: inline-block;
            padding: 0.8rem 1.5rem;
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 50px;
            margin: 0.3rem;
            font-weight: 600;
        }
        
        /* Image */
        .stImage {
            border-radius: 20px !important;
            box-shadow: 0 15px 50px rgba(0, 0, 0, 0.4) !important;
            border: 2px solid rgba(255, 0, 100, 0.3) !important;
        }
        
        h2, h3 {
            color: #ff0064 !important;
            font-weight: 700 !important;
        }
        
        .big-text {
            font-size: 1.1rem;
            line-height: 1.8;
            color: rgba(255, 255, 255, 0.8);
        }
        </style>
    """, unsafe_allow_html=True)

def main():
    """Main application"""
    apply_styles()
    
    # Hero Section
    st.markdown("""
        <div class="hero-box">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🎬</div>
            <h1 class="hero-title">Video Downloader Pro</h1>
            <p class="hero-subtitle">✨ Download HD Videos in Seconds ✨</p>
            <div>
                <span class="badge">🎥 YouTube</span>
                <span class="badge">🎵 TikTok</span>
                <span class="badge">⚡ Super Fast</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Info
    st.info("ℹ️ **Note:** This app works best locally. Streamlit Cloud may have file size limitations.")
    
    # Features
    st.markdown("""
        <div class="feature-grid">
            <div class="feature-card">
                <div class="feature-icon">⚡</div>
                <h3 style="margin: 0 0 0.5rem 0;">Lightning Fast</h3>
                <p style="color: rgba(255, 255, 255, 0.7); margin: 0;">Download videos in seconds</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🎯</div>
                <h3 style="margin: 0 0 0.5rem 0;">HD Quality</h3>
                <p style="color: rgba(255, 255, 255, 0.7); margin: 0;">Best quality available</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🔒</div>
                <h3 style="margin: 0 0 0.5rem 0;">100% Secure</h3>
                <p style="color: rgba(255, 255, 255, 0.7); margin: 0;">No data stored</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Tabs
    tab1, tab2 = st.tabs(["🎥 YouTube", "🎵 TikTok"])
    
    with tab1:
        render_tab("youtube", "🎥", "YouTube")
    
    with tab2:
        render_tab("tiktok", "🎵", "TikTok")
    
    # Footer
    st.markdown("""
        <div style="text-align: center; padding: 3rem 0; color: #666; margin-top: 3rem; border-top: 1px solid rgba(255,255,255,0.1);">
            <p style="font-size: 1.2rem; font-weight: 600; color: #ff0064;">Video Downloader Pro v5.0</p>
            <p style="font-size: 0.9rem; margin-top: 0.5rem;">Beautiful UI • Fast Downloads • Free Forever</p>
            <p style="font-size: 0.85rem; margin-top: 1rem; color: #555;">For personal use only</p>
        </div>
    """, unsafe_allow_html=True)

def render_tab(platform_name, platform_icon, platform_title):
    """Render download tab"""
    
    st.markdown("""
        <div class="glass-card">
            <h3 style="margin-top: 0;">📋 How to Download:</h3>
            <p class="big-text">
                <strong>1️⃣</strong> Copy the video URL from YouTube or TikTok<br>
                <strong>2️⃣</strong> Paste it in the field below<br>
                <strong>3️⃣</strong> Click "Download Video"<br>
                <strong>4️⃣</strong> Wait and download your video!
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    url_input = st.text_input(
        "Video URL",
        placeholder=f"✨ Paste your {platform_title} video URL here...",
        key=f"{platform_name}_url",
        label_visibility="collapsed"
    )
    
    if st.button(f"{platform_icon} Download Video", type="primary", use_container_width=True, key=f"{platform_name}_download"):
        if not url_input.strip():
            st.error("❌ Please paste a video URL first!")
            return
        
        is_valid, message = validate_url(url_input, platform_name)
        if not is_valid:
            st.error(f"❌ {message}")
            return
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        def update_progress(msg, percent):
            status_text.info(msg)
            progress_bar.progress(percent / 100)
        
        start_time = time.time()
        
        success, video_data, error = download_video(
            url_input, 
            platform_name,
            progress_callback=update_progress
        )
        
        progress_bar.empty()
        status_text.empty()
        
        if not success:
            st.error(f"❌ Unable to download this video")
            with st.expander("🔍 Error Details"):
                st.code(error)
            st.info("💡 **Tips:**\n- Make sure the video is public\n- Check if the URL is correct\n- Try a different video")
            return
        
        download_time = time.time() - start_time
        
        st.markdown(f"""
            <div class="result-card">
                <h2 style="margin-top: 0;">✅ {video_data['title']}</h2>
                <div style="margin: 1rem 0;">
                    <span class="stat-badge">👤 {video_data['uploader']}</span>
                    <span class="stat-badge">⏱️ {format_duration(video_data['duration'])}</span>
                    <span class="stat-badge">💾 {format_size(video_data['size'])}</span>
                    <span class="stat-badge">⚡ {download_time:.1f}s</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        if video_data.get('thumbnail'):
            st.image(video_data['thumbnail'], use_container_width=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.success("🎉 Your video is ready!")
        
        st.download_button(
            label="⬇️ DOWNLOAD VIDEO NOW",
            data=video_data['data'],
            file_name=video_data['filename'],
            mime="video/mp4",
            use_container_width=True
        )
        
        st.balloons()
    
    with st.expander("ℹ️ Need Help?"):
        st.markdown("""
            **Common Issues:**
            
            • **Download takes long?** → Large videos need time
            • **Video won't download?** → Check if it's public and not restricted
            • **Error appears?** → Try different video or refresh
            • **File won't play?** → Use VLC Media Player
        """)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Error: {e}")
        st.error("⚠️ Something went wrong. Please refresh the page!")
        with st.expander("🔍 Technical Details"):
            st.code(str(e))