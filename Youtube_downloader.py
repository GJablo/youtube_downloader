import os
import subprocess
import json
import tkinter as tk
from tkinter import ttk, messagebox

def get_available_formats(url):
    result = subprocess.run(
        ["yt-dlp", "-F", url],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    return result.stdout

def download_format(url, format_code, output):
    subprocess.run([
        "yt-dlp",
        "-f", format_code,
        "-o", output,
        url
    ])

def merge_video_audio(video_file, audio_file, output_file):
    subprocess.run([
        "ffmpeg",
        "-i", video_file,
        "-i", audio_file,
        "-c", "copy",
        output_file
    ])

def on_download():
    video_url = url_entry.get()
    if not video_url:
        messagebox.showerror("Error", "Please enter a video URL")
        return

    formats = get_available_formats(video_url)
    formats_display.delete(1.0, tk.END)
    formats_display.insert(tk.END, formats)

def on_merge():
    video_url = url_entry.get()
    video_format_code = video_format_entry.get()
    audio_format_code = audio_format_entry.get()
    
    if not video_url or not video_format_code or not audio_format_code:
        messagebox.showerror("Error", "Please enter all required information")
        return

    video_output = "video.mp4"
    audio_output = "audio.m4a"
    final_output = input("Give your video a name. use underscore '_' not spaces eg finalVideo.mp4 or final_video.mp4: ")

    download_format(video_url, video_format_code, video_output)
    download_format(video_url, audio_format_code, audio_output)

    merge_video_audio(video_output, audio_output, final_output)

    os.remove(video_output)
    os.remove(audio_output)

    messagebox.showinfo("Success", f"Done! The final output is saved as {final_output}")

app = tk.Tk()
app.title("Decipher YouTube Video Downloader")

tk.Label(app, text="Video URL:").grid(row=0, column=0, padx=10, pady=10)
url_entry = tk.Entry(app, width=50)
url_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Button(app, text="Get Formats", command=on_download).grid(row=0, column=2, padx=10, pady=10)

formats_display = tk.Text(app, width=100, height=20)
formats_display.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

tk.Label(app, text="Video Format Code:").grid(row=2, column=0, padx=10, pady=10)
video_format_entry = tk.Entry(app, width=20)
video_format_entry.grid(row=2, column=1, padx=10, pady=10)

tk.Label(app, text="Audio Format Code:").grid(row=3, column=0, padx=10, pady=10)
audio_format_entry = tk.Entry(app, width=20)
audio_format_entry.grid(row=3, column=1, padx=10, pady=10)

tk.Button(app, text="Download and Merge", command=on_merge).grid(row=4, column=0, columnspan=3, padx=10, pady=10)

app.mainloop()

