import os
import subprocess
import sys
import tkinter as tk
from tkinter import messagebox
import tkinter.filedialog as filedialog
import threading
import time
import json

class ModernSpotifyDownloader:
    def __init__(self):
        self.download_path = "C:/Music"  # default
        self.root = tk.Tk()
        self.setup_window()
        self.create_widgets()
        self.animate_entrance()
        
    def setup_window(self):
        """Setup main window properties"""
        self.root.title("Spotify Downloader")
        self.root.geometry("500x650")
        self.root.resizable(False, False)
        
        self.colors = {
            'primary': '#1DB954',
            'primary_dark': '#169C46',
            'background': '#0F0F23',
            'surface': '#1A1A2E',
            'card': '#16213E',
            'text': '#FFFFFF',
            'text_secondary': '#B3B3B3',
            'accent': '#FF6B6B',
            'success': '#4ECDC4'
        }
        
        self.root.configure(bg=self.colors['background'])
        
        icon_path = os.path.join(os.path.dirname(__file__), "spotify.ico")
        if os.path.exists(icon_path):
            try:
                self.root.iconbitmap(icon_path)
            except:
                pass
                
    def create_widgets(self):
        self.main_frame = tk.Frame(
            self.root, 
            bg=self.colors['background'],
            padx=30,
            pady=30
        )
        self.main_frame.pack(fill='both', expand=True)
        
        self.create_header()
        self.create_logo_section()
        self.create_input_section()
        self.create_download_button()
        self.create_progress_section()
        self.create_status_section()
        self.create_footer()

        self.url_var.trace('w', self.on_url_change)
    
    def create_header(self):
        self.title_label = tk.Label(
            self.main_frame,
            text="Spotify Downloader",
            font=('Segoe UI', 24, 'bold'),
            fg=self.colors['text'],
            bg=self.colors['background']
        )
        self.title_label.pack(pady=(0, 5))
        
        self.subtitle_label = tk.Label(
            self.main_frame,
            text="Download your favorite music and playlists",
            font=('Segoe UI', 11),
            fg=self.colors['text_secondary'],
            bg=self.colors['background']
        )
        self.subtitle_label.pack(pady=(0, 30))
    
    def create_logo_section(self):
        self.logo_frame = tk.Frame(
            self.main_frame,
            bg=self.colors['card'],
            height=120,
            relief='flat',
            bd=0
        )
        self.logo_frame.pack(fill='x', pady=(0, 30))
        self.logo_frame.pack_propagate(False)
        
        self.logo_label = tk.Label(
            self.logo_frame,
            text="♫",
            font=('Segoe UI', 48),
            fg=self.colors['primary'],
            bg=self.colors['card']
        )
        self.logo_label.pack(expand=True)
    
    def create_input_section(self):
        self.input_frame = tk.Frame(
            self.main_frame,
            bg=self.colors['background']
        )
        self.input_frame.pack(fill='x', pady=(0, 20))
        
        self.input_label = tk.Label(
            self.input_frame,
            text="Spotify URL",
            font=('Segoe UI', 12, 'bold'),
            fg=self.colors['text'],
            bg=self.colors['background'],
            anchor='w'
        )
        self.input_label.pack(fill='x', pady=(0, 8))
        
        self.url_var = tk.StringVar()
        
        self.entry = tk.Entry(
            self.input_frame,
            textvariable=self.url_var,
            font=('Segoe UI', 12),
            bg=self.colors['surface'],
            fg=self.colors['text'],
            insertbackground=self.colors['primary'],
            relief='flat',
            bd=0,
            highlightthickness=2,
            highlightcolor=self.colors['primary'],
            highlightbackground=self.colors['surface']
        )
        self.entry.pack(fill='x', ipady=12, pady=(0, 5))
        
        self.entry.insert(0, "https://open.spotify.com/...")
        self.entry.bind('<FocusIn>', self.on_entry_focus_in)
        self.entry.bind('<FocusOut>', self.on_entry_focus_out)
        self.entry.config(fg=self.colors['text_secondary'])
        
        self.helper_label = tk.Label(
            self.input_frame,
            text="Paste your Spotify track or playlist URL here",
            font=('Segoe UI', 9),
            fg=self.colors['text_secondary'],
            bg=self.colors['background'],
            anchor='w'
        )
        self.helper_label.pack(fill='x')

        # Tambahkan tombol pilih folder
        self.folder_frame = tk.Frame(
            self.input_frame,
            bg=self.colors['background']
        )
        self.folder_frame.pack(fill='x', pady=(10, 0))

        self.folder_label = tk.Label(
            self.folder_frame,
            text=f"Folder: {self.download_path}",
            font=('Segoe UI', 9),
            fg=self.colors['text_secondary'],
            bg=self.colors['background'],
            anchor='w'
        )
        self.folder_label.pack(side='left', fill='x', expand=True)

        self.choose_folder_button = tk.Button(
            self.folder_frame,
            text="Pilih Folder",
            font=('Segoe UI', 9, 'bold'),
            bg=self.colors['surface'],
            fg=self.colors['primary'],
            activebackground=self.colors['primary'],
            activeforeground='white',
            relief='flat',
            bd=0,
            cursor='hand2',
            command=self.choose_folder
        )
        self.choose_folder_button.pack(side='right')
    
    def create_download_button(self):
        self.button_frame = tk.Frame(
            self.main_frame,
            bg=self.colors['background']
        )
        self.button_frame.pack(fill='x', pady=(30, 20))
        
        self.download_button = tk.Button(
            self.button_frame,
            text="Download",
            font=('Segoe UI', 14, 'bold'),
            bg=self.colors['primary'],
            fg='white',
            activebackground=self.colors['primary_dark'],
            activeforeground='white',
            relief='flat',
            bd=0,
            cursor='hand2',
            command=self.start_download
        )
        self.download_button.pack(fill='x', ipady=15)
        
        self.download_button.bind('<Enter>', self.on_button_hover)
        self.download_button.bind('<Leave>', self.on_button_leave)
    
    def create_progress_section(self):
        self.progress_frame = tk.Frame(
            self.main_frame,
            bg=self.colors['background']
        )
        self.progress_frame.pack(fill='x', pady=(0, 20))
        
        self.progress_bg = tk.Frame(
            self.progress_frame,
            bg=self.colors['surface'],
            height=6
        )
        self.progress_bg.pack(fill='x')
        self.progress_bg.pack_propagate(False)
        
        self.progress_fill = tk.Frame(
            self.progress_bg,
            bg=self.colors['primary'],
            height=6
        )
        
        self.progress_text = tk.Label(
            self.progress_frame,
            text="",
            font=('Segoe UI', 10),
            fg=self.colors['text_secondary'],
            bg=self.colors['background']
        )
        self.progress_text.pack(pady=(10, 0))
    
    def create_status_section(self):
        self.status_frame = tk.Frame(
            self.main_frame,
            bg=self.colors['card'],
            relief='flat',
            bd=0
        )
        self.status_frame.pack(fill='x', pady=(0, 20))
        
        self.status_label = tk.Label(
            self.status_frame,
            text="Ready to download",
            font=('Segoe UI', 11),
            fg=self.colors['text_secondary'],
            bg=self.colors['card']
        )
        self.status_label.pack(pady=15)
    
    def create_footer(self):
        self.footer_frame = tk.Frame(
            self.main_frame,
            bg=self.colors['background']
        )
        self.footer_frame.pack(side='bottom', fill='x', pady=(20, 0))
        
        self.version_label = tk.Label(
            self.footer_frame,
            text="Powered by spotdl • v2.0",
            font=('Segoe UI', 9),
            fg=self.colors['text_secondary'],
            bg=self.colors['background']
        )
        self.version_label.pack()
    
    def animate_entrance(self):
        self.main_frame.pack_forget()
        self.root.after(100, self.fade_in)
    
    def fade_in(self):
        self.main_frame.pack(fill='both', expand=True)
        self.animate_logo_bounce()
    
    def animate_logo_bounce(self):
        original_font = self.logo_label.cget('font')
        
        def bounce_animation(step=0):
            if step < 10:
                size = 48 + int(8 * abs(5 - step) / 5)
                self.logo_label.config(font=('Segoe UI', size))
                self.root.after(50, lambda: bounce_animation(step + 1))
            else:
                self.logo_label.config(font=('Segoe UI', 48))
        
        bounce_animation()
    
    def on_entry_focus_in(self, event):
        if self.entry.get() == "https://open.spotify.com/...":
            self.entry.delete(0, tk.END)
            self.entry.config(fg=self.colors['text'])
    
    def on_entry_focus_out(self, event):
        if not self.entry.get():
            self.entry.insert(0, "https://open.spotify.com/...")
            self.entry.config(fg=self.colors['text_secondary'])
    
    def on_url_change(self, *args):
        url = self.url_var.get()
        if url and url != "https://open.spotify.com/...":
            if "spotify.com" in url:
                self.entry.config(highlightbackground=self.colors['primary'])
                self.download_button.config(state='normal')
            else:
                self.entry.config(highlightbackground=self.colors['accent'])
                self.download_button.config(state='normal')
        else:
            self.entry.config(highlightbackground=self.colors['surface'])
            self.download_button.config(state='normal')
    
    def on_button_hover(self, event):
        self.download_button.config(bg=self.colors['primary_dark'])
    
    def on_button_leave(self, event):
        self.download_button.config(bg=self.colors['primary'])
    
    def update_progress(self, value, text=""):
        if value == 0:
            self.progress_fill.place_forget()
        else:
            width = int(self.progress_bg.winfo_width() * value / 100)
            self.progress_fill.place(x=0, y=0, width=width, height=6)
        
        self.progress_text.config(text=text)
        self.root.update()
    
    def update_status(self, message, color=None):
        if color is None:
            color = self.colors['text_secondary']
        self.status_label.config(text=message, fg=color)
        self.root.update()
    
    def install_python_and_libraries(self):
        try:
            subprocess.run(["python", "--version"], check=True, stdout=subprocess.PIPE)
        except subprocess.CalledProcessError:
            messagebox.showerror("Error", "Python tidak terinstal. Silakan instal Python terlebih dahulu.")
            return False

        try:
            subprocess.run(["pip", "show", "spotdl"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError:
            try:
                self.update_status("Installing spotdl...", self.colors['primary'])
                subprocess.run(["pip", "install", "spotdl"], check=True)
                self.update_status("spotdl installed successfully!", self.colors['success'])
                time.sleep(1)
            except subprocess.CalledProcessError:
                messagebox.showerror("Error", "Gagal menginstal spotdl. Periksa koneksi internet Anda.")
                return False
        return True
    
    def get_playlist_name(self, spotify_url):
        """Get playlist name using spotdl meta (JSON)"""
        try:
            result = subprocess.run(
                ["spotdl", "meta", "--json", spotify_url],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            data = json.loads(result.stdout)
            if isinstance(data, dict) and "name" in data:
                return data["name"]
        except Exception as e:
            print("Metadata error:", e)
        return "Playlist"
    
    def sanitize_filename(self, name):
        return "".join(c for c in name if c not in r'\/:*?"<>|').strip()

    def download_spotify(self, spotify_url):
        download_path = self.download_path  # gunakan folder yang dipilih user

        if not os.path.exists(download_path):
            os.makedirs(download_path)

        if "playlist" in spotify_url:
            playlist_name = self.get_playlist_name(spotify_url)
            playlist_name = self.sanitize_filename(playlist_name)
            playlist_folder = os.path.join(download_path, playlist_name)
            if not os.path.exists(playlist_folder):
                os.makedirs(playlist_folder)
            output_path = playlist_folder
        else:
            output_path = download_path

        try:
            self.update_status("Downloading...", self.colors['primary'])
            self.update_progress(0, "Starting download...")
            
            for i in range(0, 101, 20):
                self.update_progress(i, f"Downloading... {i}%")
                time.sleep(0.5)
            
            subprocess.run(["spotdl", "download", spotify_url, "--output", output_path], check=True)
            
            self.update_progress(100, "Download complete!")
            self.update_status(f"Download successful! Saved to: {output_path}", self.colors['success'])
            
            messagebox.showinfo("Success", f"Download complete! Files saved to: {output_path}")
            
        except subprocess.CalledProcessError as e:
            self.update_progress(0, "")
            self.update_status("Download failed", self.colors['accent'])
            messagebox.showerror("Error", f"Download error: {e}")
        finally:
            self.download_button.config(state='normal', text="Download")
    
    def start_download(self):
        spotify_link = self.entry.get()
        
        if not spotify_link or spotify_link == "https://open.spotify.com/...":
            messagebox.showwarning("Warning", "Please enter a valid Spotify URL.")
            return
        
        if "spotify.com" not in spotify_link:
            messagebox.showwarning("Warning", "Please enter a valid Spotify URL.")
            return
        
        self.download_button.config(state='disabled', text="Downloading...")
        
        if not self.install_python_and_libraries():
            self.download_button.config(state='normal', text="Download")
            return
        
        download_thread = threading.Thread(
            target=self.download_spotify, 
            args=(spotify_link,)
        )
        download_thread.daemon = True
        download_thread.start()
    
    def choose_folder(self):
        folder = filedialog.askdirectory(initialdir=self.download_path)
        if folder:
            self.download_path = folder
            self.folder_label.config(text=f"Folder: {self.download_path}")
            messagebox.showinfo("Folder Dipilih", f"Folder unduhan diubah menjadi:\n{self.download_path}")
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ModernSpotifyDownloader()
    app.run()
