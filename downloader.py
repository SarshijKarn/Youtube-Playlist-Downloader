#!/usr/bin/env python3
"""
YouTube Playlist Downloader
A simple application to download YouTube playlists using yt-dlp
"""

import os
import sys
import yt_dlp
from pathlib import Path


class PlaylistDownloader:
    def __init__(self, download_path="downloads"):
        self.download_path = Path(download_path)
        self.download_path.mkdir(exist_ok=True)
        
    def download_playlist(self, playlist_url, format_choice="best", audio_only=False):
        """
        Download a YouTube playlist
        
        Args:
            playlist_url: URL of the YouTube playlist
            format_choice: Video quality (best, 1080p, 720p, 480p)
            audio_only: If True, download only audio
        """
        try:
            ydl_opts = {
                'outtmpl': str(self.download_path / '%(playlist)s/%(title)s.%(ext)s'),
                'ignoreerrors': True,
                'no_warnings': False,
                'progress_hooks': [self.progress_hook],
            }
            
            if audio_only:
                ydl_opts.update({
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                })
            else:
                if format_choice == "1080p":
                    ydl_opts['format'] = 'bestvideo[height<=1080]+bestaudio/best[height<=1080]'
                elif format_choice == "720p":
                    ydl_opts['format'] = 'bestvideo[height<=720]+bestaudio/best[height<=720]'
                elif format_choice == "480p":
                    ydl_opts['format'] = 'bestvideo[height<=480]+bestaudio/best[height<=480]'
                else:
                    ydl_opts['format'] = 'bestvideo+bestaudio/best'
            
            print(f"\n{'='*60}")
            print(f"Starting download from: {playlist_url}")
            print(f"Save location: {self.download_path.absolute()}")
            print(f"{'='*60}\n")
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(playlist_url, download=True)
                
                if 'entries' in info:
                    playlist_title = info.get('title', 'Unknown Playlist')
                    video_count = len([e for e in info['entries'] if e])
                    print(f"\n{'='*60}")
                    print(f"✓ Successfully downloaded playlist: {playlist_title}")
                    print(f"✓ Total videos: {video_count}")
                    print(f"{'='*60}\n")
                else:
                    print("\n✓ Successfully downloaded single video\n")
                    
            return True
            
        except Exception as e:
            print(f"\n✗ Error occurred: {str(e)}\n")
            return False
    
    def progress_hook(self, d):
        """Hook to display download progress"""
        if d['status'] == 'downloading':
            print(f"\rDownloading: {d.get('filename', 'unknown')} - "
                  f"{d.get('_percent_str', 'N/A')} at {d.get('_speed_str', 'N/A')}", 
                  end='', flush=True)
        elif d['status'] == 'finished':
            print(f"\n✓ Download completed: {d.get('filename', 'unknown')}")


def main():
    print("\n" + "="*60)
    print("YouTube Playlist Downloader".center(60))
    print("="*60 + "\n")
    
    # Get playlist URL
    playlist_url = input("Enter YouTube playlist URL (or video URL): ").strip()
    
    if not playlist_url:
        print("Error: No URL provided")
        return
    
    # Get download path
    download_path = input("Enter download folder (press Enter for 'downloads'): ").strip()
    if not download_path:
        download_path = "downloads"
    
    # Get format choice
    print("\nSelect format:")
    print("1. Best quality (default)")
    print("2. 1080p")
    print("3. 720p")
    print("4. 480p")
    print("5. Audio only (MP3)")
    
    choice = input("\nEnter choice (1-5): ").strip()
    
    format_map = {
        "1": ("best", False),
        "2": ("1080p", False),
        "3": ("720p", False),
        "4": ("480p", False),
        "5": ("best", True),
    }
    
    format_choice, audio_only = format_map.get(choice, ("best", False))
    
    # Download
    downloader = PlaylistDownloader(download_path)
    success = downloader.download_playlist(playlist_url, format_choice, audio_only)
    
    if success:
        print(f"All files saved to: {Path(download_path).absolute()}")
    else:
        print("Download failed or incomplete")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nDownload cancelled by user")
        sys.exit(0)

