import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
import threading
import subprocess
import time
import os
import main2
import pygame


# === Paths ===
gif_dir = "gifs"
gifs = {
    "starting": os.path.join(gif_dir, "starting.gif"),
    "auth_success": os.path.join(gif_dir, "auth_success.gif"),
    "auth_fail": os.path.join(gif_dir, "auth_fail.gif"),
    "listening": os.path.join(gif_dir, "listening.gif"),
    "terminate": os.path.join(gif_dir, "terminate.gif")
}
music_path = "music/kuromi_music.mp3"
python_path = r"path to python file"
assistant_script = "main.py"

# === Music ===
def play_music(path, loop=False):
    pygame.mixer.init()
    pygame.mixer.music.load(path)
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1 if loop else 0)

def stop_music():
    pygame.mixer.music.stop()


# === GUI setup ===
root = tk.Tk()
root.title("Kuromi Assistant 💀")
root.geometry("600x600")
root.configure(bg="black")

# --- Title at top ---
title_label = tk.Label(root, text="💀 Kuromi Assistant 💀", font=("Comic Sans MS", 20, "bold"),
                       bg="black", fg="#ff69b4")
title_label.pack(pady=10)

# --- GIF Display ---
gif_label = tk.Label(root, bg="black")
gif_label.pack(pady=(0, 10))

# --- Status below gif ---
status_label = tk.Label(root, text="", font=("Arial", 12, "italic"),
                        bg="black", fg="#ffb6c1")
status_label.pack()

# --- Output box below status ---
output_text = tk.Text(root, bg="black", fg="white", font=("Consolas", 11), wrap=tk.WORD)
output_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# === Helpers ===
gif_animation = None

def set_status(text):
    status_label.config(text=text)

def quit_app():
    stop_music()
    set_status("Exiting... See ya, cutie~")
    root.after(1500, lambda: (root.quit(), root.destroy()))

def play_gif(path, duration=None, on_finish=None):
    global gif_animation
    try:
        gif = Image.open(path)
        frames = [ImageTk.PhotoImage(f.copy().convert('RGBA')) for f in ImageSequence.Iterator(gif)]
    except Exception as e:
        print(f"⚠️ Error loading gif: {e}")
        return

    if gif_animation:
        root.after_cancel(gif_animation)

    gif_label.config(image='')
    gif_label.image = None

    def animate(index=0):
        global gif_animation
        gif_label.config(image=frames[index])
        gif_label.image = frames[index]
        gif_animation = root.after(100, animate, (index + 1) % len(frames))

    animate()
    if duration:
        root.after(int(duration * 1000), lambda: on_finish() if on_finish else None)
    elif on_finish:
        root.after(100, on_finish)

# === Assistant logic ===
def run_assistant():
    set_status("✨ Assistant is now active~")
    output_text.delete(1.0, tk.END)

    try:
        process = subprocess.Popen(
            [python_path, assistant_script],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )

        def read_output():
            for line in iter(process.stdout.readline, ''):
                output_text.insert(tk.END, line)
                output_text.see(tk.END)
            process.stdout.close()
            process.wait()
            set_status("Terminating... 👋")
            stop_music()
            play_gif(gifs["terminate"], duration=4, on_finish=quit_app)

        threading.Thread(target=read_output, daemon=True).start()

    except Exception as e:
        output_text.insert(tk.END, f"Error: {e}\n")
        quit_app()

def run_listening():
    set_status("🎧 I'm listening... Tell me your secrets~")
    play_music(music_path, loop=True)
    play_gif(gifs["listening"])
    run_assistant()

def do_authentication():
    set_status("🔐 Authenticating...")
    try:
        result = main2.authenticate_face()
        if result:
            set_status("✅ Authentication successful! Hello cutie~")
            play_music(music_path)
            play_gif(gifs["auth_success"], duration=3, on_finish=run_listening)
        else:
            set_status("❌ Authentication failed. Bye~")
            play_gif(gifs["auth_fail"], duration=3, on_finish=quit_app)
    except Exception as e:
        set_status(f"Error during authentication: {e}")
        quit_app()

def start_sequence():
    set_status("🌀 Waking up Kuromi~")
    play_music(music_path)
    play_gif(gifs["starting"], duration=3, on_finish=lambda: threading.Thread(target=do_authentication).start())

# === Auto-launch ===
print("✨ GUI loaded. Auto-launching Kuromi Assistant...")
root.after(1000, start_sequence)
root.mainloop()
