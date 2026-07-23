import shutil
import subprocess
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

try:
    import yt_dlp
except ImportError:  # pragma: no cover - depends on runtime environment
    yt_dlp = None

BEST_FORMAT = "bestvideo[height<=1080]+bestaudio/best[height<=1080]"


class DownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Decipher YouTube Video Downloader")
        self.root.geometry("640x220")
        self.root.minsize(560, 200)

        style = ttk.Style(self.root)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        self.root.columnconfigure(1, weight=1)

        self.status_var = tk.StringVar(value="Ready")
        self._build_ui()

    def _build_ui(self):
        instructions = (
            "Enter a YouTube URL and download the best available video and audio (up to 1080p), "
            "merged into a single file."
        )
        ttk.Label(self.root, text=instructions, wraplength=580, justify="left").grid(
            row=0, column=0, columnspan=2, padx=12, pady=(14, 10), sticky="w"
        )

        ttk.Label(self.root, text="Video URL:").grid(row=1, column=0, padx=12, pady=10, sticky="w")
        self.url_entry = ttk.Entry(self.root, width=60)
        self.url_entry.grid(row=1, column=1, padx=12, pady=10, sticky="ew")

        self.download_btn = ttk.Button(self.root, text="Download", command=self.on_download)
        self.download_btn.grid(row=2, column=0, columnspan=2, padx=12, pady=14)

        self.status_bar = ttk.Label(
            self.root,
            textvariable=self.status_var,
            anchor="w",
            padding=(8, 4),
        )
        self.status_bar.grid(row=3, column=0, columnspan=2, sticky="ew", padx=5, pady=(0, 6))

    def set_status(self, message):
        self.status_var.set(message)

    def _run_in_thread(self, target, on_error=None, on_finish=None):
        def worker():
            try:
                target()
            except Exception as exc:
                if on_error is not None:
                    self.root.after(0, lambda: on_error(exc))
            finally:
                if on_finish is not None:
                    self.root.after(0, on_finish)

        threading.Thread(target=worker, daemon=True).start()

    def on_download(self):
        video_url = self.url_entry.get().strip()
        if not video_url:
            messagebox.showerror("Error", "Please enter a video URL")
            return

        if not self._is_youtube_url(video_url):
            messagebox.showerror("Error", "Please enter a valid YouTube URL")
            return

        output_file = filedialog.asksaveasfilename(
            defaultextension=".mp4",
            filetypes=[("MP4 files", "*.mp4"), ("All files", "*.*")],
            title="Save Video As",
        )
        if not output_file:
            return

        self.download_btn.state(["disabled"])
        self.set_status("Downloading and merging best quality...")

        def worker():
            download_best(video_url, output_file, progress_hook=self._progress_hook)
            self.root.after(0, lambda: self.set_status("Ready"))
            self.root.after(0, lambda: messagebox.showinfo("Success", f"Video saved as:\n{output_file}"))

        def on_error(exc):
            messagebox.showerror("Error", f"Download failed:\n{exc}")
            self.set_status("Error occurred")

        def on_finish():
            self.download_btn.state(["!disabled"])

        self._run_in_thread(worker, on_error=on_error, on_finish=on_finish)

    def _progress_hook(self, status):
        self.root.after(0, lambda: self.set_status(status))

    @staticmethod
    def _is_youtube_url(url):
        return "youtube.com" in url or "youtu.be" in url


def check_dependencies():
    issues = []
    if not shutil.which("ffmpeg"):
        issues.append("ffmpeg is not installed or is not available in PATH")
    if yt_dlp is None and not shutil.which("yt-dlp"):
        issues.append("yt-dlp is not installed")
    return issues


def download_best(url, output_path, progress_hook=None):
    """Download the best available video+audio (up to 1080p) and merge into output_path."""
    issues = check_dependencies()
    if issues:
        raise RuntimeError("Missing dependencies: " + "; ".join(issues))

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    merge_format = output_path.suffix.lstrip(".") or "mp4"
    outtmpl = str(output_path.with_suffix(""))

    if yt_dlp is not None:
        def hook(d):
            if progress_hook is None:
                return
            if d["status"] == "downloading":
                pct = d.get("_percent_str", "").strip()
                progress_hook(f"Downloading... {pct}")
            elif d["status"] == "finished":
                progress_hook("Merging...")

        options = {
            "format": BEST_FORMAT,
            "outtmpl": outtmpl + ".%(ext)s",
            "merge_output_format": merge_format,
            "quiet": True,
            "no_warnings": True,
            "noplaylist": True,
            "progress_hooks": [hook],
        }
        with yt_dlp.YoutubeDL(options) as downloader:
            downloader.download([url])
        return

    subprocess.run(
        [
            "yt-dlp",
            "-f",
            BEST_FORMAT,
            "--merge-output-format",
            merge_format,
            "-o",
            outtmpl + ".%(ext)s",
            url,
        ],
        check=True,
    )


def main():
    issues = check_dependencies()
    if issues:
        message = "The following requirements are missing:\n- " + "\n- ".join(issues)
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Missing dependencies", message)
        root.destroy()
        return

    root = tk.Tk()
    app = DownloaderApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
