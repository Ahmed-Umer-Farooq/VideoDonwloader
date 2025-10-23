#!/usr/bin/env python3
"""
Video Downloader Pro - The Most Beautiful UI Ever
Downloads videos directly - Stunning Design!
Version: 5.0.0 - Ultimate Edition
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
            view_count = info.get("view_count", 0)
            
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
            "filename": f"{title[:100]}.mp4",
            "view_count": view_count
        }, None
        
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Error: {error_msg}")
        return False, None, error_msg

def apply_styles():
    """Apply the most beautiful styles ever created"""
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&family=Orbitron:wght@400;500;600;700;800;900&display=swap');
        
        * {
            font-family: 'Poppins', sans-serif;
        }
        
        /* Stunning animated background */
        .stApp {
            background: #000000;
            position: relative;
            overflow-x: hidden;
        }
        
        .stApp::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: 
                radial-gradient(circle at 20% 50%, rgba(255, 0, 100, 0.15) 0%, transparent 50%),
                radial-gradient(circle at 80% 80%, rgba(138, 43, 226, 0.15) 0%, transparent 50%),
                radial-gradient(circle at 40% 20%, rgba(0, 150, 255, 0.12) 0%, transparent 50%),
                radial-gradient(circle at 60% 90%, rgba(255, 0, 50, 0.12) 0%, transparent 50%);
            animation: gradientMove 20s ease infinite;
            z-index: 0;
        }
        
        @keyframes gradientMove {
            0%, 100% { transform: scale(1) rotate(0deg); }
            33% { transform: scale(1.1) rotate(5deg); }
            66% { transform: scale(0.95) rotate(-5deg); }
        }
        
        /* Floating particles */
        .stApp::after {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-image: 
                radial-gradient(2px 2px at 20% 30%, rgba(255, 255, 255, 0.3), transparent),
                radial-gradient(2px 2px at 60% 70%, rgba(255, 255, 255, 0.3), transparent),
                radial-gradient(1px 1px at 50% 50%, rgba(255, 255, 255, 0.3), transparent),
                radial-gradient(1px 1px at 80% 10%, rgba(255, 255, 255, 0.3), transparent),
                radial-gradient(2px 2px at 90% 60%, rgba(255, 255, 255, 0.3), transparent),
                radial-gradient(1px 1px at 33% 80%, rgba(255, 255, 255, 0.3), transparent);
            background-size: 200% 200%;
            animation: particles 60s linear infinite;
            pointer-events: none;
            z-index: 0;
        }
        
        @keyframes particles {
            0% { background-position: 0% 0%; }
            100% { background-position: 100% 100%; }
        }
        
        .block-container {
            position: relative;
            z-index: 1;
            padding: 2rem 2rem !important;
            max-width: 1400px !important;
        }
        
        #MainMenu, footer, header {visibility: hidden;}
        .stDeployButton {display: none;}
        
        /* Epic Hero Section */
        .mega-hero {
            text-align: center;
            padding: 5rem 2rem;
            margin: 2rem 0 3rem 0;
            background: linear-gradient(135deg, rgba(255, 0, 100, 0.1), rgba(138, 43, 226, 0.1));
            backdrop-filter: blur(20px);
            border: 2px solid transparent;
            border-radius: 40px;
            position: relative;
            overflow: hidden;
            box-shadow: 
                0 0 80px rgba(255, 0, 100, 0.3),
                0 0 120px rgba(138, 43, 226, 0.2),
                inset 0 0 80px rgba(255, 255, 255, 0.02);
        }
        
        .mega-hero::before {
            content: '';
            position: absolute;
            inset: 0;
            border-radius: 40px;
            padding: 2px;
            background: linear-gradient(135deg, #ff0064, #8a2be2, #0096ff, #ff0032);
            background-size: 300% 300%;
            -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
            -webkit-mask-composite: xor;
            mask-composite: exclude;
            animation: borderFlow 4s linear infinite;
        }
        
        @keyframes borderFlow {
            0%, 100% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
        }
        
        .mega-hero::after {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(45deg, transparent, rgba(255, 255, 255, 0.03), transparent);
            animation: shine 3s linear infinite;
        }
        
        @keyframes shine {
            0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
            100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
        }
        
        .epic-title {
            font-family: 'Orbitron', sans-serif;
            font-size: 5rem;
            font-weight: 900;
            background: linear-gradient(135deg, #ff0064, #ff6b9d, #8a2be2, #0096ff);
            background-size: 200% 200%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 0 0 1rem 0;
            text-transform: uppercase;
            letter-spacing: 4px;
            animation: epicGradient 5s ease infinite;
            text-shadow: 0 0 80px rgba(255, 0, 100, 0.5);
            position: relative;
            z-index: 1;
        }
        
        @keyframes epicGradient {
            0%, 100% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
        }
        
        .epic-icon {
            font-size: 4rem;
            display: inline-block;
            animation: float 3s ease-in-out infinite;
            filter: drop-shadow(0 0 20px rgba(255, 0, 100, 0.6));
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0px) rotate(0deg); }
            50% { transform: translateY(-20px) rotate(5deg); }
        }
        
        .epic-subtitle {
            font-size: 1.8rem;
            color: rgba(255, 255, 255, 0.8);
            font-weight: 300;
            margin-bottom: 2rem;
            position: relative;
            z-index: 1;
        }
        
        .platform-badges {
            display: flex;
            justify-content: center;
            gap: 1.5rem;
            flex-wrap: wrap;
            position: relative;
            z-index: 1;
        }
        
        .epic-badge {
            padding: 1rem 2rem;
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05));
            backdrop-filter: blur(10px);
            border: 2px solid rgba(255, 255, 255, 0.2);
            border-radius: 50px;
            font-size: 1.2rem;
            font-weight: 600;
            color: #fff;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            cursor: default;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        }
        
        .epic-badge:hover {
            transform: translateY(-8px) scale(1.05);
            background: linear-gradient(135deg, rgba(255, 0, 100, 0.3), rgba(138, 43, 226, 0.3));
            border-color: rgba(255, 0, 100, 0.5);
            box-shadow: 0 20px 60px rgba(255, 0, 100, 0.4);
        }
        
        /* Futuristic Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 2rem;
            background: transparent;
            justify-content: center;
            border-bottom: none;
            padding: 0;
            margin: 3rem 0;
        }
        
        .stTabs [data-baseweb="tab"] {
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.05), rgba(255, 255, 255, 0.02));
            backdrop-filter: blur(10px);
            border: 2px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 1.5rem 3rem;
            font-weight: 700;
            font-size: 1.3rem;
            color: rgba(255, 255, 255, 0.5);
            transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }
        
        .stTabs [data-baseweb="tab"]::before {
            content: '';
            position: absolute;
            inset: 0;
            background: linear-gradient(135deg, #ff0064, #8a2be2);
            opacity: 0;
            transition: opacity 0.5s;
        }
        
        .stTabs [data-baseweb="tab"]::after {
            content: '';
            position: absolute;
            inset: 0;
            background: linear-gradient(45deg, transparent, rgba(255, 255, 255, 0.1), transparent);
            transform: translateX(-100%);
            transition: transform 0.6s;
        }
        
        .stTabs [data-baseweb="tab"][aria-selected="true"] {
            background: linear-gradient(135deg, rgba(255, 0, 100, 0.3), rgba(138, 43, 226, 0.2));
            color: #ffffff;
            border-color: rgba(255, 0, 100, 0.6);
            box-shadow: 
                0 0 60px rgba(255, 0, 100, 0.4),
                0 0 100px rgba(138, 43, 226, 0.3),
                inset 0 0 40px rgba(255, 255, 255, 0.1);
            transform: translateY(-4px) scale(1.05);
        }
        
        .stTabs [data-baseweb="tab"][aria-selected="true"]::before {
            opacity: 0.3;
        }
        
        .stTabs [data-baseweb="tab"][aria-selected="true"]::after {
            transform: translateX(100%);
        }
        
        /* Stunning Cards */
        .glass-card {
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.05), rgba(255, 255, 255, 0.02));
            backdrop-filter: blur(20px);
            border: 2px solid rgba(255, 255, 255, 0.1);
            border-radius: 30px;
            padding: 3rem;
            margin: 2rem 0;
            position: relative;
            overflow: hidden;
            transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        }
        
        .glass-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
            transition: left 0.7s;
        }
        
        .glass-card:hover {
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.08), rgba(255, 255, 255, 0.04));
            border-color: rgba(255, 0, 100, 0.4);
            transform: translateY(-8px);
            box-shadow: 
                0 30px 90px rgba(255, 0, 100, 0.3),
                0 0 100px rgba(138, 43, 226, 0.2);
        }
        
        .glass-card:hover::before {
            left: 100%;
        }
        
        /* Premium Input */
        .stTextInput > div > div > input {
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.08), rgba(255, 255, 255, 0.04)) !important;
            backdrop-filter: blur(10px) !important;
            border: 3px solid rgba(255, 255, 255, 0.2) !important;
            border-radius: 20px !important;
            padding: 2rem !important;
            color: #fff !important;
            font-size: 1.2rem !important;
            font-weight: 500 !important;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2) !important;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #ff0064 !important;
            background: linear-gradient(135deg, rgba(255, 0, 100, 0.1), rgba(138, 43, 226, 0.05)) !important;
            box-shadow: 
                0 0 0 6px rgba(255, 0, 100, 0.2),
                0 20px 60px rgba(255, 0, 100, 0.4),
                0 0 100px rgba(138, 43, 226, 0.3) !important;
            transform: translateY(-4px) !important;
        }
        
        .stTextInput > div > div > input::placeholder {
            color: rgba(255, 255, 255, 0.4) !important;
        }
        
        /* Epic Buttons */
        .stButton > button {
            background: linear-gradient(135deg, #ff0064, #8a2be2) !important;
            background-size: 200% 200% !important;
            color: white !important;
            border: none !important;
            border-radius: 20px !important;
            padding: 1.8rem 3rem !important;
            font-weight: 800 !important;
            font-size: 1.4rem !important;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
            box-shadow: 
                0 15px 50px rgba(255, 0, 100, 0.5),
                0 0 80px rgba(138, 43, 226, 0.3),
                inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
            position: relative !important;
            overflow: hidden !important;
            animation: buttonPulse 3s ease infinite !important;
        }
        
        @keyframes buttonPulse {
            0%, 100% { 
                background-position: 0% 50%;
                box-shadow: 
                    0 15px 50px rgba(255, 0, 100, 0.5),
                    0 0 80px rgba(138, 43, 226, 0.3);
            }
            50% { 
                background-position: 100% 50%;
                box-shadow: 
                    0 20px 70px rgba(255, 0, 100, 0.7),
                    0 0 120px rgba(138, 43, 226, 0.5);
            }
        }
        
        .stButton > button::before {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 0;
            height: 0;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.3);
            transform: translate(-50%, -50%);
            transition: width 0.6s, height 0.6s;
        }
        
        .stButton > button:hover {
            transform: translateY(-6px) scale(1.05) !important;
            box-shadow: 
                0 25px 80px rgba(255, 0, 100, 0.7),
                0 0 150px rgba(138, 43, 226, 0.5),
                inset 0 1px 0 rgba(255, 255, 255, 0.3) !important;
        }
        
        .stButton > button:hover::before {
            width: 300px;
            height: 300px;
        }
        
        .stButton > button:active {
            transform: translateY(-2px) scale(1.02) !important;
        }
        
        /* Legendary Download Button */
        .stDownloadButton > button {
            background: linear-gradient(135deg, #00ff88, #00ffff, #0096ff) !important;
            background-size: 200% 200% !important;
            color: #000 !important;
            border: none !important;
            border-radius: 25px !important;
            padding: 2.5rem 4rem !important;
            font-weight: 900 !important;
            font-size: 1.8rem !important;
            width: 100% !important;
            box-shadow: 
                0 20px 80px rgba(0, 255, 136, 0.6),
                0 0 120px rgba(0, 255, 255, 0.4),
                inset 0 2px 0 rgba(255, 255, 255, 0.5) !important;
            transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1) !important;
            animation: downloadPulse 2s ease infinite !important;
            position: relative !important;
            overflow: hidden !important;
        }
        
        @keyframes downloadPulse {
            0%, 100% { 
                background-position: 0% 50%;
                box-shadow: 
                    0 20px 80px rgba(0, 255, 136, 0.6),
                    0 0 120px rgba(0, 255, 255, 0.4);
            }
            50% { 
                background-position: 100% 50%;
                box-shadow: 
                    0 30px 120px rgba(0, 255, 136, 0.8),
                    0 0 180px rgba(0, 255, 255, 0.6);
            }
        }
        
        .stDownloadButton > button::after {
            content: '⚡';
            position: absolute;
            top: 50%;
            right: -50px;
            transform: translateY(-50%);
            font-size: 3rem;
            animation: lightning 2s ease infinite;
        }
        
        @keyframes lightning {
            0%, 100% { right: -50px; opacity: 0; }
            50% { right: 20px; opacity: 1; }
        }
        
        .stDownloadButton > button:hover {
            transform: translateY(-8px) scale(1.03) !important;
            box-shadow: 
                0 35px 140px rgba(0, 255, 136, 0.8),
                0 0 200px rgba(0, 255, 255, 0.6),
                inset 0 2px 0 rgba(255, 255, 255, 0.6) !important;
        }
        
        /* Progress Bar */
        .stProgress > div > div > div {
            background: linear-gradient(90deg, #ff0064, #8a2be2, #0096ff) !important;
            background-size: 200% 100% !important;
            border-radius: 10px !important;
            animation: progressFlow 2s linear infinite !important;
            box-shadow: 0 0 20px rgba(255, 0, 100, 0.6) !important;
        }
        
        @keyframes progressFlow {
            0% { background-position: 0% 50%; }
            100% { background-position: 200% 50%; }
        }
        
        /* Result Card */
        .result-card {
            background: linear-gradient(135deg, rgba(255, 0, 100, 0.15), rgba(138, 43, 226, 0.1));
            backdrop-filter: blur(20px);
            border: 3px solid transparent;
            border-radius: 30px;
            padding: 3rem;
            margin: 2rem 0;
            position: relative;
            overflow: hidden;
            animation: resultAppear 0.6s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        @keyframes resultAppear {
            from {
                opacity: 0;
                transform: translateY(40px) scale(0.9);
            }
            to {
                opacity: 1;
                transform: translateY(0) scale(1);
            }
        }
        
        .result-card::before {
            content: '';
            position: absolute;
            inset: 0;
            border-radius: 30px;
            padding: 3px;
            background: linear-gradient(135deg, #ff0064, #8a2be2, #0096ff, #ff0064);
            background-size: 300% 300%;
            -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
            -webkit-mask-composite: xor;
            mask-composite: exclude;
            animation: borderRotate 4s linear infinite;
        }
        
        @keyframes borderRotate {
            0%, 100% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
        }
        
        .result-card::after {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255, 255, 255, 0.1) 0%, transparent 70%);
            animation: spotlight 4s ease-in-out infinite;
        }
        
        @keyframes spotlight {
            0%, 100% { transform: translate(0%, 0%); }
            50% { transform: translate(20%, 20%); }
        }
        
        /* Stats Badges */
        .stat-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.8rem;
            padding: 1rem 1.8rem;
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05));
            backdrop-filter: blur(10px);
            border: 2px solid rgba(255, 255, 255, 0.2);
            border-radius: 50px;
            margin: 0.5rem;
            font-size: 1.1rem;
            font-weight: 600;
            transition: all 0.3s;
        }
        
        .stat-badge:hover {
            background: linear-gradient(135deg, rgba(255, 0, 100, 0.3), rgba(138, 43, 226, 0.2));
            border-color: rgba(255, 0, 100, 0.5);
            transform: translateY(-4px) scale(1.05);
            box-shadow: 0 10px 40px rgba(255, 0, 100, 0.4);
        }
        
        /* Feature Cards */
        .feature-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
            margin: 3rem 0;
        }
        
        .feature-card {
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.05), rgba(255, 255, 255, 0.02));
            backdrop-filter: blur(15px);
            border: 2px solid rgba(255, 255, 255, 0.1);
            border-radius: 25px;
            padding: 2.5rem;
            transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }
        
        .feature-card::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(45deg, transparent, rgba(255, 0, 100, 0.1), transparent);
            transform: rotate(45deg);
            transition: all 0.5s;
        }
        
        .feature-card:hover {
            background: linear-gradient(135deg, rgba(255, 0, 100, 0.1), rgba(138, 43, 226, 0.05));
            border-color: rgba(255, 0, 100, 0.4);
            transform: translateY(-12px) scale(1.02);
            box-shadow: 0 30px 90px rgba(255, 0, 100, 0.4);
        }
        
        .feature-card:hover::before {
            transform: rotate(45deg) translate(50%, 50%);
        }
        
        .feature-icon {
            font-size: 3.5rem;
            margin-bottom: 1.5rem;
            display: inline-block;
            animation: iconFloat 3s ease-in-out infinite;
            filter: drop-shadow(0 0 20px rgba(255, 0, 100, 0.5));
        }
        
        @keyframes iconFloat {
            0%, 100% { transform: translateY(0px) rotate(0deg); }
            50% { transform: translateY(-15px) rotate(10deg); }
        }
        
        /* Thumbnail */
        .stImage {
            border-radius: 25px !important;
            overflow: hidden !important;
            box-shadow: 0 20px 80px rgba(0, 0, 0, 0.5) !important;
            border: 3px solid rgba(255, 0, 100, 0.3) !important;
            transition: all 0.4s !important;
        }
        
        .stImage:hover {
            transform: scale(1.02) !important;
            box-shadow: 0 30px 120px rgba(255, 0, 100, 0.5) !important;
        }
        
        /* Headers */
        h2, h3 {
            background: linear-gradient(135deg, #ff0064, #ff6b9d);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800 !important;
            position: relative;
        }
        
        h2 {
            font-size: 2.2rem !important;
        }
        
        h3 {
            font-size: 1.6rem !important;
        }
        
        /* Alerts */
        .stAlert {
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.08), rgba(255, 255, 255, 0.04)) !important;
            backdrop-filter: blur(10px) !important;
            border-radius: 20px !important;
            border: 2px solid rgba(255, 255, 255, 0.15) !important;
            border-left: 6px solid !important;
        }
        
        /* Expander */
        .streamlit-expanderHeader {
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.08), rgba(255, 255, 255, 0.04)) !important;
            backdrop-filter: blur(10px) !important;
            border-radius: 15px !important;
            border: 2px solid rgba(255, 255, 255, 0.15) !important;
            font-weight: 700 !important;
            font-size: 1.1rem !important;
            transition: all 0.3s !important;
        }
        
        .streamlit-expanderHeader:hover {
            background: linear-gradient(135deg, rgba(255, 0, 100, 0.1), rgba(138, 43, 226, 0.05)) !important;
            border-color: rgba(255, 0, 100, 0.4) !important;
            transform: translateX(10px) !important;
        }
        
        /* Text styling */
        .big-text {
            font-size: 1.2rem;
            line-height: 2;
            color: rgba(255, 255, 255, 0.8);
            font-weight: 400;
        }
        
        /* Success message */
        .stSuccess {
            animation: successPop 0.5s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        @keyframes successPop {
            0% { transform: scale(0.8); opacity: 0; }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); opacity: 1; }
        }
        
        /* Scrollbar */
        ::-webkit-scrollbar {
            width: 12px;
        }
        
        ::-webkit-scrollbar-track {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(135deg, #ff0064, #8a2be2);
            border-radius: 10px;
            border: 2px solid rgba(0, 0, 0, 0.2);
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(135deg, #ff0080, #9d3be8);
        }
        </style>
    """, unsafe_allow_html=True)

def render_hero():
    """Render epic hero section"""
    st.markdown("""
        <div class="mega-hero">
            <div class="epic-icon">🎬</div>
            <h1 class="epic-title">Video Downloader Pro</h1>
            <p class="epic-subtitle">✨ The Most Beautiful Video Downloader Ever Created ✨</p>
            <div class="platform-badges">
                <div class="epic-badge">🎥 YouTube</div>
                <div class="epic-badge">🎵 TikTok</div>
                <div class="epic-badge">⚡ Lightning Fast</div>
                <div class="epic-badge">🎯 HD Quality</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

def render_features():
    """Render stunning features section"""
    st.markdown("""
        <div class="feature-grid">
            <div class="feature-card">
                <div class="feature-icon">⚡</div>
                <h3 style="margin: 0 0 1rem 0;">Lightning Speed</h3>
                <p style="color: rgba(255, 255, 255, 0.7); margin: 0; font-size: 1.05rem;">
                    Download your favorite videos in seconds with our optimized ultra-fast technology
                </p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🎯</div>
                <h3 style="margin: 0 0 1rem 0;">Maximum Quality</h3>
                <p style="color: rgba(255, 255, 255, 0.7); margin: 0; font-size: 1.05rem;">
                    Get crystal-clear HD quality downloads with the best resolution available
                </p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🔒</div>
                <h3 style="margin: 0 0 1rem 0;">100% Secure</h3>
                <p style="color: rgba(255, 255, 255, 0.7); margin: 0; font-size: 1.05rem;">
                    Your privacy matters - completely secure with zero data storage
                </p>
            </div>
        </div>
    """, unsafe_allow_html=True)

def render_tab(platform_name, platform_icon, platform_title):
    """Render download tab with the most beautiful UI"""
    
    st.markdown("""
        <div class="glass-card">
            <h3 style="margin-top: 0; font-size: 1.8rem;">📋 Simple Steps to Download:</h3>
            <p class="big-text">
                <strong style="color: #ff0064;">1️⃣</strong> Copy the video URL from YouTube or TikTok<br>
                <strong style="color: #8a2be2;">2️⃣</strong> Paste it in the magical input field below<br>
                <strong style="color: #0096ff;">3️⃣</strong> Click the glowing "Download Video" button<br>
                <strong style="color: #00ff88;">4️⃣</strong> Wait a few seconds and enjoy your video!
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    url_input = st.text_input(
        "Video URL",
        placeholder=f"✨ Paste your {platform_title.split()[0]} video URL here and watch the magic happen...",
        key=f"{platform_name}_url",
        label_visibility="collapsed"
    )
    
    if st.button(f"{platform_icon} Download Video", type="primary", use_container_width=True, key=f"{platform_name}_download"):
        if not url_input.strip():
            st.error("❌ Oops! Please paste a video URL first!")
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
            with st.expander("🔍 Technical Error Details"):
                st.code(error)
            st.info("💡 **Quick Fixes:**\n- Verify the video is public and not age-restricted\n- Double-check the URL is correct\n- Try another video or refresh the page")
            return
        
        download_time = time.time() - start_time
        
        st.markdown(f"""
            <div class="result-card">
                <h2 style="margin-top: 0; font-size: 2rem; position: relative; z-index: 1;">✅ {video_data['title']}</h2>
                <div style="margin: 1.5rem 0; position: relative; z-index: 1;">
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
        
        st.success("🎉 **Amazing!** Your video is ready for download!")
        
        st.download_button(
            label="⬇️ DOWNLOAD VIDEO NOW",
            data=video_data['data'],
            file_name=video_data['filename'],
            mime="video/mp4",
            use_container_width=True
        )
        
        st.balloons()
        st.info("💡 **Pro Tip:** Your download will begin automatically! Check your Downloads folder.")
    
    with st.expander("ℹ️ Need Help? We've Got You Covered!"):
        st.markdown("""
            ### 🆘 Troubleshooting Guide
            
            **⏰ Download taking forever?**  
            → Larger videos need more processing time. Patience is a virtue! Or try a shorter clip.
            
            **🚫 Video won't download?**  
            → Make sure it's public, not age-restricted, not a live stream, and available in your region.
            
            **⚠️ Getting error messages?**  
            → Try a different video, check your internet connection, or refresh the page.
            
            **🎬 Downloaded video won't play?**  
            → Install VLC Media Player (it plays everything!) or update your current player.
            
            **📉 Quality seems low?**  
            → We download the highest available quality. The source video's quality matters!
            
            **🔒 Is this safe?**  
            → Absolutely! We don't store any of your data. Download and enjoy safely.
        """)

def main():
    """Main application"""
    apply_styles()
    
    render_hero()
    
    st.info("ℹ️ **Platform Notice:** This app performs best when run locally. Streamlit Cloud has file size limitations that may affect large videos.")
    
    render_features()
    
    tab1, tab2 = st.tabs(["🎥 YouTube", "🎵 TikTok"])
    
    with tab1:
        render_tab("youtube", "🎥", "YouTube Downloader")
    
    with tab2:
        render_tab("tiktok", "🎵", "TikTok Downloader")
    
    st.markdown("""
        <div style="text-align: center; padding: 4rem 2rem 2rem 2rem; color: rgba(255, 255, 255, 0.5); margin-top: 5rem; border-top: 2px solid rgba(255, 0, 100, 0.2);">
            <p style="font-size: 1.3rem; margin-bottom: 0.8rem; font-weight: 600; background: linear-gradient(135deg, #ff0064, #8a2be2); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                Video Downloader Pro v5.0 - Ultimate Edition
            </p>
            <p style="font-size: 1rem; color: rgba(255, 255, 255, 0.4); margin-top: 0.5rem;">
                ✨ Most Beautiful UI • ⚡ Lightning Fast • 🎯 HD Quality • 🔒 100% Secure
            </p>
            <p style="font-size: 0.9rem; color: rgba(255, 255, 255, 0.3); margin-top: 1.5rem;">
                For personal use only • Please respect copyright laws and content creators
            </p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Error: {e}")
        st.error("⚠️ Something unexpected happened. Please refresh the page and try again!")
        with st.expander("🔍 Technical Details for Nerds"):
            st.code(str(e))