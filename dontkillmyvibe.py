import speech_recognition as sr
from pynput.keyboard import Key, Controller, Listener
import time
from threading import Thread
import subprocess
import json
import os
import tkinter as tk
from tkinter import ttk
import pystray
from PIL import Image, ImageDraw
import ctypes
import sys
import logging

# Setup logging to file
log_file = os.path.join(os.path.dirname(__file__), 'debug.log')
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

# Global debug flag and log widget
DEBUG = False
log_widget = None

def log(message):
    """Log to file, console, and GUI widget"""
    global DEBUG, log_widget
    if DEBUG:
        logger.info(message)
        # Also add to GUI widget if it exists
        if log_widget:
            log_widget.config(state=tk.NORMAL)
            log_widget.insert(tk.END, message + '\n')
            log_widget.see(tk.END)  # Auto scroll
            log_widget.config(state=tk.DISABLED)


def ensure_console():
    """Open a separate PowerShell tail window; closing it won't kill the app"""
    log_path = log_file
    cmd = [
        "powershell",
        "-NoExit",
        "-Command",
        f"Get-Content -Path '{log_path}' -Wait -Tail 200"
    ]
    try:
        subprocess.Popen(cmd, creationflags=subprocess.CREATE_NEW_CONSOLE)
    except Exception:
        pass

# Load config từ file
def load_config():
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        log(f"❌ Config file not found: {config_path}")
        return {'app_path': ''}
    except json.JSONDecodeError:
        log("❌ Invalid JSON in config file")
        return {'app_path': ''}

CONFIG = load_config()

class VoiceController:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.keyboard = Controller()
        self.running = False
        self.pressed_keys = set()
        self.last_alt_time = 0.0
        self.alt_tap_count = 0
        
        self.commands = {
            'save me': self.open_and_play,
            'play': self.play_pause,
            'stop': self.stop_media,
            'next song': self.next_media,
            'previous song': self.previous_media,
            'volume up': self.volume_up,
            'volume down': self.volume_down
        }
    
    def open_and_play(self):
        try:
            log(f"🚀 Opening: {CONFIG['app_path']}")
            subprocess.Popen(CONFIG['app_path'])
            time.sleep(2)  # Chờ app mở
            log("▶️ Playing...")
            self.keyboard.press(Key.media_play_pause)
            self.keyboard.release(Key.media_play_pause)
        except Exception as e:
            log(f"❌ Failed to open app: {e}")

    def play_pause(self):
        self.keyboard.press(Key.media_play_pause)
        self.keyboard.release(Key.media_play_pause)
    
    def stop_media(self):
        # Không có media stop key riêng, dùng play/pause
        self.keyboard.press(Key.media_play_pause)
        self.keyboard.release(Key.media_play_pause)
    
    def next_media(self):
        self.keyboard.press(Key.media_next)
        self.keyboard.release(Key.media_next)
    
    def previous_media(self):
        self.keyboard.press(Key.media_previous)
        self.keyboard.release(Key.media_previous)
    
    def volume_up(self):
        self.keyboard.press(Key.media_volume_up)
        self.keyboard.release(Key.media_volume_up)
    
    def volume_down(self):
        self.keyboard.press(Key.media_volume_down)
        self.keyboard.release(Key.media_volume_down)
    
    def process_audio(self, recognizer, audio):
        """Callback để xử lý audio trong background"""
        try:
            log("🔄 Processing audio...")
            text = recognizer.recognize_google(audio, language='en-US').lower()
            log(f"📝 Detected: {text}")
            
            for command, action in self.commands.items():
                if command in text:
                    log(f"✅ Executing: {command}")
                    # Chạy action trong thread riêng, không block
                    Thread(target=action, daemon=True).start()
                    return
                
        except sr.UnknownValueError:
            log("❌ Could not understand audio")
        except sr.RequestError as e:
            log(f"❌ API error: {e}")
        except Exception as e:
            log(f"❌ Error: {e}")
    
    def run(self):
        self.running = True
        log("🚀 Voice control started!")
        log("🎤 Listening continuously in background...")
        
        # Tạo microphone source
        self.microphone = sr.Microphone()
        
        # Adjust for ambient noise
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
        
        # listen_in_background sẽ nghe liên tục và gọi callback khi có audio
        self.stop_listening = self.recognizer.listen_in_background(
            self.microphone, 
            self.process_audio,
            phrase_time_limit=5  # Giới hạn thời gian mỗi phrase
        )
        
        # Giữ cho thread chạy
        while self.running:
            time.sleep(0.1)
        
        # Dừng background listening khi stop
        if hasattr(self, 'stop_listening'):
            self.stop_listening(wait_for_stop=False)
    
    def stop(self):
        self.running = False
    
    def on_key_press(self, key):
        # Track pressed keys for modifier detection
        self.pressed_keys.add(key)

        # Alt double-tap -> Play/Pause
        if key in (Key.alt, Key.alt_l, Key.alt_r):
            now = time.time()
            if now - self.last_alt_time <= 0.4:
                self.alt_tap_count += 1
            else:
                self.alt_tap_count = 1
            self.last_alt_time = now

            if self.alt_tap_count >= 2:
                Thread(target=self.play_pause, daemon=True).start()
                log("Keyboard: Alt x2 -> Play/Pause")
                self.alt_tap_count = 0
            return

        # Alt-modified arrow hotkeys
        alt_pressed = bool(self.ppressed_alt_keys())
        if alt_pressed:
            if key == Key.up:
                Thread(target=self.volume_up, daemon=True).start()
                log("Keyboard: Alt+Up -> Volume up")
                return
            if key == Key.down:
                Thread(target=self.volume_down, daemon=True).start()
                log("Keyboard: Alt+Down -> Volume down")
                return
            if key == Key.right:
                Thread(target=self.next_media, daemon=True).start()
                log("Keyboard: Alt+Right -> Next song")
                return
            if key == Key.left:
                Thread(target=self.previous_media, daemon=True).start()
                log("Keyboard: Alt+Left -> Previous song")
                return

    def on_key_release(self, key):
        # Remove from pressed set when released
        if key in self.pressed_keys:
            self.pressed_keys.remove(key)

    def ppressed_alt_keys(self):
        # Helper to normalize alt detection (some keyboards report alt/alt_l/alt_r)
        return {Key.alt, Key.alt_l, Key.alt_r}.intersection(self.pressed_keys)

class TrayApp:
    def __init__(self):
        self.controller = VoiceController()
        self.window = None
        self.icon = None
        self.is_running = True
        
    def create_image(self):
        """Load icon from config or create default"""
        icon_path = CONFIG.get('icon_path', '')
        if icon_path and os.path.exists(icon_path):
            try:
                return Image.open(icon_path)
            except Exception as e:
                log(f"❌ Failed to load icon: {e}")
        
        # Create default icon if not found
        width = 64
        height = 64
        image = Image.new('RGB', (width, height), 'blue')
        dc = ImageDraw.Draw(image)
        dc.rectangle([width // 4, height // 4, width * 3 // 4, height * 3 // 4], fill='white')
        return image
    
    def create_window(self):
        self.window = tk.Tk()
        self.window.title("Don't Kill My Vibe")
        self.window.geometry("270x470")
        # Center window on screen
        self.window.update_idletasks()
        w = self.window.winfo_width()
        h = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (w // 2)
        y = (self.window.winfo_screenheight() // 2) - (h // 2)
        self.window.geometry(f"{w}x{h}+{x}+{y}")
        
        # Ngăn window đóng khi nhấn X, thay vào đó minimize to tray
        self.window.protocol("WM_DELETE_WINDOW", self.hide_window)
        
        # Set window icon from config
        icon_path = CONFIG.get('icon_path', '')
        if icon_path and os.path.exists(icon_path):
            try:
                self.window.iconbitmap(icon_path)
            except Exception as e:
                log(f"❌ Failed to set window icon: {e}")
        
        # UI elements
        frame = ttk.Frame(self.window, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        frame.columnconfigure(0, weight=1)  # Make column expand
        
        title_label = ttk.Label(frame, text="Voice & Keyboard Control", font=('Arial', 14, 'bold'))
        title_label.grid(row=0, column=0, pady=10, sticky=(tk.W, tk.E))
        title_label.configure(anchor='center')  # Center align text
        
        status_frame = ttk.LabelFrame(frame, text="Status", padding="10")
        status_frame.grid(row=1, column=0, pady=10, sticky=(tk.W, tk.E))
        status_frame.columnconfigure(0, weight=1)
        
        ttk.Label(status_frame, text="✅ Voice control active", foreground="green").grid(row=0, column=0, sticky=tk.W)
        ttk.Label(status_frame, text="✅ Keyboard control active", foreground="green").grid(row=1, column=0, sticky=tk.W)
        
        commands_frame = ttk.LabelFrame(frame, text="Keyboard Shortcuts", padding="10")
        commands_frame.grid(row=2, column=0, pady=10, sticky=(tk.W, tk.E))
        commands_frame.columnconfigure(0, weight=1)
        
        ttk.Label(commands_frame, text="Alt x2 - Play/Pause").grid(row=0, column=0, sticky=tk.W)
        ttk.Label(commands_frame, text="Alt+Up - Volume up").grid(row=1, column=0, sticky=tk.W)
        ttk.Label(commands_frame, text="Alt+Down - Volume down").grid(row=2, column=0, sticky=tk.W)
        ttk.Label(commands_frame, text="Alt+Right - Next song").grid(row=3, column=0, sticky=tk.W)
        ttk.Label(commands_frame, text="Alt+Left - Previous song").grid(row=4, column=0, sticky=tk.W)
        
        debug_frame = ttk.LabelFrame(frame, text="Debug", padding="10")
        debug_frame.grid(row=3, column=0, pady=10, sticky=(tk.W, tk.E))
        debug_frame.columnconfigure(0, weight=1)

        ttk.Button(debug_frame, text="Open Debug Console", command=self.toggle_debug).grid(row=0, column=0, sticky=tk.W, padx=5)

        button_frame = ttk.Frame(frame)
        button_frame.grid(row=4, column=0, pady=10)
        
        ttk.Button(button_frame, text="Hide to Tray", command=self.hide_window).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Quit", command=self.quit_app).pack(side=tk.LEFT, padx=5)
    
    def show_window(self, icon=None, item=None):
        if self.window:
            self.window.deiconify()
            self.window.lift()
            self.window.focus_force()
    
    def hide_window(self):
        if self.window:
            self.window.withdraw()
    
    def toggle_debug(self):
        global DEBUG
        # Always enable debug and open a new console tail window
        DEBUG = True
        ensure_console()
    
    def quit_app(self, icon=None, item=None):
        self.is_running = False
        self.controller.stop()
        if self.icon:
            self.icon.stop()
        if self.window:
            self.window.quit()
    
    def setup_tray_icon(self):
        menu = pystray.Menu(
            pystray.MenuItem('Show', self.show_window, default=True),
            pystray.MenuItem('Quit', self.quit_app)
        )
        self.icon = pystray.Icon("DontKillMyVibe", self.create_image(), "Don't Kill My Vibe", menu)
        
        # Chạy tray icon trong thread riêng
        Thread(target=self.icon.run, daemon=True).start()
    
    def run(self):
        # Start voice control thread
        Thread(target=self.controller.run, daemon=True).start()
        
        # Start keyboard listener
        listener = Listener(
            on_press=self.controller.on_key_press,
            on_release=self.controller.on_key_release
        )
        listener.start()
        
        # Setup tray icon
        self.setup_tray_icon()
        
        # Create and show window
        self.create_window()
        self.window.mainloop()

if __name__ == "__main__":
    app = TrayApp()
    app.run()