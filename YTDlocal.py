import subprocess
import sys
import shutil
import re
from pathlib import Path

OUT_DIR = Path.home() / "Downloads" / "YT_Downloads"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def check_dependencies():
    required = ["ffmpeg", "node"]
    missing = [x for x in required if shutil.which(x) is None]
    if missing:
        print("Missing:", ", ".join(missing))
        sys.exit()


def format_progress(line):
    match = re.search(r"(\d{1,3}\.\d|\d{1,3})%", line)
    if not match:
        return None

    percent = float(match.group(1))
    filled = int(percent / 2.5)
    bar = "█" * filled + " " * (40 - filled)
    return f"[{bar}] {percent:5.1f}%"


def get_video_format():
    formats = {
        "1": ("Best available", "bv*+ba/b"),
        "2": ("8K (4320p)", "bv*[height<=4320]+ba/b[height<=4320]"),
        "3": ("4K (2160p)", "bv*[height<=2160]+ba/b[height<=2160]"),
        "4": ("1440p", "bv*[height<=1440]+ba/b[height<=1440]"),
        "5": ("1080p", "bv*[height<=1080]+ba/b[height<=1080]"),
        "6": ("720p", "bv*[height<=720]+ba/b[height<=720]"),
        "7": ("480p", "bv*[height<=480]+ba/b[height<=480]"),
        "8": ("360p", "bv*[height<=360]+ba/b[height<=360]"),
    }

    print("\nVideo quality options:")
    for k, v in formats.items():
        print(f"{k} - {v[0]}")

    choice = input("Select video quality: ").strip()
    return formats.get(choice, formats["1"])[1]


def get_audio_format():
    formats = {
        "1": "m4a",
        "2": "mp3",
        "3": "wav",
        "4": "ogg",
    }

    print("\nAudio format options:")
    print("1 - M4A (best quality)")
    print("2 - MP3")
    print("3 - WAV")
    print("4 - OGG")

    choice = input("Select audio format: ").strip()
    return formats.get(choice, "m4a")


def download(url, fmt, audio=False, audio_ext=None):
    command = [
        sys.executable, "-m", "yt_dlp",
        "--js-runtimes", "node",
        "--remote-components", "ejs:github",
        "-f", fmt,
        "-o", str(OUT_DIR / "%(title).200s.%(ext)s"),
        url
    ]

    if audio:
        command += ["-x", "--audio-format", audio_ext, "--audio-quality", "0"]

    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    for line in process.stdout:
        line = line.strip()

        progress = format_progress(line)
        if progress:
            print("\r" + progress, end="")
        elif "Downloading" in line:
            print(line)

    process.wait()
    print("\nDone.")
    print("Saved to:", OUT_DIR)


def main():
    print("YouTube Downloader (Windows x64)")
    print("--------------------------------")

    check_dependencies()

    url = input("\nPaste YouTube URL: ").strip()
    if not url:
        return

    print("\nMode:")
    print("1 - Video download")
    print("2 - Audio download")

    mode = input("Select mode: ").strip()

    if mode == "2":
        audio_ext = get_audio_format()
        download(url, "bestaudio/b", audio=True, audio_ext=audio_ext)
    else:
        fmt = get_video_format()
        download(url, fmt)

    input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()