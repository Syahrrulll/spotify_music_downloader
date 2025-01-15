import os
import subprocess
import sys

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

def main():
    """
    Logika utama untuk menjalankan downloader.
    """
    # Pastikan install_python.bat sudah dijalankan
    batch_file = "install_python.bat"
    if not os.path.exists(batch_file):
        print(f"File {batch_file} tidak ditemukan. Pastikan batch file ada di folder yang sama.")
        sys.exit(1)

    print("Menjalankan install_python.bat...")
    run_batch_file(batch_file)
    
    print("Memvalidasi instalasi...")
    validate_installation()

    print("Semua persiapan selesai. Jalankan logika utama aplikasi di sini.")
    # Tambahkan logika downloader atau GUI Anda di bawah ini
    # ...

if __name__ == "__main__":
    main()
