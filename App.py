#!/usr/bin/env python3
"""
Video Downloader Pro - Advanced UI with Fixes
Downloads videos directly - No complicated steps!
Version: 4.0.0
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
    """Format bytes to readable size - FIXED"""
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
    """Format seconds to MM:SS - FIXED"""
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
        
        # Create temp directory
        temp_dir = tempfile.mkdtemp()
        
        # Progress hook
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
            view_count = info.get("view_count", 0)
            upload_date = info.get("upload_date", "")
            
            # Get estimated file size
            formats = info.get("formats", [])
            estimated_size = 0
            for fmt in formats:
                size = fmt.get("filesize") or fmt.get("filesize_approx", 0)
                if size and size > estimated_size:
                    estimated_size = size
        
        if progress_callback:
            progress_callback(f"⬇️ Downloading: {title[:50]}...", 20)
        
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
            progress_callback("📦 Preparing download...", 98)
        
        with open(video_file, 'rb') as f:
            video_data = f.read()
        
        # Clean up
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
            "filename": f"{title[:100]}.mp4",
            "view_count": view_count,
            "upload_date": upload_date
        }, None
        
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Error: {error_msg}")
        return False, None, error_msg

def apply_styles():
    """Apply advanced modern styles"""
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@400;500;600;700&display=swap');
        
        * {
            font-family: 'Inter', sans-serif;
        }
        
        h1, h2, h3 {
            font-family: 'Space Grotesk', sans-serif !important;
        }
        
        .stApp {
            background: #0a0a0a;
            background-image: 
                radial-gradient(at 0% 0%, rgba(255, 0, 0, 0.1) 0px, transparent 50%),
                radial-gradient(at 100% 0%, rgba(0, 150, 255, 0.08) 0px, transparent 50%),
                radial-gradient(at 100% 100%, rgba(255, 0, 100, 0.08) 0px, transparent 50%);
            color: #ffffff;
        }
        
        #MainMenu, footer, header {visibility: hidden;}
        .stDeployButton {display: none;}
        
        .block-container {
            padding: 1.5rem 2rem !important;
            max-width: 1200px !important;
        }
        
        /* Animated gradient border tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 1rem;
            background: transparent;
            justify-content: center;
            border-bottom: none;
            padding-bottom: 1.5rem;
            margin-bottom: 2rem;
        }
        
        .stTabs [data-baseweb="tab"] {
            background: rgba(255, 255, 255, 0.03);
            border: 2px solid rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            padding: 1rem 2.5rem;
            font-weight: 600;
            font-size: 1.1rem;
            color: #666;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }
        
        .stTabs [data-baseweb="tab"]::before {
            content: '';
            position: absolute;
            inset: 0;
            border-radius: 16px;
            padding: 2px;
            background: linear-gradient(135deg, #FF0000, #FF6B6B, #00C853);
            -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
            -webkit-mask-composite: xor;
            mask-composite: exclude;
            opacity: 0;
            transition: opacity 0.4s;
        }
        
        .stTabs [data-baseweb="tab"][aria-selected="true"] {
            background: linear-gradient(135deg, rgba(255, 0, 0, 0.15), rgba(204, 0, 0, 0.1));
            color: white;
            border-color: rgba(255, 0, 0, 0.5);
            box-shadow: 0 8px 32px rgba(255, 0, 0, 0.25), 0 0 0 1px rgba(255, 0, 0, 0.1) inset;
            transform: translateY(-2px);
        }
        
        .stTabs [data-baseweb="tab"][aria-selected="true"]::before {
            opacity: 1;
        }
        
        /* Hero Header with glassmorphism */
        .hero-header {
            text-align: center;
            padding: 3rem 2rem;
            margin-bottom: 2rem;
            background: rgba(255, 255, 255, 0.02);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 24px;
            position: relative;
            overflow: hidden;
        }
        
        .hero-header::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(45deg, transparent, rgba(255, 0, 0, 0.05), transparent);
            animation: scan 8s linear infinite;
        }
        
        @keyframes scan {
            0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
            100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
        }
        
        .main-title {
            font-size: 3.5rem;
            font-weight: 900;
            background: linear-gradient(135deg, #FF0000, #FF6B6B, #FF0050);
            background-size: 200% 200%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.8rem;
            animation: gradientShift 3s ease infinite;
            position: relative;
            z-index: 1;
        }
        
        @keyframes gradientShift {
            0%, 100% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
        }
        
        .subtitle {
            font-size: 1.3rem;
            color: #999;
            position: relative;
            z-index: 1;
        }
        
        .platform-badge {
            display: inline-block;
            padding: 0.5rem 1.2rem;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.15);
            border-radius: 50px;
            font-size: 0.9rem;
            margin: 0.3rem;
            font-weight: 600;
        }
        
        /* Advanced cards with hover effects */
        .glass-card {
            background: rgba(255, 255, 255, 0.03);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 2rem;
            margin: 1.5rem 0;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        .glass-card:hover {
            background: rgba(255, 255, 255, 0.05);
            border-color: rgba(255, 255, 255, 0.2);
            transform: translateY(-4px);
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4);
        }
        
        .video-result-card {
            background: linear-gradient(135deg, rgba(255, 0, 0, 0.08), rgba(255, 107, 107, 0.05));
            border: 2px solid rgba(255, 0, 0, 0.3);
            border-radius: 20px;
            padding: 2rem;
            margin: 1.5rem 0;
            position: relative;
            overflow: hidden;
        }
        
        .video-result-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
            animation: shimmer 2s infinite;
        }
        
        @keyframes shimmer {
            0% { left: -100%; }
            100% { left: 100%; }
        }
        
        /* Premium input styling */
        .stTextInput > div > div > input {
            background: rgba(255, 255, 255, 0.04) !important;
            border: 2px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 16px !important;
            padding: 1.5rem !important;
            color: #fff !important;
            font-size: 1.05rem !important;
            transition: all 0.3s !important;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #FF0000 !important;
            background: rgba(255, 0, 0, 0.05) !important;
            box-shadow: 0 0 0 4px rgba(255, 0, 0, 0.1), 0 8px 32px rgba(255, 0, 0, 0.2) !important;
            transform: translateY(-2px) !important;
        }
        
        .stTextInput > div > div > input::placeholder {
            color: #666 !important;
        }
        
        /* Premium buttons with 3D effect */
        .stButton > button {
            background: linear-gradient(135deg, #FF0000, #CC0000) !important;
            color: white !important;
            border: none !important;
            border-radius: 14px !important;
            padding: 1rem 2.5rem !important;
            font-weight: 700 !important;
            font-size: 1.1rem !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            box-shadow: 0 8px 24px rgba(255, 0, 0, 0.3), 0 4px 8px rgba(0, 0, 0, 0.2) !important;
            position: relative !important;
        }
        
        .stButton > button:hover {
            transform: translateY(-3px) !important;
            box-shadow: 0 12px 36px rgba(255, 0, 0, 0.4), 0 6px 12px rgba(0, 0, 0, 0.3) !important;
        }
        
        .stButton > button:active {
            transform: translateY(-1px) !important;
        }
        
        .stDownloadButton > button {
            background: linear-gradient(135deg, #00C853, #00E676) !important;
            color: white !important;
            border: none !important;
            border-radius: 16px !important;
            padding: 1.5rem 3rem !important;
            font-weight: 800 !important;
            font-size: 1.3rem !important;
            width: 100% !important;
            box-shadow: 0 12px 40px rgba(0,200,83,0.4), 0 0 60px rgba(0,200,83,0.1) !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            animation: pulse 2s infinite !important;
        }
        
        @keyframes pulse {
            0%, 100% { box-shadow: 0 12px 40px rgba(0,200,83,0.4), 0 0 60px rgba(0,200,83,0.1); }
            50% { box-shadow: 0 12px 50px rgba(0,200,83,0.6), 0 0 80px rgba(0,200,83,0.2); }
        }
        
        .stDownloadButton > button:hover {
            transform: translateY(-4px) scale(1.02) !important;
            box-shadow: 0 16px 60px rgba(0,200,83,0.5), 0 0 100px rgba(0,200,83,0.2) !important;
        }
        
        /* Progress bar */
        .stProgress > div > div > div {
            background: linear-gradient(90deg, #FF0000, #FF6B6B) !important;
            border-radius: 10px !important;
        }
        
        /* Stats badges */
        .stat-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.6rem 1.2rem;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            margin: 0.3rem;
            font-size: 0.95rem;
            font-weight: 500;
        }
        
        /* Feature grid */
        .feature-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1.5rem;
            margin: 2rem 0;
        }
        
        .feature-card {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            padding: 1.5rem;
            transition: all 0.3s;
        }
        
        .feature-card:hover {
            background: rgba(255, 255, 255, 0.05);
            transform: translateY(-4px);
            border-color: rgba(255, 0, 0, 0.3);
        }
        
        .feature-icon {
            font-size: 2.5rem;
            margin-bottom: 1rem;
        }
        
        h2, h3 {
            color: #FF0000 !important;
            font-weight: 700 !important;
        }
        
        .big-text {
            font-size: 1.1rem;
            line-height: 1.8;
            color: #bbb;
        }
        
        /* Alert/Info boxes */
        .stAlert {
            background: rgba(255, 255, 255, 0.05) !important;
            border-radius: 12px !important;
            border-left: 4px solid !important;
        }
        
        /* Thumbnail styling */
        .stImage {
            border-radius: 16px !important;
            overflow: hidden !important;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3) !important;
        }
        
        /* Expander */
        .streamlit-expanderHeader {
            background: rgba(255, 255, 255, 0.03) !important;
            border-radius: 12px !important;
            font-weight: 600 !important;
        }
        </style>
    """, unsafe_allow_html=True)

def render_hero():
    """Render hero section"""
    st.markdown("""
        <div class="hero-header">
            <h1 class="main-title">🎬 Video Downloader Pro</h1>
            <p class="subtitle">Download HD videos in seconds • Fast • Simple • Free</p>
            <div style="margin-top: 1.5rem;">
                <span class="platform-badge">🎥 YouTube</span>
                <span class="platform-badge">🎵 TikTok</span>
                <span class="platform-badge">⚡ Super Fast</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

def render_features():
    """Render features section"""
    st.markdown("""
        <div class="feature-grid">
            <div class="feature-card">
                <div class="feature-icon">⚡</div>
                <h3 style="margin: 0 0 0.5rem 0; font-size: 1.2rem;">Lightning Fast</h3>
                <p style="color: #888; margin: 0;">Download videos in seconds with optimized speed</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🎯</div>
                <h3 style="margin: 0 0 0.5rem 0; font-size: 1.2rem;">High Quality</h3>
                <p style="color: #888; margin: 0;">Get the best quality available for your videos</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🔒</div>
                <h3 style="margin: 0 0 0.5rem 0; font-size: 1.2rem;">Safe & Secure</h3>
                <p style="color: #888; margin: 0;">Your privacy is our priority, no data stored</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

def render_tab(platform_name, platform_icon, platform_title):
    """Render download tab with advanced UI"""
    
    # Simple instructions
    st.markdown("""
        <div class="glass-card">
            <h3 style="margin-top: 0;">📋 How to Download:</h3>
            <p class="big-text">
                <strong>1️⃣</strong> Copy the video URL from YouTube or TikTok<br>
                <strong>2️⃣</strong> Paste it in the input field below<br>
                <strong>3️⃣</strong> Click the "Download Video" button<br>
                <strong>4️⃣</strong> Wait for processing and download your video!
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # URL Input
    url_input = st.text_input(
        "Video URL",
        placeholder=f"🔗 Paste your {platform_title.split()[0]} video URL here...",
        key=f"{platform_name}_url",
        label_visibility="collapsed"
    )
    
    # Download button
    if st.button(f"{platform_icon} Download Video", type="primary", use_container_width=True, key=f"{platform_name}_download"):
        if not url_input.strip():
            st.error("❌ Please paste a video URL first!")
            return
        
        # Validate URL
        is_valid, message = validate_url(url_input, platform_name)
        if not is_valid:
            st.error(f"❌ {message}")
            return
        
        # Show progress
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
            st.error(f"❌ Couldn't download this video")
            with st.expander("🔍 Error Details"):
                st.code(error)
            st.info("💡 **Tips:**\n- Make sure the video is public and not age-restricted\n- Check if the URL is correct\n- Try a different video or refresh the page")
            return
        
        download_time = time.time() - start_time
        
        # Show success with video info
        st.markdown(f"""
            <div class="video-result-card">
                <h2 style="margin-top: 0; font-size: 1.8rem;">✅ {video_data['title']}</h2>
                <div style="margin: 1rem 0;">
                    <span class="stat-badge">👤 {video_data['uploader']}</span>
                    <span class="stat-badge">⏱️ {format_duration(video_data['duration'])}</span>
                    <span class="stat-badge">💾 {format_size(video_data['size'])}</span>
                    <span class="stat-badge">⚡ {download_time:.1f}s</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Show thumbnail
        if video_data.get('thumbnail'):
            st.image(video_data['thumbnail'], use_container_width=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Create download button
        st.success("🎉 Your video is ready! Click below to download:")
        
        st.download_button(
            label="⬇️ DOWNLOAD VIDEO NOW",
            data=video_data['data'],
            file_name=video_data['filename'],
            mime="video/mp4",
            use_container_width=True
        )
        
        st.balloons()
        
        # Additional info
        st.info("💡 **Tip:** The download will start automatically. Check your Downloads folder!")
    
    # Help section
    with st.expander("ℹ️ Need Help?"):
        st.markdown("""
            ### 🆘 Common Issues & Solutions
            
            **Download takes too long?**  
            → Large videos need more time. Please be patient or try a shorter video.
            
            **Video won't download?**  
            → Ensure the video is public, not age-restricted, and not a live stream.
            
            **Error message appears?**  
            → Try a different video, check your internet, or refresh the page.
            
            **Downloaded file won't play?**  
            → Use VLC Media Player or update your default video player.
            
            **Low quality video?**  
            → We download the best available quality. Source quality matters!
        """)

def main():
    """Main app"""
    apply_styles()
    
    # Hero section
    render_hero()
    
    # Warning about limitations
    st.info("ℹ️ **Note:** This app works best locally. On Streamlit Cloud, large videos may timeout due to platform limitations.")
    
    # Features
    render_features()
    
    # Create tabs
    tab1, tab2 = st.tabs(["🎥 YouTube", "🎵 TikTok"])
    
    with tab1:
        render_tab("youtube", "🎥", "YouTube Downloader")
    
    with tab2:
        render_tab("tiktok", "🎵", "TikTok Downloader")
    
    # Footer
    st.markdown("""
        <div style="text-align: center; padding: 3rem 0; color: #666; margin-top: 4rem; border-top: 1px solid rgba(255,255,255,0.1);">
            <p style="font-size: 1.1rem; margin-bottom: 0.5rem;">Video Downloader Pro v4.0</p>
            <p style="font-size: 0.9rem; color: #555;">Advanced UI • Lightning Fast • Free Forever</p>
            <p style="font-size: 0.85rem; color: #444; margin-top: 1rem;">For personal use only • Respect copyright laws</p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Error: {e}")
        st.error("⚠️ Something went wrong. Please refresh the page and try again.")
        with st.expander("🔍 Technical Details"):
            st.code(str(e))