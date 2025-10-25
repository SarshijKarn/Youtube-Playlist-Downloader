#!/usr/bin/env python3
"""
YouTube Playlist Downloader - GUI Version
A graphical interface for downloading YouTube playlists
"""

import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
import threading
from pathlib import Path
import yt_dlp


class PlaylistDownloaderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Playlist Downloader")
        self.root.geometry("700x600")
        self.root.resizable(True, True)
        
        self.download_thread = None
        self.is_downloading = False
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(5, weight=1)
        
        # URL input
        ttk.Label(main_frame, text="Playlist/Video URL:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.url_entry = ttk.Entry(main_frame, width=50)
        self.url_entry.grid(row=0, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Download path
        ttk.Label(main_frame, text="Download Folder:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.path_entry = ttk.Entry(main_frame, width=40)
        self.path_entry.insert(0, str(Path("downloads").absolute()))
        self.path_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)
        
        browse_btn = ttk.Button(main_frame, text="Browse", command=self.browse_folder)
        browse_btn.grid(row=1, column=2, sticky=tk.W, padx=5, pady=5)
        
        # Format selection
        ttk.Label(main_frame, text="Format:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.format_var = tk.StringVar(value="best")
        format_frame = ttk.Frame(main_frame)
        format_frame.grid(row=2, column=1, columnspan=2, sticky=tk.W, pady=5)
        
        formats = [
            ("Best Quality", "best"),
            ("1080p", "1080p"),
            ("720p", "720p"),
            ("480p", "480p"),
            ("Audio Only (MP3)", "audio")
        ]
        
        for i, (text, value) in enumerate(formats):
            ttk.Radiobutton(format_frame, text=text, variable=self.format_var, 
                           value=value).grid(row=0, column=i, padx=5)
        
        # Progress bar
        ttk.Label(main_frame, text="Progress:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=3, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Download button
        self.download_btn = ttk.Button(main_frame, text="Download", command=self.start_download)
        self.download_btn.grid(row=4, column=0, columnspan=3, pady=10)
        
        # Output log
        ttk.Label(main_frame, text="Log:").grid(row=5, column=0, sticky=(tk.W, tk.N), pady=5)
        self.log_text = scrolledtext.ScrolledText(main_frame, height=15, width=70, 
                                                   state='disabled', wrap=tk.WORD)
        self.log_text.grid(row=5, column=1, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, folder)
    
    def log(self, message):
        """Add message to log window"""
        self.log_text.configure(state='normal')
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.configure(state='disabled')
        self.root.update_idletasks()
    
    def start_download(self):
        if self.is_downloading:
            messagebox.showwarning("Download in Progress", "A download is already in progress!")
            return
        
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a URL")
            return
        
        download_path = self.path_entry.get().strip()
        if not download_path:
            messagebox.showerror("Error", "Please select a download folder")
            return
        
        # Start download in separate thread
        self.is_downloading = True
        self.download_btn.configure(state='disabled')
        self.progress.start()
        self.log_text.configure(state='normal')
        self.log_text.delete(1.0, tk.END)
        self.log_text.configure(state='disabled')
        
        self.download_thread = threading.Thread(
            target=self.download_playlist,
            args=(url, download_path),
            daemon=True
        )
        self.download_thread.start()
    
    def download_playlist(self, url, download_path):
        """Download playlist in background thread"""
        try:
            Path(download_path).mkdir(parents=True, exist_ok=True)
            
            ydl_opts = {
                'outtmpl': str(Path(download_path) / '%(playlist)s/%(title)s.%(ext)s'),
                'ignoreerrors': True,
                'no_warnings': False,
                'progress_hooks': [self.progress_hook],
            }
            
            format_choice = self.format_var.get()
            
            if format_choice == "audio":
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
            
            self.log(f"Starting download from: {url}")
            self.log(f"Saving to: {download_path}")
            self.log("-" * 60)
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                
                if 'entries' in info:
                    playlist_title = info.get('title', 'Unknown Playlist')
                    video_count = len([e for e in info['entries'] if e])
                    self.log("-" * 60)
                    self.log(f"✓ Successfully downloaded playlist: {playlist_title}")
                    self.log(f"✓ Total videos: {video_count}")
                else:
                    self.log("-" * 60)
                    self.log("✓ Successfully downloaded single video")
            
            self.root.after(0, lambda: messagebox.showinfo("Success", "Download completed!"))
            
        except Exception as e:
            self.log(f"✗ Error: {str(e)}")
            self.root.after(0, lambda: messagebox.showerror("Error", f"Download failed: {str(e)}"))
        
        finally:
            self.root.after(0, self.download_complete)
    
    def progress_hook(self, d):
        """Progress callback from yt-dlp"""
        if d['status'] == 'downloading':
            filename = Path(d.get('filename', 'unknown')).name
            percent = d.get('_percent_str', 'N/A')
            speed = d.get('_speed_str', 'N/A')
            self.log(f"Downloading: {filename} - {percent} at {speed}")
        elif d['status'] == 'finished':
            filename = Path(d.get('filename', 'unknown')).name
            self.log(f"✓ Finished: {filename}")
    
    def download_complete(self):
        """Called when download finishes"""
        self.is_downloading = False
        self.download_btn.configure(state='normal')
        self.progress.stop()


def main():
    root = tk.Tk()
    app = PlaylistDownloaderGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

