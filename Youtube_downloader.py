from pytube import YouTube
import os
import sys

def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_of_completion = bytes_downloaded / total_size * 100
    sys.stdout.write(f"\rDownloading: {percentage_of_completion:.2f}%")
    sys.stdout.flush()

def list_resolutions(yt):
    streams = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution')
    resolutions = [stream.resolution for stream in streams]
    unique_resolutions = sorted(set(resolutions), key=lambda x: int(x[:-1]))
    return unique_resolutions

def download_video(url, download_path, resolution):
    try:
        yt = YouTube(url, on_progress_callback=on_progress)
        
        # Filter for the desired resolution with audio
        stream = yt.streams.filter(res=resolution, file_extension='mp4', progressive=True).first()
        
        if not stream:
            print(f"\nNo video stream available at {resolution} resolution with audio.")
            return
        
        # Print details
        print(f"\nTitle: {yt.title}")
        print(f"Views: {yt.views}")
        print(f"Length: {yt.length} seconds")
        print(f"Resolution: {stream.resolution}")
        print(f"Downloading to: {download_path}")

        # Download the video
        stream.download(output_path=download_path)
        print("\nDownload completed!")
    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    video_url = input("Enter the YouTube video URL: ")
    download_path = input("Enter the download path (leave blank for current directory): ") or os.getcwd()
    
    yt = YouTube(video_url)
    available_resolutions = list_resolutions(yt)
    print("Available resolutions: ", available_resolutions)
    
    resolution = input(f"Enter the resolution you want to download (e.g., {available_resolutions}): ")
    if resolution not in available_resolutions:
        print(f"Invalid resolution. Please choose from {available_resolutions}.")
    else:
        download_video(video_url, download_path, resolution)

