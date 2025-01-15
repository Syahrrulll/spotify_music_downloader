import os
import subprocess
import sys
import tkinter as tk
from tkinter import messagebox

def install_python_and_libraries():
    """
    Memastikan Python dan library yang diperlukan terinstal. Jika tidak, menjalankan instalasi.
    """
    try:
        # Cek apakah Python sudah terinstal
        subprocess.run(["python", "--version"], check=True, stdout=subprocess.PIPE)
    except subprocess.CalledProcessError:
        messagebox.showerror("Error", "Python tidak terinstal. Instalasi otomatis akan dimulai.")
        subprocess.run([os.path.join(os.getcwd(), "install_python.bat")])
        sys.exit(1)  # Setelah instalasi selesai, keluar dari aplikasi

    # Cek dan instal spotdl jika belum terinstal
    try:
        subprocess.run(["pip", "show", "spotdl"], check=True)
    except subprocess.CalledProcessError:
        try:
            messagebox.showinfo("Informasi", "spotdl tidak ditemukan. Instalasi akan dimulai.")
            subprocess.run(["pip", "install", "spotdl"], check=True)
            messagebox.showinfo("Sukses", "spotdl berhasil diinstal.")
        except subprocess.CalledProcessError:
            messagebox.showerror("Error", "Gagal menginstal spotdl. Periksa koneksi internet Anda.")
            sys.exit(1)  # Keluar jika instalasi gagal

def download_spotify(spotify_url):
    """
    Mengunduh lagu atau playlist dari Spotify menggunakan spotdl,
    menyimpan di folder C:/Music, dan tidak membuat folder baru untuk playlist.
    
    Args:
        spotify_url (str): URL lagu atau playlist dari Spotify.
    """

    # Tentukan path folder download (tanpa folder baru)
    download_path = "C:/Music"

    # Pastikan folder tujuan ada
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    try:
        # Jalankan perintah spotdl untuk mengunduh ke folder yang sesuai
        subprocess.run(["spotdl", "download", spotify_url, "--output", download_path], check=True)
        messagebox.showinfo("Sukses", f"Download selesai! Lagu disimpan di: {download_path}")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Terjadi kesalahan saat mendownload: {e}")

def on_submit():
    spotify_link = entry.get()
    if spotify_link:
        download_spotify(spotify_link)
    else:
        messagebox.showwarning("Peringatan", "URL Spotify tidak boleh kosong.")


# GUI menggunakan tkinter
root = tk.Tk()
root.title("Spotify Downloader")

# Desain GUI
label = tk.Label(root, text="Masukkan URL Spotify:")
label.pack(pady=10)

entry = tk.Entry(root, width=40)
entry.pack(pady=10)

submit_button = tk.Button(root, text="Download", command=on_submit)
submit_button.pack(pady=20)

root.mainloop()

def run_batch_file(batch_file):
    """
    Menjalankan file batch dan menunggu hingga selesai.
    Args:
        batch_file (str): Path ke file batch.
    """
    try:
        subprocess.run(batch_file, check=True, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Error saat menjalankan {batch_file}: {e}")
        sys.exit(1)  # Keluar jika batch file gagal

def validate_installation():
    """
    Validasi apakah Python, spotdl, dan ffmpeg sudah terinstal.
    """
    # Cek Python
    try:
        subprocess.run(["python", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except FileNotFoundError:
        print("Python tidak terinstal. Periksa install_python.bat.")
        sys.exit(1)

    # Cek spotdl
    try:
        subprocess.run(["spotdl", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except FileNotFoundError:
        print("spotdl tidak terinstal. Periksa install_python.bat.")
        sys.exit(1)

    # Cek ffmpeg
    try:
        subprocess.run(["ffmpeg", "-version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except FileNotFoundError:
        print("FFmpeg tidak terinstal. Periksa install_python.bat.")
        sys.exit(1)
def on_submit():
    spotify_link = entry.get()
    if spotify_link:
        download_spotify(spotify_link)
    else:
        messagebox.showwarning("Peringatan", "URL Spotify tidak boleh kosong.")

# Memastikan Python dan libraries terinstal
install_python_and_libraries()

# GUI menggunakan tkinter
root = tk.Tk()
root.title("Spotify Downloader")

# Desain GUI
label = tk.Label(root, text="Masukkan URL Spotify:")
label.pack(pady=10)

entry = tk.Entry(root, width=40)
entry.pack(pady=10)

submit_button = tk.Button(root, text="Download", command=on_submit)
submit_button.pack(pady=20)

root.mainloop()
