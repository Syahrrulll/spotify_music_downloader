@echo off
echo ===========================================
echo Memeriksa instalasi Python, spotdl, dan FFmpeg
echo ===========================================

:: Periksa apakah Python sudah terinstal
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Python tidak ditemukan. Mengunduh dan menginstal Python...

    :: Download installer Python
    powershell -Command "Invoke-WebRequest -Uri https://www.python.org/ftp/python/3.13.1/python-3.13.1-amd64.exe -OutFile python-installer.exe"
    if NOT EXIST python-installer.exe (
        echo Gagal mengunduh installer Python. Pastikan koneksi internet Anda stabil.
        pause
        exit /b 1
    )

    :: Jalankan installer Python
    start /wait python-installer.exe /quiet InstallAllUsers=1 PrependPath=1
    if %ERRORLEVEL% NEQ 0 (
        echo Instalasi Python gagal. Silakan instal Python secara manual.
	    echo Silahkan Buka python-installer.exe
        echo Lalu Menjalankan file ini lagi
        echo .
        echo .
        pause
        exit /b 1
    )

    echo Python berhasil diinstal.
) else (
    echo Python sudah terinstal.
)

:: Perbarui pip
echo Memperbarui pip...
python -m pip install --upgrade pip

:: Periksa apakah spotdl sudah terinstal
pip show spotdl >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo spotdl tidak ditemukan. Menginstal spotdl...
    pip install spotdl
    if %ERRORLEVEL% NEQ 0 (
        echo Instalasi spotdl gagal. Pastikan pip berfungsi dengan benar.
        pause
        exit /b 1
    )
) else (
    echo spotdl sudah terinstal.
)

:: Periksa apakah FFmpeg sudah tersedia
ffmpeg -version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo FFmpeg tidak ditemukan. Mengunduh dan menginstal FFmpeg...

    :: Download dan instal FFmpeg melalui spotdl
    spotdl --download-ffmpeg
    if %ERRORLEVEL% NEQ 0 (
        echo Instalasi FFmpeg gagal. Pastikan koneksi internet Anda stabil.
        echo ==ABAIKAN KALAU FFMPEG SUDAH TERINSTAL====
        pause

    )
) else (
    echo FFmpeg sudah terinstal.
)

:: Semua komponen sudah terinstal, jalankan aplikasi utama
if EXIST spotify_downloader.py (
    echo Semua komponen berhasil diinstal. Menjalankan aplikasi Spotify Downloader...
    python spotify_downloader.py
    exit
) else (
    echo File spotify_downloader.py tidak ditemukan. Pastikan file berada di folder yang sama.File spotify_downloader.py tidak ditemukan. Pastikan file berada di folder yang sama.
    pause
    exit /b 1   exit /b 1
)

pausepause

