import os
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading

def get_available_formats(url):
    """Retrieve available video formats using yt-dlp"""
    try:
        result = subprocess.run(
            ["yt-dlp", "-F", url],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error retrieving formats: {e.stderr}"

def download_format(url, format_code, output):
    """Download specific format using yt-dlp"""
    subprocess.run([
        "yt-dlp",
        "-f", format_code,
        "-o", output,
        url
    ], check=True)

def merge_video_audio(video_file, audio_file, output_file):
    """Merge video and audio streams using ffmpeg"""
    subprocess.run([
        "ffmpeg",
        "-i", video_file,
        "-i", audio_file,
        "-c", "copy",
        "-y",  # Overwrite without prompt
        output_file
    ], check=True)

def on_download():
    """Handle format retrieval button click"""
    video_url = url_entry.get()
    if not video_url:
        messagebox.showerror("Error", "Please enter a video URL")
        return

    # Disable button during processing
    get_formats_btn.config(state=tk.DISABLED)
    status_var.set("Retrieving available formats...")

    def worker():
        try:
            formats = get_available_formats(video_url)
            formats_display.config(state=tk.NORMAL)
            formats_display.delete(1.0, tk.END)
            formats_display.insert(tk.END, formats)
            formats_display.config(state=tk.DISABLED)
            status_var.set("Formats retrieved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to get formats: {str(e)}")
            status_var.set("Ready")
        finally:
            get_formats_btn.config(state=tk.NORMAL)

    threading.Thread(target=worker, daemon=True).start()

def on_merge():
    """Handle download and merge button click"""
    video_url = url_entry.get()
    video_format_code = video_format_entry.get()
    audio_format_code = audio_format_entry.get()

    if not all([video_url, video_format_code, audio_format_code]):
        messagebox.showerror("Error", "Please enter all required information")
        return

    # Get output file path
    output_file = filedialog.asksaveasfilename(
        defaultextension=".mp4",
        filetypes=[("MP4 files", "*.mp4"), ("All files", "*.*")],
        title="Save Video As"
    )
    if not output_file:
        return  # User canceled

    # Disable button during processing
    merge_btn.config(state=tk.DISABLED)
    status_var.set("Downloading and merging...")

    def worker():
        try:
            video_output = "temp_video.mp4"
            audio_output = "temp_audio.m4a"

            download_format(video_url, video_format_code, video_output)
            download_format(video_url, audio_format_code, audio_output)
            merge_video_audio(video_output, audio_output, output_file)

            # Cleanup temporary files
            if os.path.exists(video_output):
                os.remove(video_output)
            if os.path.exists(audio_output):
                os.remove(audio_output)

            messagebox.showinfo("Success", f"Video saved as:\n{output_file}")
            status_var.set("Ready")
        except Exception as e:
            messagebox.showerror("Error", f"Processing failed: {str(e)}")
            status_var.set("Error occurred")
        finally:
            merge_btn.config(state=tk.NORMAL)

    threading.Thread(target=worker, daemon=True).start()

# Create main window
app = tk.Tk()
app.title("Decipher YouTube Video Downloader")
app.resizable(True, True)

# Configure grid
app.columnconfigure(1, weight=1)
app.rowconfigure(1, weight=1)

# URL Section
tk.Label(app, text="Video URL:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
url_entry = tk.Entry(app, width=50)
url_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

get_formats_btn = tk.Button(app, text="Get Formats", command=on_download)
get_formats_btn.grid(row=0, column=2, padx=10, pady=10)

# Formats Display
frame = ttk.Frame(app)
frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
frame.columnconfigure(0, weight=1)
frame.rowconfigure(0, weight=1)

scrollbar = tk.Scrollbar(frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

formats_display = tk.Text(frame, width=100, height=20, yscrollcommand=scrollbar.set)
formats_display.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
formats_display.config(state=tk.DISABLED)
scrollbar.config(command=formats_display.yview)

# Format Selection
tk.Label(app, text="Video Format Code:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
video_format_entry = tk.Entry(app, width=20)
video_format_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

tk.Label(app, text="Audio Format Code:").grid(row=3, column=0, padx=10, pady=10, sticky="w")
audio_format_entry = tk.Entry(app, width=20)
audio_format_entry.grid(row=3, column=1, padx=10, pady=10, sticky="w")

# Merge Button
merge_btn = tk.Button(app, text="Download and Merge", command=on_merge)
merge_btn.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

# Status Bar
status_var = tk.StringVar()
status_var.set("Ready")
status_bar = tk.Label(app, textvariable=status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
status_bar.grid(row=5, column=0, columnspan=3, sticky="ew", padx=5, pady=5)

app.mainloop()
