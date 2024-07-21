import os
import subprocess
import sys
import importlib

print(f"Python executable: {sys.executable}")

REQUIRED_PYTHON_VERSION = (3, 6)
REQUIRED_PACKAGES = {
    "tkinter": "tkinter",
    "Pillow": "PIL"
}

def install_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def check_and_import_packages():
    for package, import_name in REQUIRED_PACKAGES.items():
        try:
            importlib.import_module(import_name)
        except ImportError:
            install_package(package)
            importlib.import_module(import_name)

check_and_import_packages()

import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image

root = tk.Tk()
root.title("VideoGUI+ 2.1.6.0")
root.configure(bg="#1e1e1e")

font_style_label = ("Courier", 20, "bold")
font_style_button = ("Courier", 12, "bold")

status_label = tk.Label(root, text="VideoGUI+ 2.1.6.0", bg="#1e1e1e", fg="red", font=("Courier", 31))
status_label.pack(pady=5)

button_frame = tk.Frame(root, bg="#1e1e1e")
button_frame.pack(pady=10)

status_frame = tk.Frame(root, bg="#1e1e1e")
status_frame.pack(pady=10, fill=tk.X)

status_output_label = tk.Label(status_frame, text="", bg="#1e1e1e", fg="white", font=("Courier", 12))
status_output_label.pack(pady=5)

process = None

def display_status(message, color, duration=10):
    status_output_label.config(text=message, fg=color)
    root.after(duration * 1000, clear_status)

def clear_status():
    status_output_label.config(text="")

def select_quality():
    quality_options = ["Low Quality", "Medium Quality", "High Quality", "Same as Source"]
    selected_quality = tk.StringVar(value="Medium Quality")
    
    quality_window = tk.Toplevel(root)
    quality_window.title("Select Quality")
    quality_window.configure(bg="#1e1e1e")

    tk.Label(quality_window, text="Choose a quality profile:", bg="#1e1e1e", fg="white", font=font_style_button).pack(pady=10)
    quality_menu = tk.OptionMenu(quality_window, selected_quality, *quality_options)
    quality_menu.pack(pady=10)

    def on_ok():
        quality_window.destroy()

    tk.Button(quality_window, text="OK", command=on_ok, bg="#3a3a3a", fg="red", font=font_style_button).pack(pady=10)

    root.wait_window(quality_window)
    return selected_quality.get()

def select_resolution():
    resolution_options = ["360p", "480p", "720p", "1080p", "2160p", "Same as Source"]
    selected_resolution = tk.StringVar(value="720p")
    
    resolution_window = tk.Toplevel(root)
    resolution_window.title("Select Resolution")
    resolution_window.configure(bg="#1e1e1e")

    tk.Label(resolution_window, text="Choose a resolution:", bg="#1e1e1e", fg="white", font=font_style_button).pack(pady=10)
    resolution_menu = tk.OptionMenu(resolution_window, selected_resolution, *resolution_options)
    resolution_menu.pack(pady=10)

    def on_ok():
        resolution_window.destroy()

    tk.Button(resolution_window, text="OK", command=on_ok, bg="#3a3a3a", fg="red", font=font_style_button).pack(pady=10)

    root.wait_window(resolution_window)
    return selected_resolution.get()

def select_video_output_format():
    format_options = ["mp4", "mkv", "avi", "mov", "flv", "wmv"]
    selected_format = tk.StringVar(value="mp4")
    
    format_window = tk.Toplevel(root)
    format_window.title("Select Output Format")
    format_window.configure(bg="#1e1e1e")

    tk.Label(format_window, text="Choose an output format:", bg="#1e1e1e", fg="white", font=font_style_button).pack(pady=10)
    format_menu = tk.OptionMenu(format_window, selected_format, *format_options)
    format_menu.pack(pady=10)

    def on_ok():
        format_window.destroy()

    tk.Button(format_window, text="OK", command=on_ok, bg="#3a3a3a", fg="red", font=font_style_button).pack(pady=10)

    root.wait_window(format_window)
    return selected_format.get()

def select_audio_output_format():
    format_options = ["pcm", "wav", "aiff", "mp3", "aac", "ogg", "wma", "flac", "alac"]
    selected_format = tk.StringVar(value="mp3")
    
    format_window = tk.Toplevel(root)
    format_window.title("Select Output Format")
    format_window.configure(bg="#1e1e1e")

    tk.Label(format_window, text="Choose an output format:", bg="#1e1e1e", fg="white", font=font_style_button).pack(pady=10)
    format_menu = tk.OptionMenu(format_window, selected_format, *format_options)
    format_menu.pack(pady=10)

    def on_ok():
        format_window.destroy()

    tk.Button(format_window, text="OK", command=on_ok, bg="#3a3a3a", fg="red", font=font_style_button).pack(pady=10)

    root.wait_window(format_window)
    return selected_format.get()

def normalize_path(path):
    return os.path.abspath(os.path.normpath(os.path.expanduser(path)))

def get_ffmpeg_command(file_path, output_path, hardware, quality, resolution, file_type='video'):
    resolution_map = {
        "360p": "640x360",
        "480p": "854x480",
        "720p": "1280x720",
        "1080p": "1920x1080",
        "2160p": "3840x2160"
    }
    
    resolution_str = resolution_map.get(resolution, "")

    if file_type == 'video':
        if hardware == "nvidia":
            if quality == "Low Quality":
                return ["ffmpeg", "-i", file_path, "-c:v", "h264_nvenc", "-preset", "fast", "-b:v", "1M", "-vf", f"scale={resolution_str}" if resolution_str else "", output_path]
            elif quality == "Medium Quality":
                return ["ffmpeg", "-i", file_path, "-c:v", "h264_nvenc", "-preset", "medium", "-b:v", "2.5M", "-vf", f"scale={resolution_str}" if resolution_str else "", output_path]
            elif quality == "High Quality":
                return ["ffmpeg", "-i", file_path, "-c:v", "h264_nvenc", "-preset", "slow", "-b:v", "5M", "-vf", f"scale={resolution_str}" if resolution_str else "", output_path]
            elif quality == "Same as Source":
                return ["ffmpeg", "-i", file_path, "-c:v", "h264_nvenc", "-preset", "slow", "-crf", "18", output_path]
        elif hardware == "amd":
            if quality == "Low Quality":
                return ["ffmpeg", "-i", file_path, "-c:v", "h264_amf", "-quality", "speed", "-b:v", "1M", "-vf", f"scale={resolution_str}" if resolution_str else "", output_path]
            elif quality == "Medium Quality":
                return ["ffmpeg", "-i", file_path, "-c:v", "h264_amf", "-quality", "balanced", "-b:v", "2.5M", "-vf", f"scale={resolution_str}" if resolution_str else "", output_path]
            elif quality == "High Quality":
                return ["ffmpeg", "-i", file_path, "-c:v", "h264_amf", "-quality", "quality", "-b:v", "5M", "-vf", f"scale={resolution_str}" if resolution_str else "", output_path]
            elif quality == "Same as Source":
                return ["ffmpeg", "-i", file_path, "-c:v", "h264_amf", "-quality", "quality", "-crf", "18", output_path]
        elif hardware == "cpu":
            if quality == "Low Quality":
                return ["ffmpeg", "-i", file_path, "-c:v", "libx264", "-preset", "fast", "-b:v", "1M", "-vf", f"scale={resolution_str}" if resolution_str else "", output_path]
            elif quality == "Medium Quality":
                return ["ffmpeg", "-i", file_path, "-c:v", "libx264", "-preset", "medium", "-b:v", "2.5M", "-vf", f"scale={resolution_str}" if resolution_str else "", output_path]
            elif quality == "High Quality":
                return ["ffmpeg", "-i", file_path, "-c:v", "libx264", "-preset", "slow", "-b:v", "5M", "-vf", f"scale={resolution_str}" if resolution_str else "", output_path]
            elif quality == "Same as Source":
                return ["ffmpeg", "-i", file_path, "-c:v", "libx264", "-preset", "slow", "-crf", "18", output_path]
    elif file_type == 'audio':
        if output_path.endswith(".flac"):
            return ["ffmpeg", "-i", file_path, "-map", "0:a", "-c:a", "flac", output_path]
        else:
            if quality == "Low Quality":
                return ["ffmpeg", "-i", file_path, "-map", "0:a", "-b:a", "64k", output_path]
            elif quality == "Medium Quality":
                return ["ffmpeg", "-i", file_path, "-map", "0:a", "-b:a", "128k", output_path]
            elif quality == "High Quality":
                return ["ffmpeg", "-i", file_path, "-map", "0:a", "-b:a", "192k", output_path]
            elif quality == "Same as Source":
                return ["ffmpeg", "-i", file_path, "-map", "0:a", "-c:a", "copy", output_path]

def play_video():
    global process
    file_path = filedialog.askopenfilename(filetypes=[
        ("Video Files", "*.mp4 *.mkv *.m2ts *.ts *.vob *.avi *.wmv *.mpeg *.mpg")
    ])
    if file_path:
        ffplay_command = ["ffplay", "-autoexit", "-fs", "-sn", normalize_path(file_path)]
        try:
            process = subprocess.Popen(ffplay_command)
            display_status(f"Playing video: {file_path}", "green")
        except Exception as e:
            display_status(f"Error: {e}", "red")

def play_multiple_videos():
    global process
    file_paths = []
    while True:
        file_path = filedialog.askopenfilename(filetypes=[
            ("Video Files", "*.mp4 *.mkv *.m2ts *.ts *.vob *.avi *.wmv *.mpeg *.mpg")
        ])
        if file_path:
            file_paths.append(normalize_path(file_path))
            add_another = messagebox.askquestion("Add another video?", "Would you like to add another video?", icon='question')
            if add_another == 'no':
                break
        else:
            break
    
    for file_path in file_paths:
        ffplay_command = ["ffplay", "-autoexit", "-fs", "-sn", file_path]
        try:
            process = subprocess.Popen(ffplay_command)
            process.wait()
            display_status(f"Playing video: {file_path}", "green")
        except Exception as e:
            display_status(f"Error: {e}", "red")
            break

def handle_conversion_completion():
    messagebox.showinfo("Conversion Completed", "Conversion Completed, Returning to Main Menu")
    root.focus_set()

def convert_video_nvidia():
    quality = select_quality()
    if not quality:
        return
    
    resolution = select_resolution()
    if not resolution:
        return

    output_format = select_video_output_format()
    if not output_format:
        return
    
    file_path = filedialog.askopenfilename(filetypes=[
        ("Video Files", "*.mp4 *.mkv *.m2ts *.ts *.vob *.avi *.wmv *.mpeg *.mpg")
    ])
    if file_path:
        output_dir = normalize_path(filedialog.askdirectory())
        if output_dir:
            output_path = os.path.join(output_dir, os.path.splitext(os.path.basename(file_path))[0] + f".{output_format}")
            ffmpeg_command = get_ffmpeg_command(normalize_path(file_path), output_path, "nvidia", quality, resolution)
            try:
                subprocess.run(ffmpeg_command, check=True)
                display_status(f"Video converted: {output_path}", "green")
                handle_conversion_completion()
            except Exception as e:
                display_status(f"Error: {e}", "red")

def convert_video_amd():
    quality = select_quality()
    if not quality:
        return
    
    resolution = select_resolution()
    if not resolution:
        return

    output_format = select_video_output_format()
    if not output_format:
        return
    
    file_path = filedialog.askopenfilename(filetypes=[
        ("Video Files", "*.mp4 *.mkv *.m2ts *.ts *.vob *.avi *.wmv *.mpeg *.mpg")
    ])
    if file_path:
        output_dir = normalize_path(filedialog.askdirectory())
        if output_dir:
            output_path = os.path.join(output_dir, os.path.splitext(os.path.basename(file_path))[0] + f".{output_format}")
            ffmpeg_command = get_ffmpeg_command(normalize_path(file_path), output_path, "amd", quality, resolution)
            try:
                subprocess.run(ffmpeg_command, check=True)
                display_status(f"Video converted: {output_path}", "green")
                handle_conversion_completion()
            except Exception as e:
                display_status(f"Error: {e}", "red")

def convert_video_cpu():
    quality = select_quality()
    if not quality:
        return
    
    resolution = select_resolution()
    if not resolution:
        return

    output_format = select_video_output_format()
    if not output_format:
        return
    
    file_path = filedialog.askopenfilename(filetypes=[
        ("Video Files", "*.mp4 *.mkv *.m2ts *.ts *.vob *.avi *.wmv *.mpeg *.mpg")
    ])
    if file_path:
        output_dir = normalize_path(filedialog.askdirectory())
        if output_dir:
            output_path = os.path.join(output_dir, os.path.splitext(os.path.basename(file_path))[0] + f".{output_format}")
            ffmpeg_command = get_ffmpeg_command(normalize_path(file_path), output_path, "cpu", quality, resolution)
            try:
                subprocess.run(ffmpeg_command, check=True)
                display_status(f"Video converted: {output_path}", "green")
                handle_conversion_completion()
            except Exception as e:
                display_status(f"Error: {e}", "red")

def convert_music():
    quality = select_quality()
    if not quality:
        return

    output_format = select_audio_output_format()
    if not output_format:
        return
    
    file_path = filedialog.askopenfilename(filetypes=[
        ("Audio Files", "*.pcm *.wav *.aiff *.mp3 *.aac *.ogg *.wma *.flac *.alac")
    ])
    if file_path:
        output_dir = normalize_path(filedialog.askdirectory())
        if output_dir:
            output_path = os.path.join(output_dir, os.path.splitext(os.path.basename(file_path))[0] + f".{output_format}")
            ffmpeg_command = get_ffmpeg_command(normalize_path(file_path), output_path, "cpu", quality, "Same as Source", file_type='audio')
            try:
                subprocess.run(ffmpeg_command, check=True)
                display_status(f"Audio converted: {output_path}", "green")
                handle_conversion_completion()
            except Exception as e:
                display_status(f"Error: {e}", "red")

def convert_multiple_music():
    def add_files():
        file_paths = filedialog.askopenfilenames(filetypes=[
            ("Audio Files", "*.pcm *.wav *.aiff *.mp3 *.aac *.ogg *.wma *.flac *.alac")
        ])
        return list(file_paths)
    
    def add_directory():
        dir_path = normalize_path(filedialog.askdirectory())
        file_paths = []
        if dir_path:
            for root, _, files in os.walk(dir_path):
                for file in files:
                    if file.lower().endswith(('.pcm', '.wav', '.aiff', '.mp3', '.aac', '.ogg', '.wma', '.flac', '.alac')):
                        file_paths.append(os.path.join(root, file))
        return file_paths

    file_paths = []
    choice = messagebox.askquestion("Add files or directory?", "Would you like to add multiple files?", icon='question')
    if choice == 'yes':
        file_paths.extend(add_files())
    else:
        dir_choice = messagebox.askquestion("Add directory?", "Would you like to add a directory instead?", icon='question')
        if dir_choice == 'yes':
            file_paths.extend(add_directory())
    
    if not file_paths:
        return
    
    quality = select_quality()
    if not quality:
        return

    output_format = select_audio_output_format()
    if not output_format:
        return

    output_dir = normalize_path(filedialog.askdirectory())
    if not output_dir:
        return

    for file_path in file_paths:
        output_path = os.path.join(output_dir, os.path.splitext(os.path.basename(file_path))[0] + f".{output_format}")
        ffmpeg_command = get_ffmpeg_command(normalize_path(file_path), output_path, "cpu", quality, "Same as Source", file_type='audio')
        try:
            subprocess.run(ffmpeg_command, check=True)
            display_status(f"Audio converted: {output_path}", "green")
        except Exception as e:
            display_status(f"Error: {e}", "red")
    
    handle_conversion_completion()

def is_ffmpeg_installed():
    try:
        subprocess.run(["ffmpeg", "-version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError:
        return False
    except FileNotFoundError:
        return False

def install_ffmpeg():
    if is_ffmpeg_installed():
        user_choice = messagebox.askquestion("FFmpeg Detected", "FFmpeg is already installed. Would you like to reinstall it?")
        if user_choice != 'yes':
            display_status("FFmpeg is already installed", "green")
            return
    
    result = messagebox.askquestion("Install FFmpeg (full)", "This is the easy way to install FFmpeg if you don’t have it installed on your system. The ‘CTT Script Multimedia Tools FFmpeg (full)’ is listed as the 9th item. Do you want to proceed?")
    if result == 'yes':
        try:
            subprocess.run(["powershell", "-Command", "Start-Process powershell -ArgumentList 'iwr -useb https://christitus.com/win | iex' -Verb RunAs"], check=True)
            display_status("FFmpeg installed successfully", "green")
        except subprocess.CalledProcessError as e:
            display_status(f"Error: {e}", "red")
        except Exception as e:
            display_status(f"Unexpected error: {e}", "red")

def convert_pictures():
    input_format = select_picture_format("Input")
    if not input_format:
        return
    
    output_format = select_picture_format("Output")
    if not output_format:
        return

    choice = messagebox.askquestion("Convert multiple images?", "Would you like to convert multiple images?", icon='question')
    if choice == 'yes':
        file_paths = []
        while True:
            file_path = filedialog.askopenfilename(filetypes=[
                ("Image Files", "*.jpeg *.jpg *.png *.gif *.webp *.tiff *.bmp *.svg *.heif *.heic")
            ])
            if file_path:
                file_paths.append(file_path)
                add_another = messagebox.askquestion("Add another image?", "Would you like to add another image?", icon='question')
                if add_another == 'no':
                    break
            else:
                break
    else:
        file_path = filedialog.askopenfilename(filetypes=[
            ("Image Files", "*.jpeg *.jpg *.png *.gif *.webp *.tiff *.bmp *.svg *.heif *.heic")
        ])
        if file_path:
            file_paths = [file_path]

    output_dir = normalize_path(filedialog.askdirectory())
    if output_dir:
        for file_path in file_paths:
            output_path = os.path.join(output_dir, os.path.splitext(os.path.basename(file_path))[0] + f".{output_format.lower()}")
            try:
                with Image.open(file_path) as img:
                    img.save(output_path, format=output_format.upper())
                display_status(f"Image converted to {output_format.upper()} and saved to {output_path}", "green")
            except Exception as e:
                display_status(f"Error: {e}", "red")

def select_picture_format(prompt):
    format_options = ["JPEG", "PNG", "GIF", "WebP", "TIFF", "BMP", "SVG", "HEIF"]
    selected_format = tk.StringVar(value="JPEG")
    
    format_window = tk.Toplevel(root)
    format_window.title(f"Select {prompt} Format")
    format_window.configure(bg="#1e1e1e")

    tk.Label(format_window, text=f"Choose a {prompt.lower()} format:", bg="#1e1e1e", fg="white", font=font_style_button).pack(pady=10)
    format_menu = tk.OptionMenu(format_window, selected_format, *format_options)
    format_menu.pack(pady=10)

    def on_ok():
        format_window.destroy()

    tk.Button(format_window, text="OK", command=on_ok, bg="#3a3a3a", fg="red", font=font_style_button).pack(pady=10)

    root.wait_window(format_window)
    return selected_format.get()

play_button = tk.Button(button_frame, text="Find Video Media", command=play_video, bg="#1e1e1e", fg="red", font=font_style_button)
play_button.grid(row=0, column=0, padx=10, pady=10)

play_multiple_videos_button = tk.Button(button_frame, text="Play Multiple Videos", command=play_multiple_videos, bg="#1e1e1e", fg="red", font=font_style_button)
play_multiple_videos_button.grid(row=0, column=1, padx=10, pady=10)

convert_button_nvidia = tk.Button(button_frame, text="Convert Video (NVIDIA)", command=convert_video_nvidia, bg="#1e1e1e", fg="red", font=font_style_button)
convert_button_nvidia.grid(row=0, column=2, padx=10, pady=10)

convert_button_amd = tk.Button(button_frame, text="Convert Video (AMD)", command=convert_video_amd, bg="#1e1e1e", fg="red", font=font_style_button)
convert_button_amd.grid(row=0, column=3, padx=10, pady=10)

convert_button_cpu = tk.Button(button_frame, text="Convert Video (CPU)", command=convert_video_cpu, bg="#1e1e1e", fg="red", font=font_style_button)
convert_button_cpu.grid(row=0, column=4, padx=10, pady=10)

convert_music_button = tk.Button(button_frame, text="Convert Music", command=convert_music, bg="#1e1e1e", fg="red", font=font_style_button)
convert_music_button.grid(row=1, column=0, padx=10, pady=10)

convert_multiple_music_button = tk.Button(button_frame, text="Convert Multiple Music", command=convert_multiple_music, bg="#1e1e1e", fg="red", font=font_style_button)
convert_multiple_music_button.grid(row=1, column=1, padx=10, pady=10)

install_ffmpeg_button = tk.Button(button_frame, text="CTT", command=install_ffmpeg, bg="#1e1e1e", fg="red", font=font_style_button)
install_ffmpeg_button.grid(row=1, column=2, padx=10, pady=10)

convert_pictures_button = tk.Button(button_frame, text="Convert Pictures", command=convert_pictures, bg="#1e1e1e", fg="red", font=font_style_button)
convert_pictures_button.grid(row=1, column=3, padx=10, pady=10)

root.mainloop()
